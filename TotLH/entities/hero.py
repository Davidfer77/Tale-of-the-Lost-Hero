import os
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.events import Events
from TotLH.entities.gameobject import GameObject


class Hero(GameObject):
    def __init__(self):
        super().__init__()
        with resources.path(cfg_item("hero","image", "path"), cfg_item("hero", "image", "filename")) as image_path:
            self.__image = pygame.image.load(image_path).convert_alpha()
            self.__image_resized = pygame.transform.scale(self.__image, cfg_item("hero", "image", "size")).convert_alpha()
            self.__image_half_width = self.__image_resized.get_width()/2
            self.__image_half_height = self.__image_resized.get_height()/2
        
        screen_size = cfg_item("game","screen_size")

        self._pos = pygame.math.Vector2(screen_size[0] / 2 - self.__image_half_width, screen_size[1] / 2 - self.__image_half_height)

        self.__moving = {
            "left" : False,
            "right" : False,
            "up" : False,
            "down" : False
        }


        self.__arrow_cooldown = 0

        self.__last_direction = "up"

        self.__life = cfg_item("hero", "stats", "life")
        self.__damage = cfg_item("hero", "stats", "damage")
        self.__arrow_damage = cfg_item("projectiles", "allied", "stats", "damage")

    
    def __del__(self):
        pass

    def handle_input(self, key, is_pressed):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.__moving["left"] = is_pressed
            self.__last_direction = "left"
        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.__moving["right"] = is_pressed
            self.__last_direction = "right"
        if key == pygame.K_UP or key == pygame.K_w:
            self.__moving["up"] = is_pressed
            self.__last_direction = "up"
        if key == pygame.K_DOWN or key == pygame.K_s:
            self.__moving["down"] = is_pressed
            self.__last_direction = "down"
        if key == pygame.K_SPACE and self.__arrow_cooldown <= 0.0:
            self.__fire()

    def handle_events(self, event):
        pass

    def update(self, delta_time):
        speed=cfg_item("hero", "stats", "speed")

        movement=pygame.math.Vector2(0.0, 0.0)

        if self.__moving["left"] == True:
            movement.x -= speed
        if self.__moving["right"] == True:
            movement.x += speed
        if self.__moving["up"] == True:
            movement.y -= speed
        if self.__moving["down"] == True:
            movement.y += speed
        
        distance = movement * delta_time
        if self._in_bounds(distance):
            self._pos += distance
            move_event = pygame.event.Event(pygame.USEREVENT, event = Events.HERO_MOVES, hero_pos = self._pos)
            pygame.event.post(move_event)

        
        if self.__arrow_cooldown >= 0.0:
            self.__arrow_cooldown -= delta_time
        
        self._rect_sync()
    
    def render(self, screen):
        screen.blit(self.__image_resized, (self._pos.x, self._pos.y))

        
    def __fire(self):
        proj_pos = pygame.math.Vector2(self._pos.x + self.__image_half_width, self._pos.y + self.__image_half_height)
        
        if self.__moving["left"] == True:
            proj_pos.x -= self.__image_half_width
        elif self.__moving["right"] == True:
            proj_pos.x += self.__image_half_width
        elif self.__moving["up"] == True:
            proj_pos.y -= self.__image_half_height
        elif self.__moving["down"] == True:
            proj_pos.y += self.__image_half_height
        
   
        self.__arrow_cooldown = cfg_item("projectiles","allied", "stats", "cooldown")
    

        #Creamos el evento
        fire_event = pygame.event.Event(pygame.USEREVENT, event = Events.HERO_FIRES, pos = proj_pos, dir = self.__last_direction, dmg = self.__arrow_damage)
        #Lanzamos el evento a la cola
        pygame.event.post(fire_event)


    def take_damage(self, damage):
        self.__life -= damage

    @property
    def image(self):
        return self.__image_resized

    @property
    def damage(self):
        return self.__damage

    @property
    def life(self):
        return self.__life

    @life.setter
    def life(self, value):
        self.__life = value


