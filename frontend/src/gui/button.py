# gui/button.py : frontend : Fall '23 CS3300 Team 10
# This script is the button class for the frontend.
# This is where the button class will be defined.

import pygame as pg

class Button():

    def __init__(self, text, font, font_color, x, y, color, border_width, border_color):
        
        self.font = font                                                # PyGame Font Object
        self.font_color = font_color                                    # Font Color
        self.text = font.render(text, True, font_color)                 # Button Label

        self.rect = pg.Rect(x, y, self.text.get_width() + 10,           # Button Rectangle
                            self.text.get_height() + 10)                #
        self.color = color                                              # Button Color
        
        self.border_width = border_width                                # Border Width
        self.border_color = border_color                                # Border Color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)                             # Draw Button
        screen.blit(self.text, (self.rect.x + 5, self.rect.y + 5))              # Draw Label
        pg.draw.rect(screen, self.border_color, self.rect, self.border_width)   # Draw Border

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
