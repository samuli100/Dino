import pygame
from constants import BLACK, BLUE, GROUND_Y, BLOCK_SIZE, DINO_FRAMES
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
        
        # Apply upgrades
        self.gravity = self.base_gravity
        self.jump_force = self.base_jump_force - upgrades["jump_boost"] * 2
        
        # State
        self.on_ground = True
        self.anim_frame = 0
        self.anim_timer = 0
        
        # Shield system
        self.shield_active = False
        self.shield_duration = 0
        self.shield_cooldown = 0

    def handle_input(self, keys, upgrades):
        """Handle player input"""
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            
        # Shield activation
        if (keys[pygame.K_s] and upgrades["shield"] > 0 and 
            self.shield_cooldown == 0 and not self.shield_active):
            self.activate_shield()

    def jump(self):
        """Make the player jump"""
        self.vel_y = self.jump_force
        self.on_ground = False

    def activate_shield(self):
        """Activate shield protection"""
        self.shield_duration = 180  # 3 seconds at 60 FPS
        self.shield_cooldown = 600   # 10 seconds cooldown

    def update(self, upgrades):
        """Update player physics and animation"""
        keys = pygame.key.get_pressed()
        self.handle_input(keys, upgrades)
        
        # Update shield
        self.update_shield()
        
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

    def update_physics(self):
        """Update player physics"""
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Ground collision
        if self.y + len(DINO_FRAMES[0]) * BLOCK_SIZE >= GROUND_Y:
            self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
            self.vel_y = 0
            self.on_ground = True

    def update_animation(self):
        """Update running animation"""
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
        color = BLUE if self.shield_active else BLACK
        draw_pixel_art(win, DINO_FRAMES[self.anim_frame], self.x, self.y, color)
        
        # Draw shield indicator
        if self.shield_active:
            pygame.draw.circle(win, BLUE, (self.x + 32, self.y + 48), 40, 2)