import sys
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.states.intro import Intro
from TotLH.states.state import State
from TotLH.states.states import States

class Instructions(State):

    def __init__(self):
        super().__init__()
        self.next_state = States.Intro

        # Instructions text
        with resources.path(cfg_item("fonts", "instructions", "path"), cfg_item("fonts", "instructions", "filename")) as instructions_path:
            gameplay_font = pygame.font.Font(instructions_path, cfg_item("fonts", "instructions", "config", "gameplay_size"))
            instructions_font = pygame.font.Font(instructions_path, cfg_item("fonts", "instructions", "config", "instructions_size"))

        self.__melee_attack_text = gameplay_font.render(cfg_item("fonts", "instructions", "config", "melee_attack"), True, cfg_item("fonts", "instructions", "config", "color"))
        self.__arrows_text = gameplay_font.render(cfg_item("fonts", "instructions", "config", "arrows"), True, cfg_item("fonts", "instructions", "config", "color"))
        self.__instructions_text = instructions_font.render(cfg_item("fonts", "instructions", "config", "instructions"), True, cfg_item("fonts", "instructions", "config", "color"))


    def __del__(self):
        pass

    def enter(self):
        self.done = False

    def exit(self):
        pass

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: 
            self.next_state = Intro.second_next_state
            self.done = True


    def handle_menu_click(self, pos):
        pass


    def handle_events(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self, screen):
        screen.fill([0,0,0])
        screen.blit(self.__melee_attack_text, cfg_item("fonts", "instructions", "config", "melee_attack_pos"))
        screen.blit(self.__arrows_text, cfg_item("fonts", "instructions", "config", "arrows_pos"))
        screen.blit(self.__instructions_text, cfg_item("fonts", "instructions", "config", "instructions_pos"))
