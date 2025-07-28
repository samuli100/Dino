import random
import pygame
from constants import WIDTH, GROUND_Y, BLOCK_SIZE, DARK_GRAY
from utils import draw_pixel_art
from constants import CACTUS_PATTERNS

class Obstacle:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x + self.get_width() < 0

    def get_width(self):
        return 0

    def get_rect(self):
        return pygame.Rect(0, 0, 0, 0)

    def draw(self, win):
        pass

class Cactus(Obstacle):
    def __init__(self, speed, slow_motion_level):
        self.pattern = random.choice(CACTUS_PATTERNS)
        x = WIDTH
        y = GROUND_Y - len(self.pattern) * BLOCK_SIZE
        final_speed = speed - slow_motion_level * 0.5
        super().__init__(x, y, final_speed)

    def get_width(self):
        return len(self.pattern[0]) * BLOCK_SIZE

    def get_rect(self):
        width = len(self.pattern[0]) * BLOCK_SIZE
        height = len(self.pattern) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def get_collision_rect(self):
        rect = self.get_rect()
        rect.inflate_ip(-4, -4)
        return rect

    def draw(self, win):
        draw_pixel_art(win, self.pattern, self.x, self.y, DARK_GRAY)

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = 0
        self.base_speed = 6
        self.current_speed = self.base_speed
        self.game_time = 0
        self.obstacles_destroyed_by_dash = 0

    def update(self, upgrades):
        self.game_time += 1
        
        acceleration_rate = 0.05 - (upgrades["slow_acceleration"] * 0.01)
        acceleration_rate = max(0.01, acceleration_rate)
        
        speed_increase = (self.game_time // 300) * acceleration_rate
        self.current_speed = self.base_speed + speed_increase + upgrades["speed_boost"] * 0.5
        
        self.spawn_timer += 1
        
        if self.should_spawn():
            self.spawn_obstacle(upgrades)
            
        for obstacle in self.obstacles[:]:
            obstacle.speed = self.current_speed - upgrades["slow_motion"] * 0.5
            obstacle.update()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)

    def should_spawn(self):
        base_interval = 100
        speed_factor = max(0.5, 1.0 - (self.current_speed - self.base_speed) * 0.1)
        spawn_interval = int(base_interval * speed_factor)
        spawn_interval = max(60, min(120, spawn_interval))
        
        if self.spawn_timer >= spawn_interval:
            self.spawn_timer = 0
            return True
        return False

    def spawn_obstacle(self, upgrades):
        cactus = Cactus(self.current_speed, upgrades["slow_motion"])
        self.obstacles.append(cactus)

    def check_collisions(self, player, upgrades):
        if player.shield_active or player.invulnerable_timer > 0:
            return False
            
        player_rect = player.get_collision_rect()
        
        for obstacle in self.obstacles[:]:
            if hasattr(obstacle, 'get_collision_rect'):
                obs_rect = obstacle.get_collision_rect()
            else:
                obs_rect = obstacle.get_rect()
                
            if player_rect.colliderect(obs_rect):
                if player.is_dashing():
                    self.obstacles.remove(obstacle)
                    self.obstacles_destroyed_by_dash += 1
                    return False
                
                self.obstacles.remove(obstacle)
                
                return player.take_damage(upgrades)
        return False

    def count_passed_obstacles(self):
        passed_count = 0
        for obstacle in self.obstacles[:]:
            if obstacle.x + obstacle.get_width() < 50:
                self.obstacles.remove(obstacle)
                passed_count += 1
        return passed_count

    def get_destroyed_count(self):
        count = self.obstacles_destroyed_by_dash
        self.obstacles_destroyed_by_dash = 0
        return count

    def draw(self, win):
        for obstacle in self.obstacles:
            obstacle.draw(win)

    def reset(self):
        self.obstacles.clear()
        self.spawn_timer = 0
        self.current_speed = self.base_speed
        self.game_time = 0
        self.obstacles_destroyed_by_dash = 0