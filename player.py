import pygame
import random
from constants import GROUND_Y, BLOCK_SIZE, DINO_FRAMES, DINO, SHIELD_PATTERNS, get_color
from utils import draw_pixel_art


class Player:
    def __init__(self, upgrades, settings_system=None):
        self.settings_system = settings_system
        self.x = 100
        self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
        self.vel_y = 0
        
        self.base_gravity = 0.8
        self.base_jump_force = -15
        
        self.gravity = self.base_gravity
        jump_multiplier = 1.0 + (upgrades["jump_boost"] * 0.04)
        self.jump_force = self.base_jump_force * jump_multiplier
        
        self.air_jump_used = False
        self.air_dash_used = False
        self.dash_velocity = 0
        self.dash_duration = 0
        self.dash_cooldown = 0
        self.max_dash_cooldown = 300
        self.returning_to_start = False
        self.start_x = 100
        
        self.on_ground = True
        self.anim_frame = 0
        self.anim_timer = 0
        
        self.prev_space = False
        self.prev_s = False
        self.prev_d = False
        
        self.prev_keys = {}
        
        self.max_health = 1 + upgrades["bonus_health"]
        self.current_health = self.max_health
        self.invulnerable_timer = 0
        
        self.shield_active = False
        self.shield_duration = 0
        self.shield_cooldown = 0
        
        base_duration = 120
        base_cooldown = 900
        
        shield_level = upgrades["shield_upgrade"]
        self.max_shield_duration = base_duration + (shield_level * 30)
        self.max_shield_cooldown = base_cooldown - (shield_level * 150)
        self.max_shield_cooldown = max(600, self.max_shield_cooldown)

    def get_keybind(self, action):
        if self.settings_system:
            return self.settings_system.get_keybind(action)
        else:
            defaults = {
                "jump": pygame.K_SPACE,
                "shield": pygame.K_s,
                "dash": pygame.K_d
            }
            return defaults.get(action, pygame.K_UNKNOWN)

    def is_key_pressed(self, keys, action):
        key = self.get_keybind(action)
        if key == pygame.K_UNKNOWN:
            return False
        
        current_pressed = keys[key]
        prev_pressed = self.prev_keys.get(key, False)
        
        return current_pressed and not prev_pressed

    def handle_input(self, keys, upgrades):
        if self.settings_system:
            jump_pressed = self.is_key_pressed(keys, "jump")
            shield_pressed = self.is_key_pressed(keys, "shield")
            dash_pressed = self.is_key_pressed(keys, "dash")
        else:
            jump_pressed = keys[pygame.K_SPACE] and not self.prev_space
            shield_pressed = keys[pygame.K_s] and not self.prev_s
            dash_pressed = keys[pygame.K_d] and not self.prev_d
        
        if jump_pressed and self.on_ground:
            self.jump()
        
        elif (jump_pressed and not self.on_ground and 
              not self.air_jump_used and upgrades["air_jump"] > 0):
            self.air_jump()
            
        if (shield_pressed and upgrades["shield"] > 0 and 
            self.shield_cooldown == 0 and not self.shield_active):
            self.activate_shield()
            
        if (dash_pressed and not self.on_ground and 
            not self.air_dash_used and upgrades["air_dash"] > 0 and
            self.dash_cooldown == 0):
            self.air_dash(upgrades)
        
        if self.settings_system:
            for action in ["jump", "shield", "dash"]:
                key = self.get_keybind(action)
                if key != pygame.K_UNKNOWN:
                    self.prev_keys[key] = keys[key]
        else:
            self.prev_space = keys[pygame.K_SPACE]
            self.prev_s = keys[pygame.K_s]
            self.prev_d = keys[pygame.K_d]

    def jump(self):
        self.vel_y = self.jump_force
        self.on_ground = False
        self.air_jump_used = False
        self.air_dash_used = False

    def air_jump(self):
        self.vel_y = -8
        self.air_jump_used = True

    def air_dash(self, upgrades):
        base_dash = 12
        dash_bonus = upgrades["dash_distance"] * 3
        self.dash_velocity = base_dash + dash_bonus
        self.dash_duration = 15
        self.air_dash_used = True
        self.dash_cooldown = self.max_dash_cooldown

    def activate_shield(self):
        self.shield_duration = self.max_shield_duration
        self.shield_cooldown = self.max_shield_cooldown

    def get_shield_stage(self):
        if not self.shield_active:
            return -1
        
        ratio = self.shield_duration / self.max_shield_duration
        if ratio > 0.66:
            return 0
        elif ratio > 0.33:
            return 1
        else:
            return 2

    def is_dashing(self):
        return self.dash_duration > 0 or self.returning_to_start

    def take_damage(self, upgrades):
        if self.invulnerable_timer > 0 or self.shield_active or self.is_dashing():
            return False
            
        dodge_level = upgrades["dodge_chance"]
        dodge_chance = dodge_level * 5
        
        if random.randint(1, 100) <= dodge_chance:
            return False
            
        self.current_health -= 1
        self.invulnerable_timer = 120
        
        return self.current_health <= 0

    def update(self, upgrades, obstacle_speed=6):
        keys = pygame.key.get_pressed()
        
        self.handle_input(keys, upgrades)
        
        self.update_shield()
        self.update_invulnerability()
        self.update_dash_cooldown()
        self.update_dash(obstacle_speed)
        
        self.update_physics()
        self.update_animation()

    def update_shield(self):
        if self.shield_duration > 0:
            self.shield_duration -= 1
            self.shield_active = True
        else:
            self.shield_active = False
            
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

    def update_invulnerability(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def update_dash_cooldown(self):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

    def update_dash(self, obstacle_speed=6):
        if not hasattr(self, 'returning_to_start'):
            self.returning_to_start = False
        if not hasattr(self, 'start_x'):
            self.start_x = 100
            
        if self.dash_duration > 0:
            self.x += self.dash_velocity
            self.dash_duration -= 1
            if self.x > 750:
                self.x = 750
            
            if self.dash_duration == 0 and self.x > self.start_x:
                self.returning_to_start = True
        
        if self.returning_to_start:
            if self.x > self.start_x:
                self.x -= obstacle_speed
                
                if self.x <= self.start_x:
                    self.x = self.start_x
                    self.returning_to_start = False

    def update_physics(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y + len(DINO_FRAMES[0]) * BLOCK_SIZE >= GROUND_Y:
            self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
            self.vel_y = 0
            self.on_ground = True
            self.air_jump_used = False
            self.air_dash_used = False

        if self.y < 50:
            self.y = 50
            self.vel_y = 0

    def update_animation(self):
        if not hasattr(self, 'returning_to_start'):
            self.returning_to_start = False
            
        if self.returning_to_start:
            return
            
        if self.on_ground:
            self.anim_timer += 1
            if self.anim_timer > 8:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(DINO_FRAMES)

    def get_rect(self):
        width = len(DINO_FRAMES[0][0]) * BLOCK_SIZE
        height = len(DINO_FRAMES[0]) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def get_collision_rect(self):
        rect = self.get_rect()
        rect.inflate_ip(-8, -8)
        return rect

    def draw(self, win):
        if self.invulnerable_timer > 0 and self.invulnerable_timer % 10 < 5:
            return
        
        if (hasattr(self, 'returning_to_start') and self.returning_to_start and 
            'DINO' in globals() and DINO):
            dino_frame = DINO[0]
        else:
            dino_frame = DINO_FRAMES[self.anim_frame]
            
        if self.is_dashing():
            draw_pixel_art(win, dino_frame, self.x, self.y, get_color("DARK_GRAY"))
        else:
            draw_pixel_art(win, dino_frame, self.x, self.y, get_color("VERY_DARK"))
        
        if self.shield_active:
            shield_stage = self.get_shield_stage()
            if shield_stage >= 0:
                shield_x = self.x + 8
                shield_y = self.y + 15
                draw_pixel_art(win, SHIELD_PATTERNS[shield_stage], shield_x, shield_y, get_color("DARK_GRAY"))