from enum import Enum

class Events(Enum):
    HERO_FIRES = 0, # parameter pos = position of the projectile to spawn and dir = direction of the projectile
    PROJECTILE_OUT_OF_SCREEN = 1, # parameter instance of the projectile
    ENEMY_OUT_OF_SCREEN = 2, # parameter enemy = instance of the enemy
    ENEMY_FIRES = 3, # parameter pos = position of the projectile in the spawn
    EXPLOSION_ENDS = 4, # parameter expl = instance of the explosion
    HERO_MOVES = 5, # parameter hero_pos = position of the player
    ENEMY_SLAINED = 6, # parameter score = enemy scorepoints

