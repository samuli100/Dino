import pygame
import math

class DisplaySystem:
    def __init__(self, settings_system, color_manager):
        self.settings_system = settings_system
        self.color_manager = color_manager
        
        self.base_width = 800
        self.base_height = 400
        
        self.virtual_screen = pygame.Surface((self.base_width, self.base_height))
        
        self.screen = None
        self.display_rect = pygame.Rect(0, 0, self.base_width, self.base_height)
        
        self.poster_font = pygame.font.Font(None, 36)
        self.poster_small_font = pygame.font.Font(None, 24)
        
        self.init_display()
    
    def init_display(self):
        if self.settings_system.data["fullscreen"]:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.calculate_fullscreen_layout()
        else:
            width, height = self.settings_system.get_scaled_resolution()
            self.screen = pygame.display.set_mode((width, height))
            self.display_rect = pygame.Rect(0, 0, width, height)
    
    def calculate_fullscreen_layout(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        target_height = int(screen_height * 0.75)
        target_width = int(target_height * (self.base_width / self.base_height))
        
        if target_width > screen_width * 0.9:
            target_width = int(screen_width * 0.9)
            target_height = int(target_width * (self.base_height / self.base_width))
        
        x = (screen_width - target_width) // 2
        y = (screen_height - target_height) // 2
        
        self.display_rect = pygame.Rect(x, y, target_width, target_height)
    
    def get_virtual_screen(self):
        return self.virtual_screen
    
    def present(self):
        if self.settings_system.data["fullscreen"]:
            self.draw_poster_background()
        
        if self.display_rect.size != (self.base_width, self.base_height):
            scaled_surface = pygame.transform.scale(self.virtual_screen, self.display_rect.size)
            self.screen.blit(scaled_surface, self.display_rect)
        else:
            self.screen.blit(self.virtual_screen, self.display_rect)
        
        pygame.display.flip()
    
    def draw_poster_background(self):
        colors = self.color_manager.get_poster_colors()
        
        self.screen.fill(colors["background"])
        
        self.draw_poster_border(colors)
        
        self.draw_poster_decorations(colors)
    
    def draw_poster_border(self, colors):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        border_width = 20
        
        pygame.draw.rect(self.screen, colors["border"], 
                        (self.display_rect.x - border_width, 
                         self.display_rect.y - border_width,
                         self.display_rect.width + border_width * 2,
                         self.display_rect.height + border_width * 2))
        
        inner_border = 5
        pygame.draw.rect(self.screen, colors["accent"],
                        (self.display_rect.x - inner_border,
                         self.display_rect.y - inner_border,
                         self.display_rect.width + inner_border * 2,
                         self.display_rect.height + inner_border * 2))
        
        self.draw_corner_decorations(colors)
    
    def draw_corner_decorations(self, colors):
        corner_size = 40
        
        points = [
            (self.display_rect.x - 20, self.display_rect.y - 20),
            (self.display_rect.x - 20 + corner_size, self.display_rect.y - 20),
            (self.display_rect.x - 20, self.display_rect.y - 20 + corner_size)
        ]
        pygame.draw.polygon(self.screen, colors["text"], points)
        
        points = [
            (self.display_rect.right + 20, self.display_rect.y - 20),
            (self.display_rect.right + 20 - corner_size, self.display_rect.y - 20),
            (self.display_rect.right + 20, self.display_rect.y - 20 + corner_size)
        ]
        pygame.draw.polygon(self.screen, colors["text"], points)
        
        points = [
            (self.display_rect.x - 20, self.display_rect.bottom + 20),
            (self.display_rect.x - 20 + corner_size, self.display_rect.bottom + 20),
            (self.display_rect.x - 20, self.display_rect.bottom + 20 - corner_size)
        ]
        pygame.draw.polygon(self.screen, colors["text"], points)
        
        points = [
            (self.display_rect.right + 20, self.display_rect.bottom + 20),
            (self.display_rect.right + 20 - corner_size, self.display_rect.bottom + 20),
            (self.display_rect.right + 20, self.display_rect.bottom + 20 - corner_size)
        ]
        pygame.draw.polygon(self.screen, colors["text"], points)
    
    def draw_poster_decorations(self, colors):
        screen_width = self.screen.get_width()
        
        title_y = max(50, self.display_rect.y - 80)
        title_text = self.poster_font.render("ROGUE DINO", True, colors["text"])
        title_rect = title_text.get_rect(center=(screen_width // 2, title_y))
        self.screen.blit(title_text, title_rect)
        
        if self.display_rect.bottom + 60 < self.screen.get_height():
            bottom_text = self.poster_small_font.render("Press ESC for Menu", True, colors["accent"])
            bottom_rect = bottom_text.get_rect(center=(screen_width // 2, self.display_rect.bottom + 40))
            self.screen.blit(bottom_text, bottom_rect)
        
        self.draw_stars(colors)
    
    def draw_stars(self, colors):
        star_size = 8
        
        left_x = self.display_rect.x - 60
        if left_x > star_size * 2:
            for i in range(3):
                y = self.display_rect.y + (self.display_rect.height // 4) * (i + 1)
                self.draw_star(left_x, y, star_size, colors["accent"])
        
        right_x = self.display_rect.right + 60
        if right_x < self.screen.get_width() - star_size * 2:
            for i in range(3):
                y = self.display_rect.y + (self.display_rect.height // 4) * (i + 1)
                self.draw_star(right_x, y, star_size, colors["accent"])
    
    def draw_star(self, x, y, size, color):
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            
            star_x = x + radius * math.cos(angle - math.pi / 2)
            star_y = y + radius * math.sin(angle - math.pi / 2)
            points.append((star_x, star_y))
        
        pygame.draw.polygon(self.screen, color, points)
    
    def update_display(self):
        self.init_display()
        
    def get_mouse_pos(self):
        if not self.settings_system.data["fullscreen"]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            scale_x = self.base_width / self.display_rect.width
            scale_y = self.base_height / self.display_rect.height
            return int(mouse_x * scale_x), int(mouse_y * scale_y)
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x = mouse_x - self.display_rect.x
            rel_y = mouse_y - self.display_rect.y
            
            if 0 <= rel_x <= self.display_rect.width and 0 <= rel_y <= self.display_rect.height:
                scale_x = self.base_width / self.display_rect.width
                scale_y = self.base_height / self.display_rect.height
                return int(rel_x * scale_x), int(rel_y * scale_y)
            else:
                return -1, -1  