from enum import Enum
import random
from importlib import resources
import pygame
from TotLH.entities.gameobject import GameObject
from TotLH.entities.reusableobject import ReusableObject
from TotLH.config import cfg_item
from TotLH.events import Events


class EnemyType(Enum):
    Skeleton = 0,
    Predator = 1,
    Shadow = 2,
    Devil = 3

class Enemy(GameObject, ReusableObject):

    __skeleton_image = None
    __predator_image = None
    __shadow_image = None
    __devil_image = None

    def __init__(self):
        super().__init__()
        Enemy.__skeleton_image = self.__load_image(Enemy.__skeleton_image, "skeleton")
        Enemy.__predator_image = self.__load_image(Enemy.__predator_image, "predator")
        Enemy.__shadow_image = self.__load_image(Enemy.__shadow_image, "shadow")
        Enemy.__devil_image = self.__load_image(Enemy.__devil_image, "devil")

        self.__fire_cooldown = 0

        self.__moving = {
            "left" : False,
            "right" : False,
            "up" : False,
            "down" : False
        }

        self.__last_movement = "down"

        self.__direction = pygame.math.Vector2(0.0, 0.0)

    def __load_image(self, image, enemy_str):
        if image is None:
            with resources.path(cfg_item("enemy",enemy_str, "image", "path"), cfg_item("enemy",enemy_str, "image", "filename")) as image_path:
                __raw_image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(__raw_image, cfg_item("enemy",enemy_str, "image", "size")).convert_alpha()
                return image
        return image


    def __load_data(self, enemy_str): 
        self.__speed = cfg_item("enemy", enemy_str, "stats", "speed")
        self.__life = cfg_item("enemy", enemy_str, "stats", "life")
        self.__damage = cfg_item("enemy", enemy_str, "stats", "damage")
        self.__fire_rate = cfg_item("enemy", enemy_str, "stats", "fire_rate")

    def reset(self):
        self.__enemy_type = None
        self._pos = pygame.math.Vector2(0.0, 0.0)

    def init(self, enemy_type, spawn_point):
        self.__enemy_type = enemy_type
        self._pos = spawn_point

        if enemy_type == EnemyType.Skeleton:
            self.__load_data("skeleton")
            self.__image = Enemy.__skeleton_image
        elif enemy_type == EnemyType.Predator:
            self.__load_data("predator")
            self.__image = Enemy.__predator_image
        elif enemy_type == EnemyType.Shadow:
            self.__load_data("shadow")
            self.__image = Enemy.__shadow_image
        elif enemy_type == EnemyType.Devil:
            self.__load_data("devil")
            self.__image = Enemy.__devil_image

    def handle_input(self, key, is_pressed):
        pass

    def handle_events(self, event):
        pass

    def update(self, delta_time):
        if self._pos.y > cfg_item("game", "screen_size")[1]:
            out_of_screen_event = pygame.event.Event(pygame.USEREVENT, event = Events.ENEMY_OUT_OF_SCREEN, enemy = self)
            pygame.event.post(out_of_screen_event)
        
        self.__fire()

        if self.__fire_cooldown >= 0.0:
            self.__fire_cooldown -= delta_time
        
        self._rect_sync()

        #self.__fire()

    def render(self, screen):
        screen.blit(self.__image, self._pos)

    #def __fire(self):
    #    if random.random() < self.__fire_Rate:
    #    proj_pos = pygame.math.Vector2(self._pos.x + self.__image_half_width, self._pos.y + self.__image_half_height)
        
    #    if self.__moving["left"] == True:
    #        proj_pos.x -= self.__image_half_width
    #    elif self.__moving["right"] == True:
    #        proj_pos.x += self.__image_half_width
    #    elif self.__moving["up"] == True:
    #        proj_pos.y -= self.__image_half_height
    #    elif self.__moving["down"] == True:
    #        proj_pos.y += self.__image_half_height
        
   
    #    self.__arrow_cooldown = cfg_item("projectiles","allied", "stats", "cooldown")
    

        #Creamos el evento
    #    fire_event = pygame.event.Event(pygame.USEREVENT, event = Events.HERO_FIRES, pos = proj_pos)
        #Lanzamos el evento a la cola
    #    pygame.event.post(fire_event)

    def __fire(self):
        if random.random() <= self.__fire_rate and self.__fire_cooldown <= 0.0:
            #proj_pos = pygame.math.Vector2(self._pos.x + self.__image_half_width, self._pos.y + self.__image_half_height)
            proj_pos = pygame.math.Vector2(self._pos.x , self._pos.y)
    
            self.__fire_cooldown = cfg_item("projectiles","enemy", "stats", "cooldown")

            if abs(self.__direction.x) > abs(self.__direction.y):
                # Disparar horizontalmente
                #direction = Vector2(self.__direction.x, 0).normalize()
                if self.__direction.x > 0:
                    self.__last_movement = "right"
                else:
                    self.__last_movement = "left"
            else:
                # Disparar verticalmente
                #direction = Vector2(0, direction.y).normalize()
                if self.__direction.y > 0:
                    self.__last_movement = "down"
                else:
                    self.__last_movement = "up"

            #Creamos el evento
            fire_event = pygame.event.Event(pygame.USEREVENT, event = Events.ENEMY_FIRES, pos = proj_pos, dir = self.__last_movement)
            #Lanzamos el evento a la cola
            pygame.event.post(fire_event)
    

    @property
    def image(self):
        return self.__image

    def move_towards_player(self, hero_pos, delta_time):
        direction = hero_pos - self._pos
        if direction.length() != 0:
            self.__direction = direction.normalize()

        self._pos += self.__direction * self.__speed * delta_time