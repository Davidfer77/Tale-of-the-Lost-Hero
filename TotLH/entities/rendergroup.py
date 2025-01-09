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

    def move_towards_player(self, hero_pos, delta_time):
        for sprite in self.sprites():
            sprite.move_towards_player(hero_pos, delta_time)

    def add_points(self, score):
        for sprite in self.sprites():
            sprite.add_points(score)

    def melee_attack(self):
        for sprite in self.sprites():
            sprite.melee_attack()

    def take_damage(self, damage):
        for sprite in self.sprites():
            sprite.take_damage(damage)