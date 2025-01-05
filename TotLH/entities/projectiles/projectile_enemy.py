from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.entities.projectiles.projectile import Projectile


class Projectile_enemy(Projectile):

    __raw_image = None
    __image = None
    __image_half_width = None
    __image_half_height = None


    def __init__(self, position):
        velocity = pygame.math.Vector2(cfg_item("projectiles", "enemy", "stats", "velocity"))
        super().__init__(position, velocity)

        if Projectile_enemy.__image is None:
            with resources.path(cfg_item("projectiles","enemy", "image", "path"), cfg_item("projectiles","enemy", "image", "filename")) as image_path:
                Projectile_enemy.__raw_image = pygame.image.load(image_path).convert_alpha()
                Projectile_enemy.__image = pygame.transform.scale(Projectile_enemy.__raw_image, cfg_item("projectiles","enemy", "image", "size")).convert_alpha()
                Projectile_enemy.__image_half_width = Projectile_enemy.__image.get_width()/2
                Projectile_enemy.__image_half_height = Projectile_enemy.__image.get_height()/2


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


