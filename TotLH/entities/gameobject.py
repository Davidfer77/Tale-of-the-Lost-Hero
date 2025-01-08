from abc import ABC, abstractmethod
import pygame
from TotLH.config import cfg_item

class GameObject(pygame.sprite.Sprite, ABC):

    def __init__(self):
        super().__init__()
        self._pos = pygame.math.Vector2(0.0, 0.0)
        self.rect = pygame.Rect(0, 0, 0, 0)

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

    def _in_bounds(self, distance, width, height):
        new_pos = self._pos + distance

        return new_pos.x >= 0 and new_pos.x <= cfg_item("game", "screen_size")[0] - width \
              and new_pos.y >=0 and new_pos.y <= cfg_item("game", "screen_size")[1] - height

    def _rect_sync(self):
        self.rect.x = self._pos.x
        self.rect.y = self._pos.y
        width, height = self.image_size
        self.rect.width = width
        self.rect.height = height

    @property
    def position(self):
        return self._pos
    
    @property
    def image_size(self):
        return self.image.get_width(), self.image.get_height()

    @property
    def half_size_pos(self):
        pos = pygame.math.Vector2(self._pos.x + self.image.get_width() / 2, self._pos.y + self.image.get_height() / 2)
        return pos