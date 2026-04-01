from game.ui import Colors
from game.core import BaseGame
from game.states import States, EmptyState
from game.utils import logger
from winmode import PygameWindowController, WindowStates
import logging
import time

def main():
    # logger config
    logging_level = logging.INFO
    logger.setLevel(logging_level)

    logger.info("=== Game - Starting ===")

    # consts
    SIZE = (800, 450)

    # create pygame window controller
    pwc = PygameWindowController(SIZE)
    game = BaseGame(pwc, logging_level=logging_level)
    game.run()


if __name__ == "__main__":
    main()
