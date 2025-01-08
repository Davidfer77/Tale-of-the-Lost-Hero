from TotLH.entities.projectiles.projectile_allied import Projectile_allied
from TotLH.entities.projectiles.projectile_enemy import Projectile_enemy
from TotLH.entities.projectiles.projectile_type import ProjectileType


class ProjectileFactory:
    @staticmethod
    def create_projectile(projectile_type, position, direction):
        if projectile_type == ProjectileType.Allied:
            return Projectile_allied(position, direction)
        elif projectile_type == ProjectileType.Enemy:
            return Projectile_enemy(position, direction)