import os
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.entities.gameobject import GameObject


class DamageText(GameObject):

    def __init__(self, text, pos, color=cfg_item("damagetext", "color"), duration=cfg_item("damagetext", "duration"), move_speed=cfg_item("damagetext", "move_speed")):
        super().__init__()
        self.__font = pygame.font.SysFont(None, cfg_item("damagetext", "size"))
        self.__text = str(text)
        self.__color = color
        self.__image = self.__font.render(self.__text, True, self.__color)
        self.__position = pos
        self.__rect = self.__image.get_rect(center=pos)
        self.__duration = duration
        self.__max_duration = duration
        self.__move_speed = move_speed
        self.__alpha = 255

    def update(self, delta_time):
        self.__rect.y -= self.__move_speed * delta_time

        self.__duration -= delta_time

        self.__alpha = max(255 - int(255 * ((self.__max_duration - self.__duration) / self.__max_duration)), 0)
        self.__image.set_alpha(self.__alpha)

        if self.__duration <= 0:
            self.kill()

    def handle_input(self, key, is_pressed):
        pass

    def handle_events(self, event):
        pass


    def render(self, screen):
        screen.blit(self.__image, self.__position)
