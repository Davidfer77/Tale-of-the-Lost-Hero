from abc import ABC, abstractmethod
import pygame
from TotLH.config import cfg_item

class GameObject(pygame.sprite.Sprite, ABC):

    def __init__(self):
        super().__init__()
        self._pos = pygame.math.Vector2(0.0, 0.0)

    @abstractmethod
    def handle_input(self, key, is_pressed):
        pass

    @abstractmethod
    def handle_events(self, event):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def render(self, screen):
        pass

    def _in_bounds(self, distance):
        new_pos = self._pos + distance

        return new_pos.x >= 0 and new_pos.x <= cfg_item("game", "screen_size")[0] \
              and new_pos.y >=0 and new_pos.y <= cfg_item("game", "screen_size")[1]