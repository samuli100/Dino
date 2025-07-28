import json
import os
import pygame

class SettingsSystem:
    def __init__(self):
        self.settings_file = "dino_settings.json"
        
        self.data = {
            "resolution_scale": 1.0,  
            "fullscreen": False,
            "color_scheme": 1,  # 1=normal, 2=old paper, 3=inverted
            "keybinds": {
                "jump": pygame.K_SPACE,
                "shield": pygame.K_s,
                "dash": pygame.K_d,
                "menu": pygame.K_ESCAPE,
                "shop": pygame.K_s
            }
        }
        
        self.resolution_options = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]
        self.current_resolution_index = 2  
        
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
                    
                    if self.data["resolution_scale"] in self.resolution_options:
                        self.current_resolution_index = self.resolution_options.index(self.data["resolution_scale"])
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get_scaled_resolution(self):
        base_width, base_height = 800, 400
        scale = self.data["resolution_scale"]
        return int(base_width * scale), int(base_height * scale)
    
    def change_resolution(self, direction):
        old_index = self.current_resolution_index
        self.current_resolution_index += direction
        self.current_resolution_index = max(0, min(len(self.resolution_options) - 1, self.current_resolution_index))
        
        if self.current_resolution_index != old_index:
            self.data["resolution_scale"] = self.resolution_options[self.current_resolution_index]
            return True
        return False
    
    def toggle_fullscreen(self):
        self.data["fullscreen"] = not self.data["fullscreen"]
        return self.data["fullscreen"]
    
    def change_color_scheme(self, scheme):
        if 1 <= scheme <= 3:
            self.data["color_scheme"] = scheme
    
    def get_color_scheme_name(self):
        schemes = {1: "Normal", 2: "Old Paper", 3: "Inverted"}
        return schemes.get(self.data["color_scheme"], "Normal")
    
    def set_keybind(self, action, key):
        if action in self.data["keybinds"]:
            self.data["keybinds"][action] = key
    
    def get_keybind(self, action):
        return self.data["keybinds"].get(action, pygame.K_UNKNOWN)
    
    def get_key_name(self, key):
        key_names = {
            pygame.K_SPACE: "SPACE",
            pygame.K_RETURN: "ENTER",
            pygame.K_ESCAPE: "ESC",
            pygame.K_LSHIFT: "L-SHIFT",
            pygame.K_RSHIFT: "R-SHIFT",
            pygame.K_LCTRL: "L-CTRL",
            pygame.K_RCTRL: "R-CTRL",
            pygame.K_LALT: "L-ALT",
            pygame.K_RALT: "R-ALT",
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_TAB: "TAB",
            pygame.K_BACKSPACE: "BACKSPACE",
            pygame.K_DELETE: "DELETE"
        }
        
        if key in key_names:
            return key_names[key]
        elif 97 <= key <= 122:  # a-z
            return chr(key).upper()
        elif 48 <= key <= 57:  # 0-9
            return chr(key)
        else:
            return f"KEY_{key}"