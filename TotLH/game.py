from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.states.statemanager import StateManager


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 16)


        with resources.path(cfg_item("sounds", "background", "path"), cfg_item("sounds", "background", "filename")) as sound_path:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.set_volume(cfg_item("sounds", "background", "volume"))
            pygame.mixer.music.play(-1)

        self.__running = False

        self.__clock = pygame.time.Clock()

        self.__screen = pygame.display.set_mode(cfg_item("game","screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game","caption"))

        self.__state_manager = StateManager()
        

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
        self.__state_manager.render(self.__screen)
        pygame.display.update()
