from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.entities.projectiles.projectile import Projectile


class Projectile_allied(Projectile):

    __raw_image = None
    __image_up = None
    __image_left = None
    __image_down = None
    __image_right = None
    __image_half_width = None
    __image_half_height = None

    __damage = cfg_item("projectiles", "allied", "stats", "damage")


    def __init__(self, position, direction):
        self.__direction = direction
        velocity = pygame.math.Vector2(0.0, 0.0)
        if self.__direction == "left":
            velocity = pygame.math.Vector2(-cfg_item("projectiles", "allied", "stats", "speed"), 0.0)
        elif self.__direction == "right":
            velocity = pygame.math.Vector2(cfg_item("projectiles", "allied", "stats", "speed"), 0.0)
        elif self.__direction == "up":
            velocity = pygame.math.Vector2(0.0, -cfg_item("projectiles", "allied", "stats", "speed"))
        elif self.__direction == "down":
            velocity = pygame.math.Vector2(0.0, cfg_item("projectiles", "allied", "stats", "speed"))

        super().__init__(position, velocity)

        if Projectile_allied.__image_up is None:
            with resources.path(cfg_item("projectiles","allied", "image", "path"), cfg_item("projectiles","allied", "image", "filename")) as image_path:
                Projectile_allied.__raw_image_up = pygame.image.load(image_path).convert_alpha()
                Projectile_allied.__raw_image_left = pygame.transform.rotate(Projectile_allied.__raw_image_up, 90)
                Projectile_allied.__raw_image_down = pygame.transform.rotate(Projectile_allied.__raw_image_up, 180)
                Projectile_allied.__raw_image_right = pygame.transform.rotate(Projectile_allied.__raw_image_up, 270)
                Projectile_allied.__image_up = pygame.transform.scale(Projectile_allied.__raw_image_up, cfg_item("projectiles","allied", "image", "size")).convert_alpha()
                Projectile_allied.__image_left = pygame.transform.scale(Projectile_allied.__raw_image_left, cfg_item("projectiles","allied", "image", "lateral_size")).convert_alpha()
                Projectile_allied.__image_down = pygame.transform.scale(Projectile_allied.__raw_image_down, cfg_item("projectiles","allied", "image", "size")).convert_alpha()
                Projectile_allied.__image_right = pygame.transform.scale(Projectile_allied.__raw_image_right, cfg_item("projectiles","allied", "image", "lateral_size")).convert_alpha()
                Projectile_allied.__image_half_width = Projectile_allied.__image_up.get_width()/2
                Projectile_allied.__image_half_height = Projectile_allied.__image_up.get_height()/2


    def __del__(self):
        pass

    @property
    def image(self):
        if self.__direction == "left":
            return Projectile_allied.__image_left
        if self.__direction == "right":
            return Projectile_allied.__image_right
        if self.__direction == "up":
            return Projectile_allied.__image_up
        if self.__direction == "down":
            return Projectile_allied.__image_down
    
    @property
    def image_half_width(self):
        return Projectile_allied.__image_half_width
    
    @property
    def image_half_height(self):
        return Projectile_allied.__image_half_height


