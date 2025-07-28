class ColorManager:
    def __init__(self, settings_system):
        self.settings_system = settings_system
        
        self.base_colors = {
            "WHITE": (255, 255, 255),
            "LIGHT_GRAY": (220, 220, 220),
            "MEDIUM_GRAY": (180, 180, 180),
            "GRAY": (128, 128, 128),
            "DARK_GRAY": (80, 80, 80),
            "BLACK": (40, 40, 40),
            "VERY_DARK": (20, 20, 20),
            "UI_BACKGROUND": (248, 248, 248),
            "UI_BORDER": (200, 200, 200),
            "UI_TEXT": (60, 60, 60),
            "UI_ACCENT": (100, 100, 100),
            "BUTTON_HOVER": (230, 230, 230)
        }
        
        # Old paper color scheme
        self.old_paper_colors = {
            "WHITE": (255, 248, 220),  # Cream white
            "LIGHT_GRAY": (240, 228, 200),  # Light cream
            "MEDIUM_GRAY": (210, 190, 160),  # Medium cream
            "GRAY": (180, 150, 120),  # Brown-gray
            "DARK_GRAY": (120, 90, 60),  # Dark brown
            "BLACK": (80, 50, 30),  # Dark brown
            "VERY_DARK": (60, 35, 20),  # Very dark brown
            "UI_BACKGROUND": (250, 240, 210),  # Light cream
            "UI_BORDER": (200, 170, 140),  # Brown border
            "UI_TEXT": (90, 60, 40),  # Dark brown text
            "UI_ACCENT": (140, 100, 70),  # Brown accent
            "BUTTON_HOVER": (235, 220, 190)  # Hover cream
        }
    
    def invert_color(self, color):
        return (255 - color[0], 255 - color[1], 255 - color[2])
    
    def get_colors(self):
        scheme = self.settings_system.data["color_scheme"]
        
        if scheme == 2:  # Old paper
            return self.old_paper_colors
        elif scheme == 3:  # Inverted
            return {name: self.invert_color(color) for name, color in self.base_colors.items()}
        else:  # Normal 
            return self.base_colors
    
    def get_color(self, color_name):
        colors = self.get_colors()
        return colors.get(color_name, self.base_colors.get(color_name, (255, 255, 255)))
    
    def get_poster_colors(self):
        scheme = self.settings_system.data["color_scheme"]
        
        if scheme == 2:  # Old paper 
            return {
                "background": (139, 115, 85),  # Dark brown
                "border": (101, 78, 57),  # Darker brown
                "text": (250, 240, 210),  # Light cream
                "accent": (205, 175, 140)  # Accent brown
            }
        elif scheme == 3:  # Inverted 
            return {
                "background": (50, 50, 50),  # Dark gray
                "border": (20, 20, 20),  # Very dark gray
                "text": (200, 200, 200),  # Light gray
                "accent": (150, 150, 150)  # Medium gray
            }
        else:  # Normal 
            return {
                "background": (139, 115, 85),  # Western brown
                "border": (101, 67, 33),  # Dark brown
                "text": (255, 248, 220),  # Cream
                "accent": (205, 175, 149)  # Light brown
            }