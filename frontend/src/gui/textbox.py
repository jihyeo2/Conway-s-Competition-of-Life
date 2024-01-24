# gui/textbox.py : frontend : Fall '23 CS3300 Team 10
# This script is the textbox class for the frontend.
# This is where the textbox class will be defined.

import pygame as pg

class Textbox():
        
        def __init__(self, font, font_color, x, y, width, height, color, bd_width, bd_color):
            
            self.font = font                                                # PyGame Font Object
            self.font_color = font_color                                    # Font Color
            self.text = None                                                # Rendered Text
            self.value = ""                                                 # Textbox Value
            
            self.rect = pg.Rect(x, y, width, height)                        # Textbox Rectangle
            self.color = color                                              # Textbox Color
            
            self.bd_width = bd_width                                        # Border Width
            self.bd_color = bd_color                                        # Border Color

            self.active = False                                             # Active Flag
    
        def draw(self, screen):

            # Render text
            self.text = self.font.render(self.value, True, self.font_color)
            text_rect = self.text.get_rect(center=(self.rect.x + self.rect.width // 2, 
                                                   self.rect.y + self.rect.height // 2))

            pg.draw.rect(screen, self.color, self.rect)                     # Draw Textbox
            screen.blit(self.text, text_rect)                               # Draw Text
            pg.draw.rect(screen, self.bd_color, self.rect, self.bd_width)   # Draw Border

        def collidepoint(self, pos):
            return self.rect.collidepoint(pos)

        def set_value(self, value):
            self.value = value

        def get_value(self):
            return self.value

        def set_active(self, active):
            self.active = active

        def get_active(self):
            return self.active