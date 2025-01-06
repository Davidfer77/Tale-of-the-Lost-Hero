import pygame
from TotLH.states.intro import Intro
from TotLH.states.gameplay import GamePlay
from TotLH.states.states import States


class StateManager:

    def __init__(self):
        self.__states = {
            States.Intro : Intro(),
            States.GamePlay : GamePlay()
        }

        self.__current_state_name = States.Intro
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.enter()
    
    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            self.__current_state.handle_events(event)
        
        else:
            self.__current_state.handle_input(event)
    
    def update(self, delta_time):
        if self.__current_state.done:
            self.__change_state()

        self.__current_state.update(delta_time)

    def render(self, screen):
        self.__current_state.render(screen)

    def __change_state(self):
        self.__current_state.exit()

        self.__current_state_name = self.__current_state.next_state
        self.__current_state = self.__states[self.__current_state_name]

        self.__current_state.enter()