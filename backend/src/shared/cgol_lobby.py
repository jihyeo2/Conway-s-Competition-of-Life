from src.shared.cgol import *
from src.shared.cgoldefault import *
from abc import ABC

from typing import Optional
from datetime import datetime, timedelta
from tzlocal import get_localzone

def get_current_time():
    return datetime.now(get_localzone())

"""A lobby class to temporarily hold players before a game starts.
Once, ready the game can be started using start_game. Then, based on the settings
an instance of the game will be created and returned back to the user."""

# Also an example of chain of command pattern. The CGOLLobby passes
# responsibility for the actual game to a CGOL subclass when the game
# is ready to actually start. This change could allow us in the future to
# handle players differently before the game starts without having to
# change the logic of the game class. Thus each class better serves a single
# reponsibility improving overall reusability. It also is an example of using
# a factory pattern. The CGOLLobby class does not know the exact set of settings
# it will be provided and the settings determine the final version of the game 
# that is used (and the settings provided to that game). It is able
# to do its job with the CGOL interface which represents the items that all
# CGOL games must implement, and serves as a factory for the instance of CGOL
# that the settings class wants to generate

class CGOLLobby():
    def __init__(self, settings: CGOLSettings):
        self.players = []
        self.start_time = get_current_time()
        self.settings = settings
        
    """Attempts to add a player to the lobby, returns true if player was added, false otherwise."""
    def add_player(self, player: Player):
        if not self._verify(player):
            return False
        self.players.append(player)
        return True
        
    def start_game(self):
        return self.settings.game(self.settings, self.players)

    def _verify(self, player: Player):
        for player_compare in self.players:
            if player_compare.username == player.username or player.color_no == player_compare.color_no:
                return False
        return True
    
    def get_elapsed_time(self):
        if self.start_time is None:
            return -1
        current_time = get_current_time()
        return (current_time - self.start_time).total_seconds()        