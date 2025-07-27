import random
import pygame
from constants import WIDTH, HEIGHT, GROUND_Y, BLOCK_SIZE, LIGHT_GRAY, MEDIUM_GRAY
from constants import CLOUD_PATTERNS, MOUNTAIN_PATTERNS
from utils import draw_pixel_art


class BackgroundElement:
    """Base class for background elements"""
    
    def __init__(self, x, y, speed, pattern):
        self.x = x
        self.y = y
        self.speed = speed
        self.pattern = pattern

    def update(self):
        """Update element movement"""
        self.x -= self.speed

    def is_off_screen(self):
        """Check if element is completely off screen"""
        return self.x + len(self.pattern[0]) * BLOCK_SIZE < 0

    def draw(self, win, color):
        """Draw the background element"""
        draw_pixel_art(win, self.pattern, self.x, self.y, color)


class Cloud(BackgroundElement):
    """Cloud background element"""
    
    def __init__(self):
        pattern = random.choice(CLOUD_PATTERNS)
        x = WIDTH + random.randint(0, 200)
        y = random.randint(50, 150)
        speed = random.uniform(0.5, 1.5)
        super().__init__(x, y, speed, pattern)


class Mountain(BackgroundElement):
    """Mountain background element"""
    
    def __init__(self):
        pattern = random.choice(MOUNTAIN_PATTERNS)
        x = WIDTH + random.randint(0, 100)
        y = GROUND_Y - len(pattern) * BLOCK_SIZE
        speed = random.uniform(0.2, 0.8)
        super().__init__(x, y, speed, pattern)


class BackgroundManager:
    """Manages background elements like clouds and mountains"""
    
    def __init__(self):
        self.clouds = []
        self.mountains = []
        self.cloud_spawn_timer = 0
        self.mountain_spawn_timer = 0
        
        # Initialize with some elements
        self.spawn_initial_elements()

    def spawn_initial_elements(self):
        """Spawn initial background elements"""
        # Spawn some clouds
        for i in range(3):
            cloud = Cloud()
            cloud.x = random.randint(-200, WIDTH)
            self.clouds.append(cloud)
        
        # Spawn some mountains
        for i in range(2):
            mountain = Mountain()
            mountain.x = random.randint(-300, WIDTH)
            self.mountains.append(mountain)

    def update(self):
        """Update all background elements"""
        # Update spawn timers
        self.cloud_spawn_timer += 1
        self.mountain_spawn_timer += 1
        
        # Spawn new clouds
        if self.cloud_spawn_timer >= random.randint(300, 600):  # 5-10 seconds
            self.clouds.append(Cloud())
            self.cloud_spawn_timer = 0
        
        # Spawn new mountains
        if self.mountain_spawn_timer >= random.randint(600, 1200):  # 10-20 seconds
            self.mountains.append(Mountain())
            self.mountain_spawn_timer = 0
        
        # Update existing elements
        for cloud in self.clouds[:]:
            cloud.update()
            if cloud.is_off_screen():
                self.clouds.remove(cloud)
                
        for mountain in self.mountains[:]:
            mountain.update()
            if mountain.is_off_screen():
                self.mountains.remove(mountain)

    def draw(self, win):
        """Draw all background elements"""
        # Draw mountains first (furthest back)
        for mountain in self.mountains:
            mountain.draw(win, MEDIUM_GRAY)
        
        # Draw clouds (closer to front)
        for cloud in self.clouds:
            cloud.draw(win, LIGHT_GRAY)

    def reset(self):
        """Reset background manager"""
        self.clouds.clear()
        self.mountains.clear()
        self.cloud_spawn_timer = 0
        self.mountain_spawn_timer = 0
        self.spawn_initial_elements()