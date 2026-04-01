import luneth_engine as le
from winmode import PygameWindowController
from typing import Optional
from game.states import EmptyState
import pygame
import logging

class BaseGame:
    def __init__(
        self,
        pygame_window_controller: PygameWindowController,
        states: Optional[le.State] = [],
        json_settings_path: Optional[str] = None,
        logging_level: int = logging.INFO):
        """
        Params:
            - pwc - PygameWindowController from winmode lib.
            - states - BaseState childrens.
            - json_settings_path - the json path where the settings will be stored.
            - logging_level - the luenth_engine logging level.
        """
        # params handle
        self.pygame_window_controller = pygame_window_controller
        self.json_settings_path = json_settings_path if json_settings_path is not None else "data/settings.json"
        le.logger.setLevel(logging_level)
        
        # init system
        self.state_manager = le.StateManager(states)
        self.global_inputs = le.GlobalInputs()
        self.shared_settings = le.SharedSettings(json_path=self.json_settings_path)
        
        # flags
        self._running = True
        
        # time
        self.clock = pygame.time.Clock()
        self.dt = 0
        
        # settings
        self.shared_settings.load()
        self.fps = self.shared_settings.lget("fps", 60)
        
    def _has_states(self):
        return len(self.state_manager.states) > 0
              
    @property
    def screen(self) -> pygame.Surface:
        return self.pygame_window_controller.get_screen()
        
    def startup(self):
        """Used before starting the game loop"""
        pass

    def run(self):
        # current state
        self.current_state = self.state_manager.states[0] if self._has_states() else EmptyState()
        self.current_state.startup()
        
        # game loop
        while self._running:
            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.kill()
                self.current_state.get_event(event)
                
            # draw and update
            self.current_state.draw(self.screen)
            self.current_state.update(self.screen, self.dt)
            
            # update screen
            pygame.display.flip()
            
            # update delta time
            dt = self.clock.tick(self.fps) / 1000 # ms
            
        # cleanup last state on exit
        self.current_state.cleanup()
        self.on_exit()
            
    def kill(self):
        """Used for ending the game loop."""
        self._running = False
        
    def on_exit(self):
        """Runs when exiting the game loop."""
        pass