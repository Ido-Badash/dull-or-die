from game.ui import Colors
from game.core import BaseGame, logger
from game.states import States, GamePlay
import logging
from winmode import WindowStates, PygameWindowController
import time

def main():
    # logger config
    logger.setLevel(logging.DEBUG)

    logger.info("=== Game - Starting ===")

    # consts
    SIZE = (800, 450)

    # # create game
    # game = BaseGame(
    #     PygameWindowController(SIZE),
    #     admin=True,
    #     can_exit_via_escape=True,
    #     can_fullscreen=True,
    #     can_take_screenshots=True,
    # )

    # # defines states
    # states = [GamePlay(game)]

    # # add to game all states
    # for state in states:
    #     game.add_state(state)

    # # run the game loop
    # try:
    #     time.sleep(0.5) # small delay before running the game
    #     game.run()
    # except Exception as e:
    #     logger.exception(f"Fatal error: {e}")
    # finally:
        # logger.info("=== Game - Ended ===")


if __name__ == "__main__":
    main()
