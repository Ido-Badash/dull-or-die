import pygame


from game.core import BaseState, logger
from game.ui import Colors
from .states import States


class GamePlay(BaseState):
    def __init__(self, game=None):
        super().__init__(States.GAMEPLAY, game)

    def startup(self):
        pygame.display.set_caption("NEW GAME")

    def cleanup(self):
        pass

    def get_event(self, event: pygame.event.Event):
        pass

    def draw(self, screen: pygame.Surface):
        screen.fill(Colors.BLACK)

    def update(self, screen, dt):
        pass
