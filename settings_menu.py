import pygame
from constants import WIDTH, HEIGHT

class SettingsMenu:
    def __init__(self, settings_system, color_manager):
        self.settings_system = settings_system
        self.color_manager = color_manager
        
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        self.menu_items = [
            "resolution",
            "fullscreen",
            "color_scheme",
            "keybind_jump",
            "keybind_shield",
            "keybind_dash",
            "back"
        ]
        
        self.selected_index = 0
        self.waiting_for_key = None  
        
        self.nav_keys = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_w: "up",
            pygame.K_s: "down",
            pygame.K_PLUS: "increase",
            pygame.K_EQUALS: "increase",  
            pygame.K_KP_PLUS: "increase",
            pygame.K_MINUS: "decrease",
            pygame.K_KP_MINUS: "decrease",
            pygame.K_x: "fullscreen",
            pygame.K_RETURN: "select",
            pygame.K_SPACE: "select",
            pygame.K_ESCAPE: "back",
            pygame.K_1: "color1",
            pygame.K_2: "color2",
            pygame.K_3: "color3"
        }
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.waiting_for_key:
                if event.key == pygame.K_ESCAPE:
                    self.waiting_for_key = None
                else:
                    action = self.waiting_for_key.replace("keybind_", "")
                    self.settings_system.set_keybind(action, event.key)
                    self.waiting_for_key = None
                    self.settings_system.save_settings()
                return None
            
            action = self.nav_keys.get(event.key)
            if action:
                return self.handle_action(action)
        
        elif event.type == pygame.MOUSEWHEEL:
            if not self.waiting_for_key:
                if event.y > 0:  
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                elif event.y < 0:  
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                    
        return None
    
    def handle_action(self, action):
        if action == "up":
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif action == "down":
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif action == "increase":
            return self.handle_increase()
        elif action == "decrease":
            return self.handle_decrease()
        elif action == "fullscreen":
            self.settings_system.toggle_fullscreen()
            self.settings_system.save_settings()
            return "apply_fullscreen"
        elif action == "select":
            return self.handle_select()
        elif action == "back":
            return "menu"
        elif action in ["color1", "color2", "color3"]:
            scheme_num = int(action[-1])
            self.settings_system.change_color_scheme(scheme_num)
            self.settings_system.save_settings()
        
        return None
    
    def handle_increase(self):
        current_item = self.menu_items[self.selected_index]
        if current_item == "resolution":
            if self.settings_system.change_resolution(1):
                self.settings_system.save_settings()
                return "apply_resolution"
        return None
    
    def handle_decrease(self):
        current_item = self.menu_items[self.selected_index]
        if current_item == "resolution":
            if self.settings_system.change_resolution(-1):
                self.settings_system.save_settings()
                return "apply_resolution"
        return None
    
    def handle_select(self):
        current_item = self.menu_items[self.selected_index]
        
        if current_item == "resolution":
            self.settings_system.save_settings()
            return "apply_resolution"
        elif current_item == "fullscreen":
            self.settings_system.toggle_fullscreen()
            self.settings_system.save_settings()
            return "apply_fullscreen"
        elif current_item.startswith("keybind_"):
            self.waiting_for_key = current_item
        elif current_item == "back":
            return "menu"
        
        return None
    
    def draw(self, win):
        colors = self.color_manager.get_colors()
        
        win.fill(colors["UI_BACKGROUND"])
        
        title_y = max(60, HEIGHT // 8)
        title_text = self.title_font.render("SETTINGS", True, colors["UI_TEXT"])
        title_rect = title_text.get_rect(center=(WIDTH//2, title_y))
        win.blit(title_text, title_rect)
        
        if self.waiting_for_key:
            instruction = "Press any key to bind (ESC to cancel)"
            color = colors["UI_ACCENT"]
        else:
            instruction = "Arrow/WASD: Navigate • +/-: Change • X: Fullscreen • 1-3: Colors • Mouse Wheel: Scroll"
            color = colors["GRAY"]
        
        inst_text = self.small_font.render(instruction, True, color)
        
        if inst_text.get_width() > WIDTH - 40:
            inst_text = self.tiny_font.render(instruction, True, color)
        
        inst_rect = inst_text.get_rect(center=(WIDTH//2, HEIGHT - 30))
        win.blit(inst_text, inst_rect)
        
        menu_start_y = title_y + 60
        available_height = HEIGHT - menu_start_y - 60  
        y_spacing = min(50, available_height // len(self.menu_items))
        
        for i, item in enumerate(self.menu_items):
            y = menu_start_y + i * y_spacing
            self.draw_menu_item(win, item, y, i == self.selected_index)
    
    def draw_menu_item(self, win, item, y, selected):
        colors = self.color_manager.get_colors()
        
        margin = max(20, WIDTH // 20)  
        bg_width = WIDTH - 2 * margin
        bg_height = 40
        bg_x = margin
        
        if selected:
            bg_rect = pygame.Rect(bg_x, y - 15, bg_width, bg_height)
            pygame.draw.rect(win, colors["BUTTON_HOVER"], bg_rect)
            pygame.draw.rect(win, colors["UI_ACCENT"], bg_rect, 2)
        
        label, value = self.get_item_display(item)
        
        if self.waiting_for_key == item:
            label_color = colors["UI_ACCENT"]
            value_color = colors["UI_ACCENT"]
        else:
            label_color = colors["UI_TEXT"]
            value_color = colors["GRAY"]
        
        label_text = self.font.render(label, True, label_color)
        value_text = self.font.render(value, True, value_color)
        
        max_label_width = bg_width // 2 - 20
        max_value_width = bg_width // 2 - 20
        
        if label_text.get_width() > max_label_width:
            label_text = self.small_font.render(label, True, label_color)
        if value_text.get_width() > max_value_width:
            value_text = self.small_font.render(value, True, value_color)
        
        win.blit(label_text, (bg_x + 20, y))
        
        value_rect = value_text.get_rect()
        value_rect.right = bg_x + bg_width - 20
        value_rect.y = y
        win.blit(value_text, value_rect)
    
    def get_item_display(self, item):
        if item == "resolution":
            scale = self.settings_system.data["resolution_scale"]
            width, height = self.settings_system.get_scaled_resolution()
            return "Resolution", f"{width}x{height} ({scale}x)"
        
        elif item == "fullscreen":
            value = "ON" if self.settings_system.data["fullscreen"] else "OFF"
            return "Fullscreen", value
        
        elif item == "color_scheme":
            return "Color Scheme", self.settings_system.get_color_scheme_name()
        
        elif item.startswith("keybind_"):
            action = item.replace("keybind_", "")
            action_names = {
                "jump": "Jump",
                "shield": "Shield", 
                "dash": "Air Dash"
            }
            key = self.settings_system.get_keybind(action)
            key_name = self.settings_system.get_key_name(key)
            
            if self.waiting_for_key == item:
                return action_names.get(action, action), "Press key..."
            else:
                return action_names.get(action, action), key_name
        
        elif item == "back":
            return "Back to Menu", ""
        
        return item, ""