import sys
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.states.state import State
from TotLH.states.states import States

class Congratulations(State):

    def __init__(self):
        super().__init__()
        self.next_state = States.Intro

        with resources.path(cfg_item("fonts", "congratulations", "path"), cfg_item("fonts", "congratulations", "filename")) as instructions_path:
            congratulations_font = pygame.font.Font(instructions_path, cfg_item("fonts", "congratulations", "config", "congratulations_size"))
            explanation_font = pygame.font.Font(instructions_path, cfg_item("fonts", "congratulations", "config", "text_size"))

        with resources.path(cfg_item("scenario", "congratulations", "path"), cfg_item("scenario", "congratulations", "filename")) as congratulations_image_path:
            congratulations_image=pygame.image.load(congratulations_image_path).convert_alpha()
            self.__congratulations_image_resized = pygame.transform.scale(congratulations_image, cfg_item("game", "screen_size")).convert_alpha()

        self.__congratulations_text = congratulations_font.render(cfg_item("fonts", "congratulations", "config", "congratulations"), True, cfg_item("fonts", "congratulations", "config", "color"))
        self.__explanation_text = explanation_font.render(cfg_item("fonts", "congratulations", "config", "text"), True, cfg_item("fonts", "congratulations", "config", "color"))


    def __del__(self):
        pass

    def enter(self):
        self.done = False

    def exit(self):
        pass

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: 
            self.done = True


    def handle_menu_click(self, pos):
        pass


    def handle_events(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self, screen):
        screen.blit(self.__congratulations_image_resized,(0,0))
        screen.blit(self.__congratulations_text, cfg_item("fonts", "congratulations", "config", "congratulations_pos"))
        screen.blit(self.__explanation_text, cfg_item("fonts", "congratulations", "config", "text_pos"))
