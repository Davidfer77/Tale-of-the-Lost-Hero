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

        self._pos = pygame.math.Vector2(screen_size[0] / 2 - self.__image_half_width, screen_size[1] - self.__image_half_height * 2)

        self.__moving = {
            "left" : False,
            "right" : False,
            "up" : False,
            "down" : False
        }

        with resources.path(cfg_item("fonts", "text", "path"), cfg_item("fonts", "text", "filename")) as instructions_path:
            self.__font = pygame.font.Font(instructions_path, cfg_item("life_bar", "config", "text_size"))

        self.__arrow_cooldown = 0
        self.__attack_cooldown = 0

        self.__last_direction = "up"

        self.__life = cfg_item("hero", "stats", "life")
        self.__max_health = cfg_item("hero", "stats", "life")
        self.__damage = cfg_item("hero", "stats", "damage")
        self.__arrow_damage = cfg_item("projectiles", "allied", "stats", "damage")


        with resources.path(cfg_item("sounds", "sword_attack", "path"), cfg_item("sounds", "sword_attack", "filename")) as sound_path:
            self.__sword_attack_sound = pygame.mixer.Sound(sound_path)
            self.__sword_attack_sound.set_volume(cfg_item("sounds", "sword_attack", "volume"))

        with resources.path(cfg_item("sounds", "arrow_shot", "path"), cfg_item("sounds", "arrow_shot", "filename")) as sound_path:
            self.__arrow_shot_sound = pygame.mixer.Sound(sound_path)
            self.__arrow_shot_sound.set_volume(cfg_item("sounds", "arrow_shot", "volume"))

    
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
        if self._in_bounds(distance, self.__image_half_width*2, self.__image_half_height*2):
            self._pos += distance
            move_event = pygame.event.Event(pygame.USEREVENT, event = Events.HERO_MOVES, hero_pos = self._pos)
            pygame.event.post(move_event)

        
        if self.__arrow_cooldown >= 0.0:
            self.__arrow_cooldown -= delta_time

        if self.__attack_cooldown >= 0.0:
            self.__attack_cooldown -= delta_time
        
        self._rect_sync()
    
    def render(self, screen):
        screen.blit(self.__image_resized, (self._pos.x, self._pos.y))
        self.draw_player_health_bar(screen)
        
    def __fire(self):
        self.__arrow_shot_sound.play()
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
    

        fire_event = pygame.event.Event(pygame.USEREVENT, event = Events.HERO_FIRES, pos = proj_pos, dir = self.__last_direction, dmg = self.__arrow_damage)
        pygame.event.post(fire_event)


    def take_damage(self, damage):
        self.__life -= damage


    def melee_attack(self):
        self.__sword_attack_sound.play()
        self.__attack_cooldown = cfg_item("hero", "stats", "cooldown")


    def draw_player_health_bar(self, screen):
        bar_width = cfg_item("life_bar", "config", "bar_width")
        bar_height = cfg_item("life_bar", "config", "bar_height")
        bar_x = cfg_item("life_bar", "config", "bar_x")
        bar_y = cfg_item("life_bar", "config", "bar_y")

        health_ratio = self.__life / self.__max_health

        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), cfg_item("life_bar", "config", "rect_edge"))

        text = self.__font.render(f"{self.__life}/{self.__max_health}", True, (255, 255, 255))
        screen.blit(text, (bar_x + bar_width + cfg_item("life_bar", "config", "text_separation"), bar_y)) 



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

    @property
    def attack_cooldown(self):
        return self.__attack_cooldown

