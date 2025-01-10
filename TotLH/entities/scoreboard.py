import os
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.entities.gameobject import GameObject


class Scoreboard(GameObject):
    def __init__(self):
        super().__init__()
        self.__score = 0

        with resources.path(cfg_item("fonts", "text", "path"), cfg_item("fonts", "text", "filename")) as instructions_path:
            self.__font = pygame.font.Font(instructions_path, cfg_item("scoreboard", "config", "text_size"))

    def handle_events(self, event):
        pass

    def handle_input(self, key, is_pressed):
        pass

    def update(self, delta_time):
        pass

    def render(self, screen):
        text = self.__font.render(str(self.__score), True, cfg_item("scoreboard", "config", "color"))  

        text_width, text_height = text.get_size()

        screen_width = screen.get_width()
        x = screen_width - text_width - cfg_item("scoreboard", "config", "text_separation_x")  
        y = cfg_item("scoreboard", "config", "text_separation_y") 

        background_width = text_width + cfg_item("scoreboard", "config", "text_separation_x") /2 
        background_height = text_height + cfg_item("scoreboard", "config", "text_separation_y") /2
        background_surface = pygame.Surface((background_width, background_height), pygame.SRCALPHA)
        background_surface.fill(cfg_item("scoreboard", "config", "background_surface_color")) 

        screen.blit(background_surface, (x - cfg_item("scoreboard", "config", "text_separation_x") /4 , y - cfg_item("scoreboard", "config", "text_separation_y") /4))  
        screen.blit(text, (x, y))
    
    def add_points(self, score):
        self.__score += score

