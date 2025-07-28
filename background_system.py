import random
import pygame
from constants import WIDTH, HEIGHT, GROUND_Y, BLOCK_SIZE, get_color
from constants import CLOUD_PATTERNS, MOUNTAIN_PATTERNS
from utils import draw_pixel_art


class BackgroundElement:
    def __init__(self, x, y, speed, pattern):
        self.x = x
        self.y = y
        self.speed = speed
        self.pattern = pattern

    def update(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x + len(self.pattern[0]) * BLOCK_SIZE < 0

    def draw(self, win, color):
        draw_pixel_art(win, self.pattern, self.x, self.y, color)


class Cloud(BackgroundElement):
    def __init__(self):
        pattern = random.choice(CLOUD_PATTERNS)
        x = WIDTH + random.randint(0, 200)
        y = random.randint(50, 150)
        speed = random.uniform(0.5, 1.5)
        super().__init__(x, y, speed, pattern)


class Mountain(BackgroundElement):
    def __init__(self):
        pattern = random.choice(MOUNTAIN_PATTERNS)
        x = WIDTH + random.randint(0, 100)
        y = GROUND_Y - len(pattern) * BLOCK_SIZE
        speed = random.uniform(0.2, 0.8)
        super().__init__(x, y, speed, pattern)


class BackgroundManager:
    def __init__(self):
        self.clouds = []
        self.mountains = []
        self.cloud_spawn_timer = 0
        self.mountain_spawn_timer = 0
        
        self.spawn_initial_elements()

    def spawn_initial_elements(self):
        for i in range(3):
            cloud = Cloud()
            cloud.x = random.randint(-200, WIDTH)
            self.clouds.append(cloud)
        
        for i in range(2):
            mountain = Mountain()
            mountain.x = random.randint(-300, WIDTH)
            self.mountains.append(mountain)

    def update(self):
        self.cloud_spawn_timer += 1
        self.mountain_spawn_timer += 1
        
        if self.cloud_spawn_timer >= random.randint(300, 600):
            self.clouds.append(Cloud())
            self.cloud_spawn_timer = 0
        
        if self.mountain_spawn_timer >= random.randint(600, 1200):
            self.mountains.append(Mountain())
            self.mountain_spawn_timer = 0
        
        for cloud in self.clouds[:]:
            cloud.update()
            if cloud.is_off_screen():
                self.clouds.remove(cloud)
                
        for mountain in self.mountains[:]:
            mountain.update()
            if mountain.is_off_screen():
                self.mountains.remove(mountain)

    def draw(self, win):
        for mountain in self.mountains:
            mountain.draw(win, get_color("MEDIUM_GRAY"))
        
        for cloud in self.clouds:
            cloud.draw(win, get_color("LIGHT_GRAY"))

    def reset(self):
        self.clouds.clear()
        self.mountains.clear()
        self.cloud_spawn_timer = 0
        self.mountain_spawn_timer = 0
        self.spawn_initial_elements()