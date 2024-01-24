# menu_screen.py : frontend : Fall '23 CS3300 Team 10
# This script is the menu screen for the frontend.
# This is where the menu screen will be defined.

import pygame as pg

import sys
import time


import settings as s

import gui.button as button
import gui.label as label
import gui.textbox as textbox

class MenuScreen():

    def __init__(self, screen):
        
        self.screen = screen


        self.logo = pg.image.load("assets/logo.png")
        self.logo_rect = self.logo.get_rect(center=(s.WINDOW_WIDTH // 2, s.WINDOW_HEIGHT // 4))

        # Title Label
        self.title = label.Label("Conway's Competition of Life", pg.font.Font(None, 96), s.BLACK, 
                                 s.WINDOW_WIDTH // 2, s.WINDOW_HEIGHT // 2)

        # Username Label
        self.username_label = label.Label("Username:", pg.font.Font(None, 36), s.BLACK, 
                                          s.WINDOW_WIDTH // 3 - 10, s.WINDOW_HEIGHT // 2 + 215)

        # Text Box
        self.text_box = textbox.Textbox(pg.font.Font(None, 36), s.BLACK, 
                                        s.WINDOW_WIDTH // 2 - 160, s.WINDOW_HEIGHT // 2 + 200, 
                                        300, 36, s.WHITE, 2, s.BLACK)

        self.active_element = None

        # Submit button
        self.submit_button = button.Button("Submit", pg.font.Font(None, 36), s.BLACK, 
                                           s.WINDOW_WIDTH // 2 + 250, s.WINDOW_HEIGHT // 2 + 200, 
                                           s.WHITE, 2, s.BLACK)

        # Error Message
        self.error_message_text = "Error"
        self.error_message = label.Label(self.error_message_text, pg.font.Font(None, 24), s.RED, 
                                         s.WINDOW_WIDTH // 2 - 160, s.WINDOW_HEIGHT // 2 + 245)
        self.error_message_active = False

        # Color Message
        self.color_message = label.Label("User Color: ", pg.font.Font(None, 36), s.BLACK, 
                                         s.WINDOW_WIDTH // 3 - 10, s.WINDOW_HEIGHT // 2 + 255)
       
        # Status Update
        self.state_update = label.Label("Waiting for other players...", pg.font.Font(None, 36), s.BLUE, 
                                         s.WINDOW_WIDTH // 3 - 10, s.WINDOW_HEIGHT // 2 + 315)
        
        self.num_players = 0
        
        # Number of Joined Players
        self.joined_players = label.Label(str(self.num_players) + "/5", pg.font.Font(None, 36), s.BLUE,
                                          s.WINDOW_WIDTH // 2 + 250, s.WINDOW_HEIGHT // 2 + 315)

        self.waiting = False
        self.user_color = None

    def update_num_players(self, num_players: int):
        self.num_players = num_players


    def event_handler(self, event):
        
        if event.type == pg.MOUSEBUTTONDOWN:

            # If text box is clicked, set it to active
            if self.text_box.collidepoint(event.pos):
                self.text_box.set_active(True)
                self.active_element = self.text_box

            # If submit button is clicked, submit username
            elif self.submit_button.collidepoint(event.pos):
                print(f"Username submitted: {self.text_box.value}")
                return self.text_box.value

            # If anything else is clicked, set active element to None
            else:
                if self.active_element != None:
                    self.active_element.set_active(False)
                    self.active_element = None

        # If text box is active, handle keypresses
        if event.type == pg.KEYDOWN:
            if self.active_element != None:
                if event.key == pg.K_RETURN:
                    print(f"Username submitted: {self.text_box.value}")
                    return self.text_box.value
                elif event.key == pg.K_BACKSPACE:
                    self.text_box.set_value(self.text_box.get_value()[:-1])
                else:
                    self.text_box.set_value(self.text_box.get_value() + event.unicode)

        return None

    def draw(self):

        # Draw logo
        self.screen.blit(self.logo, self.logo_rect)

        # Draw title
        self.title.draw(self.screen)

        # Draw username label
        self.username_label.draw(self.screen)

        # Draw input box
        self.text_box.draw(self.screen)

        # Draw submit button
        self.submit_button.draw(self.screen)

        # Draw error message
        if self.error_message_active:
            self.error_message = label.Label(self.error_message_text, pg.font.Font(None, 24), s.RED, 
                                         s.WINDOW_WIDTH // 2 - 160, s.WINDOW_HEIGHT // 2 + 245)
            self.error_message.draw(self.screen)
        
        # Draw color message
        if self.user_color:
            self.color_message.draw(self.screen)
            pg.draw.rect(self.screen, self.user_color, (s.WINDOW_WIDTH // 2 - 160, s.WINDOW_HEIGHT // 2 + 255, 25, 25))
        
        # Draw status update with number of joined players
        if self.waiting:
            self.joined_players = label.Label(str(self.num_players) + "/5", pg.font.Font(None, 36), s.BLUE,
                                          s.WINDOW_WIDTH // 2 + 250, s.WINDOW_HEIGHT // 2 + 315)
            self.state_update.draw(self.screen)
            self.joined_players.draw(self.screen)

