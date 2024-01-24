# gui/label.py : frontend : Fall '23 CS3300 Team 10
# This script is the label class for the frontend.
# This is where the label class will be defined.

import pygame as pg

class Label():
    
    def __init__(self, text, font, font_color, x, y):
        
        self.font = font                                                # PyGame Font Object
        self.font_color = font_color                                    # Font Color
        self.text = font.render(text, True, font_color)                 # Button Label

        # Label Rectangle
        self.rect = pg.Rect(x - self.text.get_width() // 2, y - self.text.get_height() // 2,
                            self.text.get_width(), self.text.get_height())

    def draw(self, screen):
        screen.blit(self.text, (self.rect.x, self.rect.y))              # Draw Label
