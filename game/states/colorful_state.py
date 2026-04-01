import pygame


from game.utils import logger
from game.ui import Colors
from .states import States


class ColorfulState:
    def __init__(self, color = Colors.BLACK):
        self.name = States.COLORFUL_STATE
        self.color = color

    def startup(self):
        pass

    def cleanup(self):
        pass

    def get_event(self, event: pygame.event.Event):
        pass

    def draw(self, screen: pygame.Surface):
        screen.fill(self.color)

    def update(self, screen, dt):
        pass
