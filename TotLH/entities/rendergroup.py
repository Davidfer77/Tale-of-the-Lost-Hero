import pygame


class RenderGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()


    def handle_input(self, key, is_pressed):
        for sprite in self.sprites():
            sprite.handle_input(key, is_pressed)


    def handle_events(self, event):
        for sprite in self.sprites():
            sprite.handle_events(event)


    def render(self, screen):
        for sprite in self.sprites():
            sprite.render(screen)
