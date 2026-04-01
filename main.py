from game.ui import Colors
from game.core import BaseGame, BaseState
from game.states import States, EmptyState, ColorfulState
from game.utils import logger
from winmode import PygameWindowController, WindowStates
import logging
import time
from typing import List

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
    
    # add states
    states: List[BaseState]  = [ColorfulState(Colors.BLUE), ColorfulState(Colors.RED), ColorfulState(Colors.GREEN)]
    for state in states:
        logging.debug(f"Adding state to state manager: {state.name}")
        game.state_manager.add(state)
    
    # run game
    game.run()


if __name__ == "__main__":
    main()
