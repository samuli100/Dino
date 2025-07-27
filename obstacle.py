import random
import pygame
from constants import WIDTH, GROUND_Y, BLOCK_SIZE, GREEN
from utils import draw_pixel_art
from constants import CACTUS_PATTERNS

class Obstacle:
    """Base class for obstacles"""
    
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        """Update obstacle movement"""
        self.x -= self.speed

    def is_off_screen(self):
        """Check if obstacle is completely off screen"""
        return self.x + self.get_width() < 0

    def get_width(self):
        """Get obstacle width - to be overridden"""
        return 0

    def get_rect(self):
        """Get collision rectangle - to be overridden"""
        return pygame.Rect(0, 0, 0, 0)

    def draw(self, win):
        """Draw obstacle - to be overridden"""
        pass

class Cactus(Obstacle):
    """Cactus obstacle"""
    
    def __init__(self, base_speed, slow_motion_level):
        self.pattern = random.choice(CACTUS_PATTERNS)
        x = WIDTH
        y = GROUND_Y - len(self.pattern) * BLOCK_SIZE
        speed = base_speed - slow_motion_level * 0.5
        super().__init__(x, y, speed)

    def get_width(self):
        """Get cactus width"""
        return len(self.pattern[0]) * BLOCK_SIZE

    def get_rect(self):
        """Get collision rectangle"""
        width = len(self.pattern[0]) * BLOCK_SIZE
        height = len(self.pattern) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def get_collision_rect(self):
        """Get smaller collision rectangle for more forgiving gameplay"""
        rect = self.get_rect()
        rect.inflate_ip(-4, -4)
        return rect

    def draw(self, win):
        """Draw the cactus"""
        draw_pixel_art(win, self.pattern, self.x, self.y, GREEN)

class ObstacleManager:
    """Manages obstacle spawning and updates"""
    
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0
        self.base_speed = 6

    def update(self, upgrades):
        """Update all obstacles"""
        # Update spawn timer
        self.spawn_timer += 1
        
        # Spawn new obstacles
        if self.should_spawn():
            self.spawn_obstacle(upgrades)
            
        # Update existing obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)

    def should_spawn(self):
        """Determine if a new obstacle should spawn"""
        spawn_interval = random.randint(80, 120)
        if self.spawn_timer >= spawn_interval:
            self.spawn_timer = 0
            return True
        return False

    def spawn_obstacle(self, upgrades):
        """Spawn a new obstacle"""
        speed = self.base_speed + upgrades["speed_boost"] * 0.5
        cactus = Cactus(speed, upgrades["slow_motion"])
        self.obstacles.append(cactus)

    def check_collisions(self, player):
        """Check for collisions between player and obstacles"""
        if player.shield_active:
            return False
            
        player_rect = player.get_collision_rect()
        
        for obstacle in self.obstacles:
            if hasattr(obstacle, 'get_collision_rect'):
                obs_rect = obstacle.get_collision_rect()
            else:
                obs_rect = obstacle.get_rect()
                
            if player_rect.colliderect(obs_rect):
                return True
        return False

    def count_passed_obstacles(self):
        """Count and remove obstacles that have passed the player"""
        passed_count = 0
        for obstacle in self.obstacles[:]:
            if obstacle.x + obstacle.get_width() < 50:  # Player is at x=100
                self.obstacles.remove(obstacle)
                passed_count += 1
        return passed_count

    def draw(self, win):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            obstacle.draw(win)

    def reset(self):
        """Reset obstacle manager"""
        self.obstacles.clear()
        self.spawn_timer = 0
