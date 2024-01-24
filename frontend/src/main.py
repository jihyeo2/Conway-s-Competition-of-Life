# main.py : frontend : Fall '23 CS3300 Team 10
# This script is the main client runtime for the frontend.
# This is where the main game loop will go.

import settings as s
import menu_screen as ms
import gui.button as button
import grid.grid as g
import gui.popup as popup

import requests
import sys 
from enum import Enum

import pygame
import time

pygame.init()

# --- Display Setup -------------------------------------------------------------------------------
pygame.display.set_caption(s.WINDOW_TITLE)  # Set window title
screen = None

# Set display to fullscreen if settings.USE_FULLSCREEN is True
if s.USE_FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | s.WINDOW_FLAGS, 
                                    display=s.USE_DISPLAY)

    # Set window size to whatever the display size is
    s.WINDOW_WIDTH = screen.get_width()
    s.WINDOW_HEIGHT = screen.get_height()

else:
    screen = pygame.display.set_mode((s.WINDOW_WIDTH, s.WINDOW_HEIGHT), s.WINDOW_FLAGS, 
                                    display=s.USE_DISPLAY)
# --- Display Setup -------------------------------------------------------------------------------

# --- Game State ----------------------------------------------------------------------------------
class GameState(Enum):
    MENU = 0
    GAME = 1
    WAITING = 2
    END = 3
# --- Game State ----------------------------------------------------------------------------------



def main():    

    # Loop Semaphore
    run_game = True

    clocked = 0

    # Game State
    game_state = GameState.MENU

    # Game url
    url = s.API_URL

    # Username
    username = ""
    user_color_no = '1'

    # Submit button
    submit_button = button.Button("Submit", pygame.font.Font(None, 36), s.BLACK, 
                                    s.WINDOW_WIDTH - 250, 20, 
                                    s.WHITE, 2, s.BLACK)

    # Menu Screen
    menu = ms.MenuScreen(screen)

    # Grid
    grid = g.Grid(screen)
    #grid.update('1511,0100,0151,1234')      # Test pattern

    # Stats
    stats_popup = popup.Popup(600, 600)

    while run_game:

        # --- Event handling ----------------------------------------------------------------------
        for event in pygame.event.get():

            # Exit events
            if event.type == pygame.QUIT:
                pygame.quit()
                run_game = False        # This is redundant, but here for clarity, and in case we
                sys.exit()              # add exit conditions without directly sys.exit()ing

            # Keypress events
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:        # Exit on escape key
                    pygame.quit()
                    run_game = False
                    sys.exit()

            if game_state == GameState.MENU:
                menu_ret = menu.event_handler(event)
                if menu_ret != None:
                    username = menu_ret
                    result = requests.post(url + "/register", json={'username': username})
                    if result:
                        userdata = result.json()
                        user_color_no = str(userdata['color_no'])
                        user_color = s.COLORS[user_color_no]
                        menu.user_color = user_color
                        menu.error_message_active = False
                        game_state = GameState.WAITING
                    else:
                        menu.error_message_text = result.json()['detail']
                        menu.error_message_active = True                    

            elif game_state == GameState.GAME:
                grid.event_handler(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if submit_button.collidepoint(event.pos):
                        send = f'"username": "{username}", "newCells": "{grid.get_new_cells_str()[:-1]}"'
                        send = "{" + send + "}"
                        # >>>>>>>>>>> Send new cells to server <<<<<<<<<<<<
                        request_not_work = True
                        while request_not_work:
                            try:
                                response = requests.post(s.API_URL + "/submit", json=send)
                                grid.update(response.json()["board"])
                                request_not_work = False
                            except Exception as e:
                                print(e)
                        

        # --- Event handling ----------------------------------------------------------------------


        # --- Game logic --------------------------------------------------------------------------
        
        if game_state == GameState.WAITING:
            try:
                menu.waiting = True
                lobby_data = requests.get(url + "/lobby").json()
                waiting, num_players = lobby_data['waiting'], lobby_data['num_players']
                menu.update_num_players(num_players)
                if not waiting:
                    game_state = GameState.GAME
            except:
                pass

        # >>>>>>>>>>> Get updated grid from server <<<<<<<<<<<<
        elif game_state == GameState.GAME:

            if clocked % 120 == 0:
                try:
                    response = requests.get(s.API_URL + "/update")
                    grid.update(response.json()["board"])
                    if response.json()["end"]:
                        game_state = GameState.END
                except:
                    pass
        
        elif game_state == GameState.END:
            try:
                stats = requests.get(url + "/stats").json()
                stats_popup.update_player_info(stats)
                # added delay to make sure to have stats data before drawing a popup
                time.sleep(3)
                stats_popup.show()
            except:
                pass


        # --- Game logic --------------------------------------------------------------------------


        # --- Draw Logic --------------------------------------------------------------------------
        screen.fill((255, 255, 255))      # Make white background

        clock = pygame.time.Clock()
        clock.tick(s.FPS)                 # Set frame rate

        if game_state == GameState.MENU or game_state == GameState.WAITING:
            menu.draw()
        elif game_state == GameState.GAME:
            grid.draw()
            submit_button.draw(screen)
        elif game_state == GameState.END:
            grid.draw()
            stats_popup.draw(screen)
        # --- Draw Logic --------------------------------------------------------------------------

        # Update the display
        pygame.display.flip()
        clocked += 1

if __name__ == "__main__":
    main()
