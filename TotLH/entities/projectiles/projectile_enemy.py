from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.entities.projectiles.projectile import Projectile


class Projectile_enemy(Projectile):

    __raw_image = None
    __image = None
    __image_half_width = None
    __image_half_height = None

    __damage = cfg_item("projectiles", "enemy", "stats", "damage")


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

        if Projectile_enemy.__image is None:
            with resources.path(cfg_item("projectiles","enemy", "image", "standard", "path"), cfg_item("projectiles","enemy", "image",  "standard", "filename")) as image_path:
                Projectile_enemy.__raw_image = pygame.image.load(image_path).convert_alpha()
                Projectile_enemy.__image = pygame.transform.scale(Projectile_enemy.__raw_image, cfg_item("projectiles","enemy", "image", "standard", "size")).convert_alpha()
                Projectile_enemy.__image_half_width = Projectile_enemy.__image.get_width()/2
                Projectile_enemy.__image_half_height = Projectile_enemy.__image.get_height()/2

        self.__centered_position = pygame.math.Vector2(position.x - Projectile_enemy.__image_half_width, position.y - Projectile_enemy.__image_half_height)

        super().__init__(self.__centered_position, velocity)


    def __del__(self):
        pass

    @property
    def image(self):
        return Projectile_enemy.__image
    
    @property
    def image_half_width(self):
        return Projectile_enemy.__image_half_width
    
    @property
    def image_half_height(self):
        return Projectile_enemy.__image_half_height

    @property
    def damage(self):
        return Projectile_enemy.__damage


