import sys
from importlib import resources
import pygame
from TotLH.config import cfg_item
from TotLH.states.state import State
from TotLH.states.states import States

class Intro(State):

    def __init__(self):
        super().__init__()
        self.next_state = States.GamePlay

        # Videogame name text
        with resources.path(cfg_item("fonts", "title", "path"), cfg_item("fonts", "title", "filename")) as name_path:
            name = pygame.font.Font(name_path, cfg_item("fonts", "title", "config", "name_size"))
        # Instructions text
        with resources.path(cfg_item("fonts", "text", "path"), cfg_item("fonts", "text", "filename")) as instructions_path:
            self.font = pygame.font.Font(instructions_path, cfg_item("scenario" , "intro", "buttons", "font", "size"))

        # Intro image
        with resources.path(cfg_item("scenario","intro", "path"), cfg_item("scenario", "intro", "filename")) as intro_image_path:
            intro_image=pygame.image.load(intro_image_path).convert_alpha()
            self.__intro_image_resized = pygame.transform.scale(intro_image, cfg_item("game", "screen_size")).convert_alpha()


        self.__name_text = name.render(cfg_item("fonts", "title", "config", "name"), True, cfg_item("fonts", "title", "config", "color"))


        self.__buttons = [
            {"text": cfg_item("scenario" , "intro", "buttons", "story_mode", "text"), "color": cfg_item("scenario" , "intro", "buttons", "story_mode", "color"), "rect": pygame.Rect(cfg_item("scenario" , "intro", "buttons", "story_mode", "rectangle")), "action": "story_mode"},
            {"text": cfg_item("scenario" , "intro", "buttons", "survival_mode", "text"), "color": cfg_item("scenario" , "intro", "buttons", "survival_mode", "color"), "rect": pygame.Rect(cfg_item("scenario" , "intro", "buttons", "survival_mode", "rectangle")), "action": "survival_mode"},
            {"text": cfg_item("scenario" , "intro", "buttons", "exit", "text"), "color": cfg_item("scenario" , "intro", "buttons", "exit", "color"), "rect": pygame.Rect(cfg_item("scenario" , "intro", "buttons", "exit", "rectangle")), "action": "exit"}
        ]


    def __del__(self):
        pass

    def enter(self):
        self.done = False

    def exit(self):
        pass

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            action = self.handle_menu_click(event.pos)
            if action == "story_mode":
                pass # Soon available
            elif action == "survival_mode":
                self.done = True
            elif action == "exit":
                pygame.quit()
                sys.exit()


    def handle_menu_click(self, pos):
        for button in self.__buttons:
            if button["rect"].collidepoint(pos):
                return button["action"]
        return None


    def handle_events(self, event):
        pass

    def update(self, delta_time):
        pass

    def render(self, screen):
        screen.blit(self.__intro_image_resized,(0,0))
        screen.blit(self.__name_text, cfg_item("fonts", "title", "config", "name_pos"))

        for button in self.__buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            text_surface = self.font.render(button["text"], True, cfg_item("scenario" , "intro", "buttons", "text_color"))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            screen.blit(text_surface, text_rect)
