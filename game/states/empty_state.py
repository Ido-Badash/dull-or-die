import pygame


from game.utils import logger
from game.ui import Colors
from .states import States


class EmptyState:
    def __init__(self, name=States.EMPTY_STATE):
        self.name = name

    def startup(self):
        pass

    def cleanup(self):
        pass

    def get_event(self, event: pygame.event.Event):
        pass

    def draw(self, screen: pygame.Surface):
        screen.fill(Colors.BLACK)

    def update(self, screen, dt):
        pass
