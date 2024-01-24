from src.shared.cgol import *
import numpy as np
from typing import List

from datetime import datetime, timedelta
from tzlocal import get_localzone

def get_current_time():
    return datetime.now(get_localzone())


"""
A default implementation of the modified version of Conway's Game of Life. We will assume that
all inputs to this class are valid (no duplicate players, negative sizes, etc... ).
"""

class CGOLDefault(CGOL):

    def __init__(self, settings, players_list: List[Player]):
        self.start_time = get_current_time()

        self.spawn_rate = settings.spawn_rate
        self.max_food = settings.max_food
        
        super().__init__(settings, players=players_list)
        self.state = np.zeros((self.x_size, self.y_size))

        self.stats_dict = dict()
        for player_stats in self.stats:
            
            self.stats_dict[player_stats.player.color_no] = player_stats

    @property
    def board(self):
        return self.state

    @board.setter
    def board(self, new_board):
        self.state = new_board

    @property
    def players(self):
        return self._players

    def step(self):
        temp = self.state.copy()
        
        for x in range(self.x_size):
            for y in range(self.y_size):
                neighbors = self._get_cell_neighbors(x,y)
                contestants = self._contesting_players(x,y)
                value = self.state[x,y]

                temp[x,y] = self._cell_update_logic(neighbors, contestants, value)
        
        self.state = temp
        return self.state

    def update_board(self, square_updates: List[SquareUpdate]):
        """Updates the board with a given set of square updates"""
        success = []
        
        for update in square_updates:
            
            location = update.location
            player = update.player
            
            if not self.open_square(location.x, location.y):
                success.append(False)
            else:
                self.state[location.x,location.y] = player.color_no
                success.append(True)
        return success
     
    def open_square(self, x : int, y: int):
        """Returns 1 if the square is open 0 if it is not open for placement"""   
        return self.state[x,y] == 0

    def spawn_food(self, spawn_rate = None, max_food = None):
        """Spawns food on the board in empty spaces with a chance of spawn_rate (uses setting default if not provided)"""
        
        spawn_chance = spawn_rate
        if spawn_rate is None:
            spawn_chance = self.spawn_rate     

        if max_food is None:
            max_food = self.max_food 

        p = [1-spawn_chance, spawn_chance]
        size = self.state.shape
        replacement_mask = np.random.choice([0,1], size = size, p = p)
        
        if np.sum(self.state == 1) > max_food:
            return None
        
        self.state = np.where(self.state == 0, replacement_mask, self.state)

    def _get_cell_neighbors(self, x : int, y: int):
        neighbors = []
        for dx in range(-1,2): # Skip current cell with step
            for dy in range(-1,2):
                
                if dx == 0 and dy == 0:
                    continue

                neighbors.append(self.state[(x+dx) % self.x_size, (y+dy) % self.y_size]) #Wrap around
        return neighbors

    def _contesting_players(self, x : int, y: int):
        player_list = list(set(self._get_cell_neighbors(x,y)))
        return [player for player in player_list if player not in [0,1]]

    def _cell_update_logic(self, neighbors, contesting_players, original_value):
        neighbors = np.array(neighbors)
        nearby_alive = np.sum(neighbors >= 2)
        
        # If two players are near this square, it dies.
        if len(contesting_players) >= 2:
            for contesting_player in contesting_players:
                self.stats_dict[int(contesting_player)].contested_areas += 1
            return 0

        # If no players contest this square and this is not a cell, leave it unchanged
        # If there is a cell there then it dies
        if len(contesting_players) == 0:
            if original_value < 2:
                return original_value
            else:
                return 0

        # If a cell has 3 live neighbors it comes to life
        if (original_value < 2) and (nearby_alive == 3):
            for contesting_player in contesting_players:
                self.stats_dict[int(contesting_player)].cells_created += 1
            if (original_value == 1):
                self.stats_dict[int(contesting_player)].total_food_captured += 1
            return contesting_players[0]

        # if a cell has 2-3 live neighbors it stays alive
        if (original_value >= 2) and (nearby_alive >= 2) and (nearby_alive <= 3):
            return original_value
        
        return 0

    def get_elapsed_time(self):
        if self.start_time is None:
            return -1
        current_time = get_current_time()
        return (current_time - self.start_time).total_seconds()      

class CGOLDefaultSettings(CGOLSettings):
    game = CGOLDefault
    spawn_rate = 0.01
    max_food = 50

    def __init__(self, x_size = 10, y_size = 10):
        super().__init__(x_size, y_size)

    def create_game(self):
        return CGOLDefault(self.x_size, self.y_size, self.players)

#An example variant where the food spawn_chance has been doubled
class CGOLDefaultSettingsSuperFood(CGOLDefaultSettings):
    spawn_chance = CGOLDefaultSettings.spawn_rate*2