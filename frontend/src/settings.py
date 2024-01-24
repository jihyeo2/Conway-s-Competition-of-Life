# settings.py : frontend : Fall '23 CS3300 Team 10
# This script is the game settings file for the frontend.
# This is where the game settings will be stored.

# API URL
API_URL = "http://localhost:3301"

# Disable Welcome Message
DISABLE_PYGAME_WELCOME_MESSAGE = True
import os

if DISABLE_PYGAME_WELCOME_MESSAGE:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Window Settings
WINDOW_TITLE = "Conway's Competition of Life"       # Set window title
WINDOW_WIDTH = 1920                                 # Set window width
WINDOW_HEIGHT = 1080                                # Set window height
FPS = 60                                            # Set frame rate

# Set manually for testing and demo. See pygame docs for details:
# https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
WINDOW_FLAGS = 512 | 16 | -2147483648               # Set window flags

USE_FULLSCREEN = False                              # Set to True to use fullscreen
USE_DISPLAY = 0                                     # Set to 0 to use default display

# Game Settings
CELL_SIZE = 10                                      # Set cell size in pixels
# <<<<< DEPRECATED, CELL SIZE IS NOW DYNAMIC >>>>> 

GRID_ROWS = 30                                      # Set number of rows in grid
GRID_COLS = 60                                      # Set number of columns in grid

# Debug Settings
DEBUG = True                                        # Set to True to enable debug mode
BUILD_VERSION = 'alpha0'                            # Set to current build number

# Color Palette
WHITE   = (255, 255, 255)
BLACK   = (0  , 0  , 0)
GREY    = (128, 128, 128)

RED     = (255, 0  , 0)
GREEN   = (0  , 255, 0)
BLUE    = (0  , 0  , 255)
TEAL    = (0  , 255, 255)
PURPLE  = (255, 0  , 255)


COLORS = {'0': WHITE,  '1': RED, '2': GREEN, '3': BLUE, '4': TEAL, '5': PURPLE, '6': BLACK}
