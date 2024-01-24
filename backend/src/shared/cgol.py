#import numpy as np
from abc import ABC
from abc import abstractmethod, abstractproperty
from typing import List

"""
A coordinate class to represent the coordinates that a player can place squares on. 
0,0 is the top left corner. Coordinates MUST be positive integers.

"""
class Coordinate:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

"""
A Player class to store information about a player
"""
class Player:
    username: str
    color_no: int
    
    def __init__(self, username: str, color_no: int):
        self.username = username
        self.color_no = color_no

"""
A class to store infomation on update
"""
class SquareUpdate:
    player: Player
    location: Coordinate
    update: int #must be 0 is for now - player place (in the future this value can 
                #allow players to do more than just place
    def __init__(self, player: Player, location: Coordinate, update: int):
        self.player = player
        self.location = location
        self.update = update

"""
This class is meant to be a base class for a basic gameboard in conways game of life
"""
class CGOL(ABC):
    def __init__(self, settings, players: List[Player]):
        self.x_size = settings.x_size
        self.y_size = settings.y_size
        self._players = players

        self.stats = [PlayerStats(i) for i in players]

    @abstractproperty
    def board(self):
        """
        Returns a numpy array with the current state of the board.
        Empty space is represented by 0, Food by 1 and players with all higher values
        """
        pass
    
    @abstractproperty
    def players(self):
        """Returns the list of players for this game"""
        pass
    
    @players.setter
    def players(self, players: List[Player]):
        self._players = players

    @abstractmethod
    def update_board(self, square_updates : List[SquareUpdate]):
        """
        Update the board according to the rules of conways game of life.
        """ 
        pass

    @abstractmethod
    def step(self):
        """
        Function to update the game board by one step according to the rules.
        """
        pass

    def get_stats(self):
        """Returns the stats for each player"""
        return self.stats

# Command Pattern allows us to use polymorphism to define the exact
# game instance at runtime. This allows us to make variants with custom instructions

""" Settings class that represents the default settings for the game 
the game field is a reference to the CGOL implementation that these settings are for"""

class CGOLSettings(ABC):
    game = None
    x_size = 10
    y_size = 10

    def __init__(self, x_size = 10, y_size = 10):
        self.x_size = x_size
        self.y_size = y_size

    @abstractmethod
    def create_game(self):
        pass #creates a game instance and returns it

class PlayerStats(ABC):
    player = None
    cells_created = 0 # Total number of cells a user had come alive (without the user placing it)
    contested_areas = 0 # Number of times a users cell prevented another capture
    total_food_captured = 0 # Total amount of food captured

    def __init__(self, player: Player):
        self.player = player