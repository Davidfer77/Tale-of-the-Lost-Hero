import os
import random
from importlib import resources
import pygame
from TotLH.states.state import State
from TotLH.states.states import States
from TotLH.entities.hero import Hero
from TotLH.entities.damagetext import DamageText
from TotLH.entities.pool import Pool
from TotLH.events import Events
from TotLH.config import cfg_item
from TotLH.entities.enemies.enemy import EnemyType, Enemy
from TotLH.entities.rendergroup import RenderGroup
from TotLH.entities.projectiles.projectile_factory import ProjectileFactory
from TotLH.entities.projectiles.projectile_type import ProjectileType
from TotLH.entities.projectiles.projectile_enemy import Projectile_enemy
from TotLH.entities.scoreboard import Scoreboard
from TotLH.entities.explosion import Explosion

class Scenario1(State):
    def __init__(self):
        super().__init__()
        self.__players = RenderGroup()
        self.__enemies = RenderGroup()
        self.__projectiles_allied = RenderGroup()
        self.__projectiles_enemy = RenderGroup()
        self.__enemy_pool = Pool(10, Enemy)
        self.__explosions = RenderGroup()

        self.__scorepoints = RenderGroup()
        self.__damagetext = RenderGroup()

        self.next_state = States.Scenario2

        self.__max_score = cfg_item("scenario", "scenario1", "maximum_score")

        self.__clock = pygame.time.Clock()

        with resources.path(cfg_item("scenario","scenario1", "path"), cfg_item("scenario", "scenario1", "filename")) as scenario1_image_path:
            self.__background1=pygame.image.load(scenario1_image_path).convert_alpha()
            self.__background1_resized = pygame.transform.scale(self.__background1, cfg_item("game", "screen_size")).convert_alpha()

        with resources.path(cfg_item("sounds", "arrow_impact", "path"), cfg_item("sounds", "arrow_impact", "filename")) as sound_path:
            self.__arrow_impact_sound = pygame.mixer.Sound(sound_path)
            self.__arrow_impact_sound.set_volume(cfg_item("sounds", "arrow_impact", "volume"))


    def enter(self):
        self.__players.add(Hero())
        self.__scorepoints.add(Scoreboard())
        self.done = False

    def exit(self):
        self.__players.empty()
        self.__enemies.empty()
        self.__projectiles_allied.empty()
        self.__projectiles_enemy.empty()
        self.__explosions.empty()
        self.__scorepoints.empty()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.__players.handle_input(event.key, True)
        elif event.type == pygame.KEYUP:
            self.__players.handle_input(event.key, False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for player, enemies in pygame.sprite.groupcollide(self.__players, self.__enemies, False, False).items():
                if player.attack_cooldown <= 0.0:
                    player.melee_attack()
                    for enemy in enemies:
                        self.__damagetext.add(DamageText(player.damage, enemy.position))
                        enemy.take_damage(player.damage)





    def handle_events(self, event):
        self.__handle_events(event)
 
        self.__players.handle_events(event)
        self.__projectiles_allied.handle_events(event)
        self.__enemies.handle_events(event)
        self.__projectiles_enemy.handle_events(event)
        self.__explosions.handle_events(event)

        self.__scorepoints.handle_events(event)
        self.__damagetext.handle_events(event)


    def update(self, delta_time):
        self.__spawn_enemy()
        self.__players.update(delta_time)
        self.__projectiles_allied.update(delta_time)
        self.__enemies.update(delta_time)
        self.__projectiles_enemy.update(delta_time)
        self.__explosions.update(delta_time)

        self.__detect_colissions()

        self.__scorepoints.update(delta_time)
        self.__damagetext.update(delta_time)


    def render(self, screen):
        screen.blit(self.__background1_resized,(0,0))

        self.__enemies.render(screen)
        self.__players.render(screen)
        self.__projectiles_allied.render(screen)
        self.__projectiles_enemy.render(screen)
        self.__explosions.render(screen)

        self.__scorepoints.render(screen)
        self.__damagetext.render(screen)


    def __handle_events(self, event):
        if event.event == Events.HERO_FIRES:
            self.__projectiles_allied.add(ProjectileFactory.create_projectile(ProjectileType.Allied, event.pos, event.dir, event.dmg))
        
        elif event.event == Events.PROJECTILE_OUT_OF_SCREEN:
            self.__projectiles_allied.remove(event.proj)
            self.__projectiles_enemy.remove(event.proj)

        elif event.event == Events.ENEMY_FIRES:
            self.__projectiles_enemy.add(ProjectileFactory.create_projectile(ProjectileType.Enemy, event.pos, event.dir, event.dmg))

        elif event.event == Events.EXPLOSION_ENDS:
            self.__explosions.remove(event.expl)  

        elif event.event == Events.HERO_MOVES:
            delta_time = self.__clock.tick(cfg_item("game","fps"))
            self.__enemies.move_towards_player(event.hero_pos, delta_time)    

        elif event.event == Events.ENEMY_SLAINED:
            self.__scorepoints.add_points(event.score)
            for scoreboard in self.__scorepoints:
                if scoreboard.score >= self.__max_score:
                    self.done = True
             

    def __spawn_enemy(self):
        if random.random() < cfg_item("scenario", "scenario1", "enemy_spawn_prob"):
            enemy_list = [EnemyType.Skeleton, EnemyType.Predator, EnemyType.Shadow, EnemyType.Devil]
            enemy_prob = [cfg_item("scenario", "scenario1", "enemy_spawn_weight", "skeleton"), cfg_item("scenario", "scenario1", "enemy_spawn_weight", "predator"), \
                          cfg_item("scenario", "scenario1", "enemy_spawn_weight", "shadow"), cfg_item("scenario", "scenario1", "enemy_spawn_weight", "devil")]
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
        self.next_state = States.GameOver
        self.done = True

    def __detect_colissions(self):
        for player, projectiles in pygame.sprite.groupcollide(self.__players, self.__projectiles_enemy, False, True).items():
            self.__spawn_explosion(player.half_size_pos)
            for projectile in projectiles:
                player.take_damage(projectile.damage)
                self.__damagetext.add(DamageText(projectile.damage, player.position))
                if player.life <= 0:
                    self.__game_over()

        for enemy, projectiles in pygame.sprite.groupcollide(self.__enemies, self.__projectiles_allied, False, True).items():
            self.__arrow_impact_sound.play()
            for projectile in projectiles:
                self.__damagetext.add(DamageText(projectile.damage, enemy.position))
                enemy.take_damage(projectile.damage)


        for player, enemies in pygame.sprite.groupcollide(self.__players, self.__enemies, False, False).items():
            for enemy in enemies:
                if enemy.attack_cooldown <= 0.0:
                    self.__damagetext.add(DamageText(enemy.damage, player.position))
                    player.take_damage(enemy.damage)
                    enemy.melee_attack()
                    if player.life <= 0:
                        self.__game_over()