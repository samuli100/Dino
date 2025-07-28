import sys
import pygame
from constants import WIDTH, HEIGHT, FPS, set_color_manager
from game_states import MenuState, GameState_Playing, GameOverState
from save_system import SaveSystem
from shop import Shop
from settings_system import SettingsSystem
from color_manager import ColorManager
from display_system import DisplaySystem
from settings_menu import SettingsMenu


class GameManager:
    def __init__(self):
        pygame.init()
        self.save_system = SaveSystem()
        self.settings_system = SettingsSystem()
        self.color_manager = ColorManager(self.settings_system)
        self.display_system = DisplaySystem(self.settings_system, self.color_manager)
        
        set_color_manager(self.color_manager)
        
        self.shop = Shop(self.save_system)
        self.settings_menu = SettingsMenu(self.settings_system, self.color_manager)
        
        pygame.display.set_caption("Rogue Dino")
        self.clock = pygame.time.Clock()
        
        self.current_state_name = "menu"
        self.states = {
            "menu": MenuState(self),
            "game": None,
            "shop": self.shop,
            "settings": self.settings_menu,
            "game_over": None
        }

    def change_state(self, new_state_name):
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
        elif new_state_name == "apply_resolution":
            self.display_system.update_display()
            return  
        elif new_state_name == "apply_fullscreen":
            self.display_system.update_display()
            return  
        elif new_state_name == "quit":
            pygame.quit()
            import sys
            sys.exit()
        
        self.current_state_name = new_state_name

    def handle_custom_keybinds(self, event):
        if event.type == pygame.KEYDOWN and self.current_state_name == "game":
            game_state = self.states["game"]
            if game_state:
                if event.key == self.settings_system.get_keybind("jump"):
                    jump_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                    return game_state.handle_event(jump_event)
                elif event.key == self.settings_system.get_keybind("shield"):
                    shield_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)
                    return game_state.handle_event(shield_event)
                elif event.key == self.settings_system.get_keybind("dash"):
                    dash_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)
                    return game_state.handle_event(dash_event)
                elif event.key == self.settings_system.get_keybind("menu"):
                    return "menu"
        return None

    def run(self):
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            current_state = self.states.get(self.current_state_name)
            if not current_state:
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    custom_result = self.handle_custom_keybinds(event)
                    if custom_result:
                        if custom_result == "quit":
                            running = False
                        elif custom_result.startswith("apply_"):
                            self.change_state(custom_result)
                        else:
                            self.change_state(custom_result)
                        continue
                    
                    result = current_state.handle_event(event)
                    if result and result != self.current_state_name:
                        if result == "quit":
                            running = False
                        elif result.startswith("apply_"):
                            self.change_state(result)
                        else:
                            self.change_state(result)
            
            if hasattr(current_state, 'update'):
                result = current_state.update()
                if result and result != self.current_state_name:
                    self.change_state(result)
            
            virtual_screen = self.display_system.get_virtual_screen()
            current_state.draw(virtual_screen)
            
            self.display_system.present()
        
        pygame.quit()
        sys.exit()