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
        """
        # params handle
        self.pygame_window_controller = pygame_window_controller
        self.json_settings_path = json_settings_path if json_settings_path is not None else "data/settings.json"
        le.logger.setLevel(logging_level)
        
        # init system
        self.state_manager = le.StateManager(states)
        self.global_inputs = le.GlobalInputs()
        self.shared_settings = le.SharedSettings(json_path=self.json_settings_path)
        
        # current state
        self.current_state = states[0] if len(states) > 0 else EmptyState(self)
        
        # flags
        self._running = True
        
        # time
        self.clock = pygame.time.Clock()
        self.dt = 0
        
        # settings
        self.shared_settings.load()
        self.fps = self.shared_settings.lget("fps", 60)
    
    def startup(self):
        self.current_state.startup()
        
    def cleanup(self):
        self.current_state.cleanup()
    
    def draw(self, screen):
        self.current_state.draw(screen)
        
    def get_event(self, event):
        self.current_state.get_event(event)
        
    def update(self, screen, dt):
        self.current_state.update(screen, dt)
        
    @property
    def screen(self) -> pygame.Surface:
        return self.pygame_window_controller.get_screen()
    
    def run(self):
        self.startup()
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.kill()
                self.get_event(event)
            self.draw(self.screen)
            self.update(self.screen, self.dt)
            pygame.display.flip()
            dt = self.clock.tick(self.fps) / 1000 # ms
        self.cleanup()
        self.on_exit()
            
    def kill(self):
        """Used for ending the game loop."""
        self._running = False
        
    def on_exit(self):
        """Runs when exiting the game loop."""
        pass