import pygame
from TotLH.states.intro import Intro
from TotLH.states.gameplay import GamePlay
from TotLH.states.instructions import Instructions
from TotLH.states.scenario1 import Scenario1
from TotLH.states.scenario2 import Scenario2
from TotLH.states.scenario3 import Scenario3
from TotLH.states.gameover import GameOver
from TotLH.states.congratulations import Congratulations
from TotLH.states.states import States


class StateManager:

    def __init__(self):
        self.__states = {
            States.Intro : Intro(),
            States.Instructions : Instructions(),
            States.GamePlay : GamePlay(),
            States.Scenario1 : Scenario1(),
            States.Scenario2 : Scenario2(),
            States.Scenario3 : Scenario3(),
            States.GameOver : GameOver(),
            States.Congratulations : Congratulations()
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