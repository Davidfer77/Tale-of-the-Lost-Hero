import os
import random
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.events import Events
from TotLH.entities.hero import Hero
from TotLH.entities.projectiles.projectile_allied import Projectile_allied
from TotLH.entities.rendergroup import RenderGroup
from TotLH.entities.enemies.enemy import EnemyType, Enemy
from TotLH.entities.pool import Pool


class Game:

    def __init__(self):
        pygame.init()

        self.__running = False

        self.__clock = pygame.time.Clock()

        self.__screen = pygame.display.set_mode(cfg_item("game","screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game","caption"))

        with resources.path(cfg_item("scenario","bg_1", "path"), cfg_item("scenario", "bg_1", "filename")) as bg1_image_path:
            self.__background1=pygame.image.load(bg1_image_path).convert_alpha()
            self.__background1_resized = pygame.transform.scale(self.__background1, cfg_item("game", "screen_size")).convert_alpha()

        # Creamos los grupos para enemigos, proyectiles aliadps, proj enemigos...
        self.__players = RenderGroup()
        self.__enemies = RenderGroup()
        self.__projectiles_allied = RenderGroup()


        # A esos grupos le añadimos las instancias
        self.__players.add(Hero())


        self.__enemy_pool = Pool(10, Enemy)


    def __del__(self):
        pygame.quit()
    

    def run(self):
        self.__running = True
        while self.__running:
            delta_time = self.__clock.tick(cfg_item("game","fps"))
            self.__process_events()
            self.__update(delta_time)
            self.__render()


    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                self.__players.handle_input(event.key, True)
                #last_movement_event = pygame.event.Event(pygame.USEREVENT, event = Events.LAST_HERO_MOVEMENT, dir = direction)
                #pygame.event.post(last_movement_event)

            elif event.type == pygame.KEYUP:
                self.__players.handle_input(event.key, False)
            
            # Enviamos la comunicacion de cada evento a todos los objetos del juego
            elif event.type == pygame.USEREVENT:
                self.__handle_events(event) # Mandamos el evento a la funcion que los gestionara (handle_events)
                self.__players.handle_events(event)
                self.__projectiles_allied.handle_events(event)
                self.__enemies.handle_events(event)

    
    def __handle_events(self, event): # Gestionamos la reaccion a cada evento
        if event.event == Events.HERO_FIRES:
            self.__projectiles_allied.add(Projectile_allied(event.pos, event.dir))
        
        elif event.event == Events.PROJECTILE_OUT_OF_SCREEN:
            self.__projectiles_allied.remove(event.proj)
 
        elif event.event == Events.ENEMY_OUT_OF_SCREEN:
            self.__enemy_pool.release(event.enemy)
            self.__enemies.remove(event.enemy)
        

    
    def __update(self, delta_time):
            self.__spawn_enemy()
            self.__players.update(delta_time)
            self.__projectiles_allied.update(delta_time)
            self.__enemies.update(delta_time)


    def __render(self):
        self.__screen.blit(self.__background1_resized,(0,0))
        self.__players.render(self.__screen)
        self.__projectiles_allied.render(self.__screen)
        self.__enemies.render(self.__screen)

        pygame.display.update()
    

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





