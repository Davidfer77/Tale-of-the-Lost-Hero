from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.states.state import State
from TotLH.states.states import States

class GameOver(State):

    def __init__(self):
        super().__init__()
        self.next_state = States.Intro

        # Videogame name text
        with resources.path(cfg_item("fonts", "gameover", "path"), cfg_item("fonts", "gameover", "filename")) as name_path:
            name = pygame.font.Font(name_path, cfg_item("fonts", "gameover", "config", "gameover_size"))
        # Instructions text
        with resources.path(cfg_item("fonts", "gameover", "path"), cfg_item("fonts", "gameover", "filename")) as instructions_path:
            instructions = pygame.font.Font(instructions_path, cfg_item("fonts", "gameover", "config", "instructions_size"))

        # Intro image
        with resources.path(cfg_item("scenario", "gameover", "path"), cfg_item("scenario", "gameover", "filename")) as intro_image_path:
            intro_image=pygame.image.load(intro_image_path).convert_alpha()
            self.__intro_image_resized = pygame.transform.scale(intro_image, cfg_item("game", "screen_size")).convert_alpha()


        self.__name_text = name.render(cfg_item("fonts", "gameover", "config", "gameover"), True, cfg_item("fonts", "gameover", "config", "color"))
        self.__instructions_text = instructions.render(cfg_item("fonts", "gameover", "config", "instructions"), True, cfg_item("fonts", "gameover", "config", "color"))

    def __del__(self):
        pass

    def enter(self):
        self.done = False

    def exit(self):
        pass

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True

    def handle_events(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self, screen):
        screen.blit(self.__intro_image_resized,(0,0))
        screen.blit(self.__name_text, cfg_item("fonts", "gameover", "config", "gameover_pos"))
        screen.blit(self.__instructions_text, cfg_item("fonts", "gameover", "config", "instructions_pos"))