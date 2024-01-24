# gui/popup.py : frontend : Fall '23 CS3300 Team 10
# This script is the popup class for the frontend.
# This is where the popup class will be defined.

import pygame as pg
import settings as s

class Popup():
    
    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        self.rect = pg.Rect(0, 0, width, height)
        self.rect.center = (s.WINDOW_WIDTH // 2, s.WINDOW_HEIGHT // 2)
        self.surface = pg.Surface((width, height))
        self.visible = False
        self.player_info = []     
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False

    def update_player_info(self, player_info):
        self.player_info = player_info          

    def draw(self, screen):

        # Draw black border
        pg.draw.rect(self.surface, s.BLACK, (0, 0, self.width, self.height))

        # Draw white background
        pg.draw.rect(self.surface, s.WHITE, (0, 0, self.width, self.height))

        # Draw text on the popup
        font_header = pg.font.Font(None, 64) # Header font size
        font_data = pg.font.Font(None, 28)   # Data font size

        # Display header
        header_surface = font_header.render("Game Over", True, s.BLUE)
        header_rect = header_surface.get_rect(center=(self.width // 2, 60))
        self.surface.blit(header_surface, header_rect)

        # Display player information
        y_offset = 150  # Starting Y position for the first player's info
        for player_data in self.player_info:
            username = player_data['player']['username']
            cells_created = str(player_data['cells_created']) if 'cells_created' in player_data.keys() else "NA"
            contested_areas = str(player_data['contested_areas']) if 'contested_areas' in player_data.keys() else "NA"
            total_food_captured = str(player_data['total_food_captured']) if 'total_food_captured' in player_data.keys() else "NA"

            # Display player username
            username_surface = font_data.render(f"Player - {username}", True, s.BLACK)
            username_rect = username_surface.get_rect(center=(self.width // 2, y_offset))
            self.surface.blit(username_surface, username_rect)

            # Display cells created
            cells_created_surface = font_data.render(f"Cells Created: {cells_created}", True, s.BLACK)
            cells_created_rect = cells_created_surface.get_rect(center=(self.width // 2, y_offset + 30))
            self.surface.blit(cells_created_surface, cells_created_rect)

            # Display contested areas
            cells_created_surface = font_data.render(f"Contested Areas: {contested_areas}", True, s.BLACK)
            cells_created_rect = cells_created_surface.get_rect(center=(self.width // 2, y_offset + 60))
            self.surface.blit(cells_created_surface, cells_created_rect)

            # Display total food captured
            total_food_captured_surface = font_data.render(f"Total Food Captured: {total_food_captured}", True, s.BLACK)
            total_food_captured_rect = total_food_captured_surface.get_rect(center=(self.width // 2, y_offset + 90))
            self.surface.blit(total_food_captured_surface, total_food_captured_rect)

            y_offset += 180  # Increase Y position for the next player's info

        screen.blit(self.surface, self.rect.topleft)