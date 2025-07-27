import sys
import pygame
from constants import WIDTH, HEIGHT, FPS
from game_states import MenuState, GameState_Playing, GameOverState
from save_system import SaveSystem
from shop import Shop


class GameManager:
    """Main game manager that handles states and flow"""
    
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chrome Dino - Enhanced with Shop")
        self.clock = pygame.time.Clock()
        
        # Initialize systems
        self.save_system = SaveSystem()
        self.shop = Shop(self.save_system)
        
        # Initialize states
        self.current_state_name = "menu"
        self.states = {
            "menu": MenuState(self),
            "game": None,  # Created when needed
            "shop": self.shop,
            "game_over": None  # Created when needed
        }

    def change_state(self, new_state_name):
        """Change to a new game state"""
        if new_state_name == "game":
            self.states["game"] = GameState_Playing(self)
        elif new_state_name == "game_over":
            if self.states["game"]:
                game_state = self.states["game"]
                self.states["game_over"] = GameOverState(
                    self, 
                    game_state.score, 
                    game_state.coins_this_run
                )
        
        self.current_state_name = new_state_name

    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            # Get current state
            current_state = self.states.get(self.current_state_name)
            if not current_state:
                break
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    # Let the current state handle the event
                    result = current_state.handle_event(event)
                    if result and result != self.current_state_name:
                        if result == "quit":
                            running = False
                        else:
                            self.change_state(result)
            
            # Update current state (if it has an update method)
            if hasattr(current_state, 'update'):
                result = current_state.update()
                if result and result != self.current_state_name:
                    self.change_state(result)
            
            # Draw current state
            current_state.draw(self.win)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()