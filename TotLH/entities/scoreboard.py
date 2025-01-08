import os
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.entities.gameobject import GameObject


class Scoreboard(GameObject):
    def __init__(self):
        super().__init__()
        self.__score = 0

    def handle_events(self, event):
        pass

    def handle_input(self, key, is_pressed):
        pass

    def update(self, delta_time):
        pass

    def render(self, screen):
        font = pygame.font.Font(None, cfg_item("scoreboard", "config", "text_size"))  # Fuente por defecto con tamaño 36
        text = font.render(str(self.__score), True, cfg_item("scoreboard", "config", "color"))  # Texto blanco

        # Obtener el ancho y alto del texto
        text_width, text_height = text.get_size()

        # Calcular la posición para alinear a la derecha
        screen_width = screen.get_width()
        x = screen_width - text_width - cfg_item("scoreboard", "config", "text_separation_x")  # 20 px de margen derecho
        y = cfg_item("scoreboard", "config", "text_separation_y")  # 20 px desde la parte superior

        # Dibujar el texto en la pantalla
        screen.blit(text, (x, y))
    
    def add_points(self, score):
        self.__score += score

