from importlib import resources
import pygame
from TotLH.assets.flipbook import FlipBook
from TotLH.entities.gameobject import GameObject
from TotLH.events import Events
from TotLH.config import cfg_item

class Explosion(GameObject):

    def __init__(self, position):
        super().__init__()
        self._pos = pygame.math.Vector2(position)
        rows = cfg_item("projectiles", "enemy", "image", "explosion", "rows")
        cols = cfg_item("projectiles", "enemy", "image", "explosion", "cols")

        with resources.path(cfg_item("projectiles", "enemy", "image", "explosion", "path"), cfg_item("projectiles", "enemy", "image", "explosion", "filename")) as image_path:
            self.__flipbook = FlipBook(image_path, rows, cols)
        
        self.__current_sequence = 0
        self.__current_time = 0
        self.__time_per_sequence = cfg_item("projectiles", "enemy", "image", "explosion", "time_sequence")
        self.__total_sequences = rows * cols

    def handle_input(self, key, is_pressed):
        pass

    def handle_events(self, event):
        pass

    def update(self, delta_time):
        self.__current_time += delta_time
        if self.__current_time >= self.__time_per_sequence:
            self.__current_time -= self.__time_per_sequence
            self.__current_sequence +=1
            if self.__current_sequence >= self.__total_sequences -1:
                end_event = pygame.event.Event(pygame.USEREVENT, event = Events.EXPLOSION_ENDS, expl = self)
                pygame.event.post(end_event)

    def render(self, screen):
        self.__flipbook.render(screen, self._pos, self.__current_sequence)
 