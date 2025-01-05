import pygame
from TotLH.events import Events
from TotLH.entities.gameobject import GameObject

class Projectile(GameObject):

    def __init__(self, position, velocity):
        super().__init__()
        self._pos = position
        self.__velocity = velocity

    def __del__(self):
        pass

    def handle_input(self, key, is_pressed):
        pass

    def handle_events(self, event):
        pass

    def update(self, delta_time):
        distance = self.__velocity * delta_time

        if self._in_bounds(distance):
            self._pos += distance
        else:
            #Creamos el evento de salida de pantalla y da como parametro la propia instancia (self) para luego borrar esa instancia
            out_of_screen_event = pygame.event.Event(pygame.USEREVENT, event = Events.PROJECTILE_OUT_OF_SCREEN, proj = self)
            #Lanzamos el evento a la cola
            pygame.event.post(out_of_screen_event)

    def render(self, screen):
        screen.blit(self.image, (self._pos.x-self.image_half_width, self._pos.y-self.image_half_height))