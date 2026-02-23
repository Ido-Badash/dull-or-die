from pathlib import Path
import glob
import os
from datetime import datetime
from typing import Tuple, Optional

import luneth_engine as le
from winmode import PygameWindowController, WindowStates

import pygame
import pygame.freetype

from .logger import logger
from .trigger_handler import TriggerHandler
from game.utils import resource_path


class BaseGame:

    def __init__(
        self,
        pygame_window_controller: PygameWindowController,
        win_state: WindowStates = WindowStates.WINDOWED_STATELESS,
        can_fullscreen: bool = False,
        can_exit_via_escape: bool = False,
        can_take_screenshots: bool = False,
        open_in_fullscreen: bool = False,
        admin: bool = False,
        game_font_path: Optional[str] = None,
        screenshots_folder_path: str = "screenshots",
        json_settings_file_path: str = "data/settings.json",
        fps: int = 60,
        default_font_size: int = 11,
        shared_settings: Optional[le.SharedSettings] = None,
        state_manager: Optional[le.StateManager] = None,
        time_manager: Optional[le.TimeManager] = None,
        global_inputs: Optional[le.GlobalInputs] = None,
        last_state_time_manager: Optional[le.TimeManager] = None,
    ):
        # store simple params
        self.fps = fps
        self.wc = pygame_window_controller
        self.win_state = win_state
        self.can_fullscreen = can_fullscreen
        self.open_in_fullscreen = open_in_fullscreen
        self.admin = admin
        self.can_exit_via_escape = can_exit_via_escape
        self.can_take_screenshots = can_take_screenshots

        # paths
        self.game_font_path = game_font_path
        self.screenshots_folder = Path(screenshots_folder_path)
        self.settings_path = Path(json_settings_file_path)

        # le managers
        self.ss = shared_settings or le.SharedSettings(json_path=self.settings_path)
        self.ss.load()

        self.sm = state_manager or le.StateManager(on_state_change=self.on_state_change)
        self.tm = time_manager or le.TimeManager()
        self.gi = global_inputs or le.GlobalInputs()

        self.last_state_tm = last_state_time_manager or le.TimeManager()

        # pygame setup
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        # inputs
        self._add_user_inputs()

        # admin inputs
        if self.admin:
            self._add_admin_inputs()

        # font
        self.font = (
            pygame.freetype.Font(resource_path(self.game_font_path))
            if self.game_font_path
            else pygame.freetype.SysFont("arial", default_font_size)
        )

        # add game reference to all states
        for state in self.sm.states:
            self.add_state(state)

    # --- states helper functions ---
    def add_state(self, state: le.State):
        logger.debug(f"Added a new state: {state.name}")
        state.game = self
        self.sm.add(state)

    # --- actions ---
    def _add_user_inputs(self):
        logger.debug("Added user inputs")
        self.gi.add_action(
            "fullscreen",
            lambda events: TriggerHandler.trigger_single_key(events, pygame.K_F11),
            self.toggle_fullscreen,
        )
        self.gi.add_action(
            "screenshot",
            lambda events: TriggerHandler.trigger_single_key(events, pygame.K_F2),
            self.take_screenshot,
        )
        if self.can_exit_via_escape:
            self.gi.add_action(
                "escape_quit",
                lambda events: TriggerHandler.trigger_single_key(
                    events, pygame.K_ESCAPE
                ),
                self.quit_game,
            )

    def _add_admin_inputs(self):
        logger.debug("Added admin inputs")
        self.gi.add_action(
            "refresh_state",
            lambda events: TriggerHandler.trigger_single_key(events, pygame.K_F3),
            self.refresh_state,
        )
        self.gi.add_action(
            "admin_switch_right",
            lambda events: TriggerHandler.trigger_single_key(events, pygame.K_RIGHT),
            self.next_state,
        )
        self.gi.add_action(
            "admin_switch_left",
            lambda events: TriggerHandler.trigger_single_key(events, pygame.K_LEFT),
            self.previous_state,
        )
        logger.info("Admin mode enabled: Use LEFT/RIGHT arrows to switch states")

    def refresh_state(self):
        self.state.startup() if self.state else None
        logger.debug(f"Refreshed state: {self.state.name}")

    def next_state(self):
        if len(self.states) > 1:
            last_state_name = self.state.name
            self.sm.next_state()
            logger.debug(
                f"Moved to next state: ({last_state_name} -> {self.state.name})"
            )
        else:
            logger.debug(
                "Cant move to next state, there are less then 2 states in the state manager!"
            )

    def previous_state(self):
        if len(self.states) > 1:
            last_state_name = self.state.name
            self.sm.previous_state()
            logger.debug(
                f"Moved to previous state: ({last_state_name} -> {self.state.name})"
            )
        else:
            logger.debug(
                "Cant move to previous state, there are less then 2 states in the state manager!"
            )

    def on_state_change(self, old: le.State, new: le.State):
        logger.debug(f"Switching from [{old.name}] to [{new.name}]")

        self.last_state_tm.reset()

    def quit_game(self):
        self.running = False
        logger.debug("Quit triggered")

    def toggle_fullscreen(self):
        if self.can_fullscreen:
            is_fullscreen = self.wc.is_current_fullscreen_mode()
            if is_fullscreen:
                self.wc.set_mode(self.win_state)
            else:
                self.wc.set_mode(WindowStates.FULLSCREEN)
            logger.debug(f"Fullscreen toggled: {'Off' if is_fullscreen else 'On'}")
        else:
            logger.debug("Cant fullscreen, 'can_fullscreen' is set to False!")

    def take_screenshot(self):
        if self.can_take_screenshots:
            # make sure screenshots folder exists
            self.screenshots_folder.mkdir(exist_ok=True)

            # get datetime for filename
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

            # pattern to count existing screenshots for this state
            pattern = str(self.screenshots_folder / "screenshot_*.png")
            screenshots = glob.glob(pattern)
            count = len(screenshots)

            # if folder has too many screenshots, delete the oldest
            if count >= 100:
                oldest = min(screenshots, key=os.path.getctime)
                os.remove(oldest)  # remove the full path

            # create the file path
            path = (
                self.screenshots_folder
                / f"screenshot_{self.state.name.value.lower()}_{formatted_datetime}.png"
            )

            # save screenshot
            pygame.image.save(self.screen, path)
            logger.info(f"Screenshot {formatted_datetime} saved in {path}")
        else:
            logger.debug(
                "Cant take a screenshot, 'can_take_screenshots' is set to False!"
            )

    def clear_screenshots_folder(self):
        logger.debug("Cleared screenshots folder")
        pattern = str(self.screenshots_folder / "screenshot_*.png")
        screenshots = glob.glob(pattern)
        for f in screenshots:
            os.remove(f)

    # --- properties ---
    @property
    def screen(self) -> pygame.Surface:
        return self.wc.get_screen()

    @property
    def size(self) -> Tuple[int, int]:
        return self.screen.get_size()

    @property
    def width(self) -> int:
        return self.screen.get_width()

    @property
    def height(self) -> int:
        return self.screen.get_height()

    @property
    def state(self):
        return self.sm.state

    @property
    def states(self):
        return self.sm.states

    @property
    def time_since_last_state(self):
        return self.last_state_tm.elapsed_time

    # --- util methods ---
    def size_depended(self, base_ratio: float):
        return min(self.width, self.height) / base_ratio

    # --- run ---
    def run(self):
        self.running = True
        logger.debug("Trying to run game...")
        try:
            if self.state:
                self.state.startup()
            logger.debug("Game is up and running!")
            while self.running and self.state:
                self.dt = self.clock.tick(self.fps) / 1000.0  # seconds

                # time managers
                self.tm.update(self.dt)
                self.last_state_tm.update(self.dt)

                # get events
                events = pygame.event.get()

                # update inputs
                self.gi.update(events, self.tm.dt)

                # event handle
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
                    else:
                        self.state.get_event(event)

                # update + draw
                self.state.update(self.screen, self.tm.dt)
                self.state.draw(self.screen)

                # update display
                pygame.display.flip()

        except Exception as e:
            logger.exception(f"An unexpected error occurred in the main loop, {e}")

        finally:
            self.ss.save()
            pygame.quit()
            logger.info("Pygame Ended")
