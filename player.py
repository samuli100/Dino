import pygame
import random
from constants import VERY_DARK, DARK_GRAY, GROUND_Y, BLOCK_SIZE, DINO_FRAMES, DINO, SHIELD_PATTERNS
from utils import draw_pixel_art


class Player:
    """Player character with movement, animation, and abilities"""
    
    def __init__(self, upgrades):
        self.x = 100
        self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
        self.vel_y = 0
        
        # Base physics values
        self.base_gravity = 0.8
        self.base_jump_force = -15
        
        # Apply upgrades - balanced jump scaling
        self.gravity = self.base_gravity
        # Jump boost: 0 upgrades = 1x, 5 upgrades = 1.5x (much more balanced)
        jump_multiplier = 1.0 + (upgrades["jump_boost"] * 0.1)  # 0.1 per level = 0.5x total increase
        self.jump_force = self.base_jump_force * jump_multiplier
        
        # Air abilities
        self.air_jump_used = False
        self.air_dash_used = False
        self.dash_velocity = 0
        self.dash_duration = 0
        self.returning_to_start = False  # New state for post-dash return
        self.start_x = 100  # Starting position to return to
        
        # State
        self.on_ground = True
        self.anim_frame = 0
        self.anim_timer = 0
        
        # Health system
        self.max_health = 1 + upgrades["bonus_health"]
        self.current_health = self.max_health
        self.invulnerable_timer = 0  # Invulnerability frames after taking damage
        
        # Shield system with upgrades
        self.shield_active = False
        self.shield_duration = 0
        self.shield_cooldown = 0
        
        # Base shield values
        base_duration = 120  # 2 seconds
        base_cooldown = 900  # 15 seconds
        
        # Apply shield upgrades
        shield_level = upgrades["shield_upgrade"]
        self.max_shield_duration = base_duration + (shield_level * 30)  # +0.5s per level, max 4.5s
        self.max_shield_cooldown = base_cooldown - (shield_level * 150)  # -2.5s per level, min 10s
        self.max_shield_cooldown = max(600, self.max_shield_cooldown)  # Minimum 10 seconds

class Player:
    """Player character with movement, animation, and abilities"""
    
    def __init__(self, upgrades):
        self.x = 100
        self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
        self.vel_y = 0
        
        # Base physics values
        self.base_gravity = 0.8
        self.base_jump_force = -15
        
        # Apply upgrades - more conservative jump scaling
        self.gravity = self.base_gravity
        jump_multiplier = 1.0 + (upgrades["jump_boost"] * 0.04)  # 0.05 per level = 0.25x total increase
        self.jump_force = self.base_jump_force * jump_multiplier
        
        # Air abilities
        self.air_jump_used = False
        self.air_dash_used = False
        self.dash_velocity = 0
        self.dash_duration = 0
        
        # State
        self.on_ground = True
        self.anim_frame = 0
        self.anim_timer = 0
        
        # Input tracking for single-press detection
        self.prev_space = False
        self.prev_s = False
        self.prev_d = False
        
        # Health system
        self.max_health = 1 + upgrades["bonus_health"]
        self.current_health = self.max_health
        self.invulnerable_timer = 0  # Invulnerability frames after taking damage
        
        # Shield system with upgrades
        self.shield_active = False
        self.shield_duration = 0
        self.shield_cooldown = 0
        
        # Base shield values
        base_duration = 120  # 2 seconds
        base_cooldown = 900  # 15 seconds
        
        # Apply shield upgrades
        shield_level = upgrades["shield_upgrade"]
        self.max_shield_duration = base_duration + (shield_level * 30)  # +0.5s per level, max 4.5s
        self.max_shield_cooldown = base_cooldown - (shield_level * 150)  # -2.5s per level, min 10s
        self.max_shield_cooldown = max(600, self.max_shield_cooldown)  # Minimum 10 seconds

    def handle_input(self, keys, upgrades):
        """Handle player input"""
        # Detect key presses (was up, now down)
        space_pressed = keys[pygame.K_SPACE] and not self.prev_space
        s_pressed = keys[pygame.K_s] and not self.prev_s
        d_pressed = keys[pygame.K_d] and not self.prev_d
        
        # Jump
        if space_pressed and self.on_ground:
            self.jump()
        
        # Air jump (small jump, not affected by jump boost)
        elif (space_pressed and not self.on_ground and 
              not self.air_jump_used and upgrades["air_jump"] > 0):
            self.air_jump()
            
        # Shield activation
        if (s_pressed and upgrades["shield"] > 0 and 
            self.shield_cooldown == 0 and not self.shield_active):
            self.activate_shield()
            
        # Air dash
        if (d_pressed and not self.on_ground and 
            not self.air_dash_used and upgrades["air_dash"] > 0):
            self.air_dash(upgrades)
            
        # Update previous key states
        self.prev_space = keys[pygame.K_SPACE]
        self.prev_s = keys[pygame.K_s]
        self.prev_d = keys[pygame.K_d]

    def jump(self):
        """Make the player jump"""
        self.vel_y = self.jump_force
        self.on_ground = False
        self.air_jump_used = False  # Reset air abilities
        self.air_dash_used = False

    def air_jump(self):
        """Small air jump not affected by jump boost"""
        self.vel_y = -8  # Fixed small jump
        self.air_jump_used = True

    def air_dash(self, upgrades):
        """Horizontal air dash"""
        base_dash = 12
        dash_bonus = upgrades["dash_distance"] * 3  # 3 units per upgrade
        self.dash_velocity = base_dash + dash_bonus
        self.dash_duration = 15  # Frames
        self.air_dash_used = True

    def activate_shield(self):
        """Activate shield protection"""
        self.shield_duration = self.max_shield_duration
        self.shield_cooldown = self.max_shield_cooldown

    def get_shield_stage(self):
        """Get the current shield visual stage based on remaining duration"""
        if not self.shield_active:
            return -1
        
        ratio = self.shield_duration / self.max_shield_duration
        if ratio > 0.66:
            return 0  # Intact shield
        elif ratio > 0.33:
            return 1  # Slightly cracked
        else:
            return 2  # Very cracked

    def take_damage(self, upgrades):
        """Take damage with dodge chance"""
        if self.invulnerable_timer > 0 or self.shield_active:
            return False
            
        # Check dodge chance
        dodge_level = upgrades["dodge_chance"]
        dodge_chance = dodge_level * 5  # 5% per level, max 25%
        
        if random.randint(1, 100) <= dodge_chance:
            return False  # Dodged!
            
        # Take damage
        self.current_health -= 1
        self.invulnerable_timer = 120  # 2 seconds of invulnerability
        
        return self.current_health <= 0  # Return True if dead

    def update(self, upgrades, obstacle_speed=6):
        """Update player physics and animation"""
        keys = pygame.key.get_pressed()
        
        self.handle_input(keys, upgrades)
        
        # Update timers
        self.update_shield()
        self.update_invulnerability()
        self.update_dash(obstacle_speed)
        
        # Physics
        self.update_physics()
        
        # Animation
        self.update_animation()

    def update_shield(self):
        """Update shield status"""
        if self.shield_duration > 0:
            self.shield_duration -= 1
            self.shield_active = True
        else:
            self.shield_active = False
            
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

    def update_invulnerability(self):
        """Update invulnerability frames"""
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def update_dash(self, obstacle_speed=6):
        """Update air dash and return to start position"""
        if not hasattr(self, 'returning_to_start'):
            self.returning_to_start = False
        if not hasattr(self, 'start_x'):
            self.start_x = 100
            
        if self.dash_duration > 0:
            self.x += self.dash_velocity
            self.dash_duration -= 1
            # Prevent going off screen
            if self.x > 750:
                self.x = 750
            
            # When dash ends, start returning to start position if we're ahead
            if self.dash_duration == 0 and self.x > self.start_x:
                self.returning_to_start = True
        
        # Return to starting position after dash
        if self.returning_to_start:
            if self.x > self.start_x:
                # Move back at current obstacle speed
                self.x -= obstacle_speed
                
                # Stop when we reach starting position
                if self.x <= self.start_x:
                    self.x = self.start_x
                    self.returning_to_start = False

    def update_physics(self):
        """Update player physics"""
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Ground collision
        if self.y + len(DINO_FRAMES[0]) * BLOCK_SIZE >= GROUND_Y:
            self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
            self.vel_y = 0
            self.on_ground = True
            self.air_jump_used = False  # Reset air abilities when landing
            self.air_dash_used = False
            # Don't reset returning_to_start here - let it finish naturally

        # Prevent going too high
        if self.y < 50:
            self.y = 50
            self.vel_y = 0

    def update_animation(self):
        """Update running animation"""
        # Ensure attribute exists (backward compatibility)
        if not hasattr(self, 'returning_to_start'):
            self.returning_to_start = False
            
        # Don't animate while returning to start position
        if self.returning_to_start:
            return
            
        if self.on_ground:
            self.anim_timer += 1
            if self.anim_timer > 8:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(DINO_FRAMES)

    def get_rect(self):
        """Get collision rectangle"""
        width = len(DINO_FRAMES[0][0]) * BLOCK_SIZE
        height = len(DINO_FRAMES[0]) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def get_collision_rect(self):
        """Get smaller collision rectangle for more forgiving gameplay"""
        rect = self.get_rect()
        rect.inflate_ip(-8, -8)
        return rect

    def draw(self, win):
        """Draw the player"""
        # Flashing effect when invulnerable
        if self.invulnerable_timer > 0 and self.invulnerable_timer % 10 < 5:
            return  # Skip drawing for flashing effect
        
        # Choose the right frame to draw
        # Ensure attribute exists and DINO is defined (backward compatibility)
        if (hasattr(self, 'returning_to_start') and self.returning_to_start and 
            'DINO' in globals() and DINO):
            # Use standing frame when returning to start position
            dino_frame = DINO[0]
        else:
            # Use normal running animation
            dino_frame = DINO_FRAMES[self.anim_frame]
            
        # Draw dino in dark gray
        draw_pixel_art(win, dino_frame, self.x, self.y, VERY_DARK)
        
        # Draw shield if active (OVER the dino)
        if self.shield_active:
            shield_stage = self.get_shield_stage()
            if shield_stage >= 0:
                # Position shield to cover the dino body
                shield_x = self.x + 8
                shield_y = self.y + 15
                draw_pixel_art(win, SHIELD_PATTERNS[shield_stage], shield_x, shield_y, DARK_GRAY)