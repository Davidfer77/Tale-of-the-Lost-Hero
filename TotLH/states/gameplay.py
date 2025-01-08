import os
import random
from importlib import resources
import pygame
from TotLH.states.state import State
from TotLH.states.states import States
from TotLH.entities.hero import Hero
from TotLH.entities.pool import Pool
from TotLH.events import Events
from TotLH.config import cfg_item
from TotLH.entities.enemies.enemy import EnemyType, Enemy
from TotLH.entities.rendergroup import RenderGroup
from TotLH.entities.projectiles.projectile_factory import ProjectileFactory
from TotLH.entities.projectiles.projectile_type import ProjectileType
from TotLH.entities.projectiles.projectile_enemy import Projectile_enemy
from TotLH.entities.explosion import Explosion

class GamePlay(State):
    def __init__(self):
        super().__init__()
        self.__players = RenderGroup()
        self.__enemies = RenderGroup()
        self.__projectiles_allied = RenderGroup()
        self.__projectiles_enemy = RenderGroup()
        self.__enemy_pool = Pool(10, Enemy)
        self.__explosions = RenderGroup()

        self.next_state = States.GameOver

        self.__clock = pygame.time.Clock()
    
    def enter(self):
        self.__players.add(Hero())
        self.done = False

    def exit(self):
        self.__players.empty()
        self.__enemies.empty()
        self.__projectiles_allied.empty()
        self.__projectiles_enemy.empty()
        self.__explosions.empty()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.__players.handle_input(event.key, True)
        elif event.type == pygame.KEYUP:
            self.__players.handle_input(event.key, False)

        elif event.type == pygame.MOUSEBUTTONDOWN: #GESTIONADO CON EL CLICK DEL RATON
            self.__explosions.add(Explosion(event.pos))


    def handle_events(self, event):
        self.__handle_events(event) # Mandamos el evento a la funcion que los gestionara (handle_events)
 
        self.__players.handle_events(event)
        self.__projectiles_allied.handle_events(event)
        self.__enemies.handle_events(event)
        self.__projectiles_enemy.handle_events(event)
        self.__explosions.handle_events(event)

    def update(self, delta_time):
        self.__spawn_enemy()
        self.__players.update(delta_time)
        self.__projectiles_allied.update(delta_time)
        self.__enemies.update(delta_time)
        self.__projectiles_enemy.update(delta_time)
        self.__explosions.update(delta_time)

        self.__detect_colissions()


    def render(self, screen):
        self.__players.render(screen)
        self.__projectiles_allied.render(screen)
        self.__enemies.render(screen)
        self.__projectiles_enemy.render(screen)
        self.__explosions.render(screen)


    def __handle_events(self, event): # Gestionamos la reaccion a cada evento
        if event.event == Events.HERO_FIRES:
            self.__projectiles_allied.add(ProjectileFactory.create_projectile(ProjectileType.Allied, event.pos, event.dir, event.dmg))
        
        elif event.event == Events.PROJECTILE_OUT_OF_SCREEN:
            self.__projectiles_allied.remove(event.proj)
            self.__projectiles_enemy.remove(event.proj)

        elif event.event == Events.ENEMY_OUT_OF_SCREEN:
            self.__enemy_pool.release(event.enemy)
            self.__enemies.remove(event.enemy)

        elif event.event == Events.ENEMY_FIRES:
            self.__projectiles_enemy.add(ProjectileFactory.create_projectile(ProjectileType.Enemy, event.pos, event.dir, event.dmg))

        elif event.event == Events.EXPLOSION_ENDS:
            self.__explosions.remove(event.expl)  

        elif event.event == Events.HERO_MOVES:
            delta_time = self.__clock.tick(cfg_item("game","fps"))
            self.__enemies.move_towards_player(event.hero_pos, delta_time)      
             

    def __spawn_enemy(self):
        if random.random() < cfg_item("scenario", "bg_1", "enemy_spawn_prob"):
            enemy_list = [EnemyType.Skeleton, EnemyType.Predator, EnemyType.Shadow, EnemyType.Devil]
            enemy_prob = [cfg_item("scenario", "bg_1", "enemy_spawn_weight", "skeleton"), cfg_item("scenario", "bg_1", "enemy_spawn_weight", "predator"), \
                          cfg_item("scenario", "bg_1", "enemy_spawn_weight", "shadow"), cfg_item("scenario", "bg_1", "enemy_spawn_weight", "devil")]
            enemy_type = random.choices(enemy_list, enemy_prob, k=1)[0]

            padding_x = max(cfg_item("enemy", "skeleton", "image", "size")[0], cfg_item("enemy", "predator", "image", "size")[0],\
                           cfg_item("enemy", "shadow", "image", "size")[0], cfg_item("enemy", "devil", "image", "size")[0])

            x = random.randint(0, cfg_item("game", "screen_size")[0] - padding_x)

            padding_y= max(cfg_item("enemy", "skeleton", "image", "size")[1], cfg_item("enemy", "predator", "image", "size")[1],\
                           cfg_item("enemy", "shadow", "image", "size")[1], cfg_item("enemy", "devil", "image", "size")[1])
            
            spawn_pos = pygame.math.Vector2(x, -padding_y)

            enemy = self.__enemy_pool.acquire()

            enemy.init(enemy_type, spawn_pos)

            self.__enemies.add(enemy)
    
    def __spawn_explosion(self, position):
        self.__explosions.add(Explosion(position))

    def __game_over(self):
        self.done = True

    def __detect_colissions(self):
        for player in pygame.sprite.groupcollide(self.__players, self.__projectiles_enemy, False, True).keys():
            self.__spawn_explosion(player.half_size_pos)
            for player in self.__players:
                player.life -= 30
                if player.life <= 0:
                    self.__game_over()

        for enemy, projectiles in pygame.sprite.groupcollide(self.__enemies, self.__projectiles_allied, False, True).items():
            self.__spawn_explosion(enemy.half_size_pos)
            for projectile in projectiles:
                enemy.take_damage(30)


        for player, enemies in pygame.sprite.groupcollide(self.__players, self.__enemies, True, True).items():
            self.__spawn_explosion(player.half_size_pos)

            for enemy in enemies:
                self.__spawn_explosion(enemy.half_size_pos)
            
            self.__game_over()

