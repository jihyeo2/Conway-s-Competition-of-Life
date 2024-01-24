# api.py : backend : Fall '23 CS3300 Team 10
# This script is the root endpoint of the backend API.

from fastapi import FastAPI, HTTPException, Request
from typing import Set
from pydantic import BaseModel
from contextlib import asynccontextmanager

import src.settings as s
import src.shared.cgol_lobby as cl
import src.shared.cgol as cg
import src.shared.cgoldefault as cgd

import ast
import asyncio
from datetime import datetime, timedelta
import json
import threading


# in-game memory
usernames: Set[str] = set()
lobby = None
game = None
game_lock = threading.Lock()

last_tick = None

settings = cl.CGOLDefaultSettings(s.BOARD_WIDTH, s.BOARD_HEIGHT)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global lobby, game
    lobby = cl.CGOLLobby(settings)
    print("started", flush=True)

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return 'Hello World!'

class RegistrationInfo(BaseModel):
    username: str

# class SubmissionInfo(BaseModel):
#     username: str
#     newCells: str

# registration
@app.post("/register")
async def register(r: RegistrationInfo):

    global lobby, game, last_tick
    username = r.username

    # checks if the username exists
    if username in usernames:
        raise HTTPException(status_code=400, detail="Username already taken.")
    
    usernames.add(username)
    player = None

    # find an existing lobby with an available spot
    if lobby:
        if len(lobby.players) < s.MAX_PLAYERS_PER_GAME:
            remaining_colors = list(set(s.COLOR_NOS) - set([p.color_no for p in lobby.players]))
            player = cl.Player(username, remaining_colors[0])
            lobby.add_player(player)
            if (len(lobby.players) == s.MAX_PLAYERS_PER_GAME):
                game = lobby.start_game()
                last_tick = datetime.now()
        else:
            raise HTTPException(status_code=400, detail="Room is full.")
    
    # If none available, create a new lobby
    else:
        player = cl.Player(username, 2)
        lobby = cl.CGOLLobby(settings)
        lobby.add_player(player)

    return player
        
# lobby
@app.get("/lobby")
async def check_lobby():
    if lobby:
        num_players = len(lobby.players)
        if num_players == s.MAX_PLAYERS_PER_GAME:
            return {"waiting": False, "num_players": num_players}
        
        elapsed_time = lobby.get_elapsed_time()
        if elapsed_time == -1:
            raise HTTPException(status_code=400, detail="Lobby Timer uninitialized.")
        waiting = False if (elapsed_time >= 180 and num_players >= 2) else True

        return {"waiting": waiting, "num_players": num_players}
    
    raise HTTPException(status_code=400, detail="Lobby Invalidated.")

@app.post("/submit")
async def submit(request: Request):
    try:
        await game_update()
        jsonPayload = await request.json()
        print(jsonPayload)
        jsonPayload = json.loads(jsonPayload)
    
        newCells = jsonPayload["newCells"]
        cells = ast.literal_eval(f'[{newCells}]')
        target_player = None
        
        print(jsonPayload["username"])
        with game_lock:
            for player in game.players:
                if player.username == jsonPayload["username"]:
                    target_player = player
                    
            if not target_player:
                raise HTTPException(status_code=404, detail="Player not found")
                
            update_list = []
            for cell in cells:
                location = cg.Coordinate(cell[0], cell[1])
                update = cg.SquareUpdate(target_player, location, 0)
                update_list.append(update)
            game.update_board(update_list)
            
    except Exception as e:
        print(e)
    
    return {"board": json.dumps(game.board.astype(int).tolist())}
    
@app.get("/update")
async def update():
    await game_update()
    end_game = False
    if game:
        elapsed_time = game.get_elapsed_time()
        if elapsed_time > s.GAME_TIME_SECONDS:
            end_game = True
    return {"board": json.dumps(game.board.astype(int).tolist()), "end": end_game}

@app.get("/stats")
async def stats():
    return game.stats

async def game_update():
    global last_tick
    try:
        if game:
            with game_lock:
                diff = datetime.now() - last_tick
                
                print
                ticks = max(int(diff.total_seconds() / s.SECONDS_PER_TICK), 0)
                for i in range(0, ticks):
                    game.step()
                    game.spawn_food()
                
                print(datetime.now(), last_tick, diff.total_seconds(), ticks)
                last_tick = last_tick + timedelta(seconds=s.SECONDS_PER_TICK * ticks)
                
                return ticks
        return None
    except Exception as e:
        print(e)