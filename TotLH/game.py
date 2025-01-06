from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.states.statemanager import StateManager


class Game:

    def __init__(self):
        pygame.init()

        self.__running = False

        self.__clock = pygame.time.Clock()

        self.__screen = pygame.display.set_mode(cfg_item("game","screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game","caption"))

        self.__state_manager = StateManager()

        with resources.path(cfg_item("scenario","bg_1", "path"), cfg_item("scenario", "bg_1", "filename")) as bg1_image_path:
            self.__background1=pygame.image.load(bg1_image_path).convert_alpha()
            self.__background1_resized = pygame.transform.scale(self.__background1, cfg_item("game", "screen_size")).convert_alpha()

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

            self.__state_manager.process_events(event)
    
    def __update(self, delta_time):
        self.__state_manager.update(delta_time)

    def __render(self):
        self.__screen.blit(self.__background1_resized,(0,0))
        self.__state_manager.render(self.__screen)
        pygame.display.update()
