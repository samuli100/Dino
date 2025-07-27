import pygame
import sys
import random
import json
import os

pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue Dino")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (34, 139, 34)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
FPS = 60
GROUND_Y = 350
BLOCK_SIZE = 4

MENU = 0
GAME = 1
SHOP = 2
GAME_OVER = 3

SAVE_FILE = "dino_save.json"

DINO_FRAMES = [
    [
        # Frame 0 - Standing/Running 1
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
    ],
    [
        # Frame 1 - Running 2 (left leg lifted)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
    ],
    [
        # Frame 2 - Running 3 (both legs transition)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
    ],
    [
        # Frame 3 - Running 4 (right leg lifted)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    ]
]

CACTUS_PATTERNS = [
    # Small cactus
    [
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
    ],
    # Tall cactus
    [
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
    ],
    # Wide cactus with multiple arms
    [
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
    ]
]

def draw_pixel_art(win, pattern, top_left_x, top_left_y, color=BLACK):
    for y, row in enumerate(pattern):
        for x, val in enumerate(row):
            if val == 1:
                rect = pygame.Rect(
                    top_left_x + x * BLOCK_SIZE,
                    top_left_y + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                pygame.draw.rect(win, color, rect)

class SaveSystem:
    def __init__(self):
        self.data = {
            "coins": 0,
            "high_score": 0,
            "upgrades": {
                "jump_boost": 0,
                "coin_multiplier": 0,
                "speed_boost": 0,
                "shield": 0,
                "slow_motion": 0
            }
        }
        self.load_save()

    def load_save(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
            except:
                pass

    def save_data(self):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except:
            pass

class Player:
    def __init__(self, upgrades):
        self.x = 100
        self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
        self.vel_y = 0
        self.base_gravity = 0.8
        self.base_jump_force = -15
        self.gravity = self.base_gravity
        self.jump_force = self.base_jump_force - upgrades["jump_boost"] * 2
        self.on_ground = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.shield_active = False
        self.shield_duration = 0
        self.shield_cooldown = 0

    def update(self, upgrades):
        keys = pygame.key.get_pressed()
        
        if self.shield_duration > 0:
            self.shield_duration -= 1
            self.shield_active = True
        else:
            self.shield_active = False
            
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            
        if keys[pygame.K_s] and upgrades["shield"] > 0 and self.shield_cooldown == 0 and not self.shield_active:
            self.shield_duration = 180  
            self.shield_cooldown = 600  

        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y + len(DINO_FRAMES[0]) * BLOCK_SIZE >= GROUND_Y:
            self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
            self.vel_y = 0
            self.on_ground = True

        if self.on_ground:
            self.anim_timer += 1
            if self.anim_timer > 8:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(DINO_FRAMES)

    def get_rect(self):
        width = len(DINO_FRAMES[0][0]) * BLOCK_SIZE
        height = len(DINO_FRAMES[0]) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def draw(self, win):
        color = BLUE if self.shield_active else BLACK
        draw_pixel_art(win, DINO_FRAMES[self.anim_frame], self.x, self.y, color)
        

        if self.shield_active:
            pygame.draw.circle(win, BLUE, (self.x + 32, self.y + 48), 40, 2)

class Cactus:
    def __init__(self, base_speed, slow_motion_level):
        self.pattern = random.choice(CACTUS_PATTERNS)
        self.x = WIDTH
        self.y = GROUND_Y - len(self.pattern) * BLOCK_SIZE
        self.speed = base_speed - slow_motion_level * 0.5

    def update(self):
        self.x -= self.speed

    def get_rect(self):
        width = len(self.pattern[0]) * BLOCK_SIZE
        height = len(self.pattern) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def draw(self, win):
        draw_pixel_art(win, self.pattern, self.x, self.y, GREEN)

class Game:
    def __init__(self):
        self.save_system = SaveSystem()
        self.state = MENU
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset_game()
        

        self.shop_items = {
            "jump_boost": {
                "name": "Jump Boost",
                "description": "Higher jumps",
                "base_cost": 10,
                "unlock_score": 0,
                "max_level": 5
            },
            "coin_multiplier": {
                "name": "Coin Multiplier",
                "description": "2x coins per cactus",
                "base_cost": 25,
                "unlock_score": 100,
                "max_level": 3
            },
            "speed_boost": {
                "name": "Speed Boost",
                "description": "Faster movement",
                "base_cost": 20,
                "unlock_score": 200,
                "max_level": 3
            },
            "shield": {
                "name": "Shield",
                "description": "Press S for protection",
                "base_cost": 50,
                "unlock_score": 500,
                "max_level": 1
            },
            "slow_motion": {
                "name": "Slow Motion",
                "description": "Slower obstacles",
                "base_cost": 75,
                "unlock_score": 750,
                "max_level": 4
            }
        }

    def reset_game(self):
        self.player = Player(self.save_system.data["upgrades"])
        self.obstacles = []
        self.spawn_timer = 0
        self.score = 0
        self.coins_this_run = 0
        self.base_obstacle_speed = 6 + self.save_system.data["upgrades"]["speed_boost"] * 0.5

    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state = GAME
                self.reset_game()
            elif event.key == pygame.K_s:
                self.state = SHOP

    def handle_shop_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                self.state = MENU
            elif event.key >= pygame.K_1 and event.key <= pygame.K_5:
                item_index = event.key - pygame.K_1
                item_names = list(self.shop_items.keys())
                if item_index < len(item_names):
                    self.try_buy_upgrade(item_names[item_index])

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = MENU

    def try_buy_upgrade(self, upgrade_name):
        item = self.shop_items[upgrade_name]
        current_level = self.save_system.data["upgrades"][upgrade_name]
        
        if (self.save_system.data["high_score"] >= item["unlock_score"] and 
            current_level < item["max_level"]):
            
            cost = item["base_cost"] + (current_level * item["base_cost"] // 2)
            
            if self.save_system.data["coins"] >= cost:
                self.save_system.data["coins"] -= cost
                self.save_system.data["upgrades"][upgrade_name] += 1
                self.save_system.save_data()

    def update_game(self):
        self.player.update(self.save_system.data["upgrades"])

        self.spawn_timer += 1
        spawn_interval = random.randint(80, 120)
        if self.spawn_timer >= spawn_interval:
            self.obstacles.append(Cactus(self.base_obstacle_speed, 
                                       self.save_system.data["upgrades"]["slow_motion"]))
            self.spawn_timer = 0

        self.score += 1

        for obs in list(self.obstacles):
            obs.update()
            if obs.x + len(obs.pattern[0]) * BLOCK_SIZE < 0:
                self.obstacles.remove(obs)
                coins_earned = 1 + self.save_system.data["upgrades"]["coin_multiplier"]
                self.coins_this_run += coins_earned
                self.save_system.data["coins"] += coins_earned

            if not self.player.shield_active:
                player_rect = self.player.get_rect()
                obs_rect = obs.get_rect()
                player_rect.inflate_ip(-8, -8)
                obs_rect.inflate_ip(-4, -4)
                
                if player_rect.colliderect(obs_rect):
                    self.game_over()

    def game_over(self):
        if self.score > self.save_system.data["high_score"]:
            self.save_system.data["high_score"] = self.score
        self.save_system.save_data()
        self.state = GAME_OVER

    def draw_menu(self):
        WIN.fill(WHITE)
        
        title = self.font.render("ROGUE DINO", True, BLACK)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        instructions = [
            "Press SPACE to Start Game",
            "Press S to Enter Shop",
            "",
            f"Coins: {self.save_system.data['coins']}",
            f"High Score: {self.save_system.data['high_score']}"
        ]
        
        for i, text in enumerate(instructions):
            if text:
                rendered = self.small_font.render(text, True, BLACK)
                WIN.blit(rendered, (WIDTH//2 - rendered.get_width()//2, 200 + i * 30))

    def draw_shop(self):
        WIN.fill(WHITE)
        
        title = self.font.render(f"SHOP - Coins: {self.save_system.data['coins']}", True, BLACK)
        WIN.blit(title, (50, 30))
        
        instructions = self.small_font.render("keys (1-5) to buy, M  menu", True, BLACK)
        WIN.blit(instructions, (50, 70))
        
        y_pos = 110
        for i, (upgrade_name, item) in enumerate(self.shop_items.items()):
            current_level = self.save_system.data["upgrades"][upgrade_name]
            cost = item["base_cost"] + (current_level * item["base_cost"] // 2)
            
            unlocked = self.save_system.data["high_score"] >= item["unlock_score"]
            maxed = current_level >= item["max_level"]
            
            color = BLACK if unlocked else GRAY
            if maxed:
                color = GREEN
            
            text = f"{i+1}. {item['name']} - Level {current_level}/{item['max_level']}"
            if not unlocked:
                text += f" (Unlock at score {item['unlock_score']})"
            elif maxed:
                text += " (MAXED)"
            else:
                text += f" - Cost: {cost} coins"
            
            rendered = self.small_font.render(text, True, color)
            WIN.blit(rendered, (50, y_pos))
            
            desc = self.small_font.render(f"   {item['description']}", True, GRAY)
            WIN.blit(desc, (50, y_pos + 20))
            
            y_pos += 50

    def draw_game(self):
        WIN.fill(WHITE)
        
        pygame.draw.line(WIN, GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        
        self.player.draw(WIN)
        
        for obs in self.obstacles:
            obs.draw(WIN)
        
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        WIN.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
        
        coins_text = self.small_font.render(f"Coins: {self.save_system.data['coins']} (+{self.coins_this_run})", True, GOLD)
        WIN.blit(coins_text, (20, 20))
        
        if self.player.shield_cooldown > 0:
            cooldown_text = self.small_font.render(f"Shield: {self.player.shield_cooldown//60 + 1}s", True, RED)
            WIN.blit(cooldown_text, (20, 50))
        elif self.save_system.data["upgrades"]["shield"] > 0:
            shield_text = self.small_font.render("Shield: Ready (Press S)", True, BLUE)
            WIN.blit(shield_text, (20, 50))

    def draw_game_over(self):
        WIN.fill(WHITE)
        
        game_over_text = self.font.render(f"Game Over! Score: {self.score}", True, BLACK)
        WIN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
        
        coins_earned = self.small_font.render(f"Coins Earned This Run: {self.coins_this_run}", True, GOLD)
        WIN.blit(coins_earned, (WIDTH//2 - coins_earned.get_width()//2, HEIGHT//2 - 40))
        
        if self.score == self.save_system.data["high_score"]:
            new_high = self.small_font.render("NEW HIGH SCORE!", True, GREEN)
            WIN.blit(new_high, (WIDTH//2 - new_high.get_width()//2, HEIGHT//2 - 10))
        
        restart_text = self.small_font.render("Press R to restart, M for menu, or ESC to quit", True, BLACK)
        WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.state = GAME
            self.reset_game()
        elif keys[pygame.K_m]:
            self.state = MENU
        elif keys[pygame.K_ESCAPE]:
            return False
        
        return True

    def run(self):
        run = True
        while run:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if self.state == MENU:
                    self.handle_menu_events(event)
                elif self.state == SHOP:
                    self.handle_shop_events(event)
                elif self.state == GAME:
                    self.handle_game_events(event)
            
            if self.state == MENU:
                self.draw_menu()
            elif self.state == SHOP:
                self.draw_shop()
            elif self.state == GAME:
                self.update_game()
                self.draw_game()
            elif self.state == GAME_OVER:
                if not self.draw_game_over():
                    run = False
            
            pygame.display.update()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()