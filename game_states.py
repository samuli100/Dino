import pygame
from constants import BLACK, BLUE, GOLD, GRAY, HEIGHT, RED, WHITE, WIDTH, GROUND_Y, BLOCK_SIZE, GREEN
from obstacle import ObstacleManager
from player import Player
from utils import draw_pixel_art
from game_states import GameState, MenuState, GameState_Playing, GameOverState
 

class GameState:
    """Base class for game states"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def handle_event(self, event):
        """Handle events - to be overridden"""
        pass

    def update(self):
        """Update state - to be overridden"""
        pass

    def draw(self, win):
        """Draw state - to be overridden"""
        pass

class MenuState(GameState):
    """Main menu state"""
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "game"
            elif event.key == pygame.K_s:
                return "shop"
        return "menu"

    def draw(self, win):
        win.fill(WHITE)
        
        # Title
        title = self.font.render("CHROME DINO - ENHANCED", True, BLACK)
        win.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Instructions and stats
        instructions = [
            "Press SPACE to Start Game",
            "Press S to Enter Shop",
            "",
            f"Coins: {self.game_manager.save_system.data['coins']}",
            f"High Score: {self.game_manager.save_system.data['high_score']}"
        ]
        
        for i, text in enumerate(instructions):
            if text:
                rendered = self.small_font.render(text, True, BLACK)
                win.blit(rendered, (WIDTH//2 - rendered.get_width()//2, 200 + i * 30))

class GameState_Playing(GameState):
    """Main gameplay state"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.reset_game()

    def reset_game(self):
        """Reset game for new play session"""
        upgrades = self.game_manager.save_system.data["upgrades"]
        self.player = Player(upgrades)
        self.obstacle_manager = ObstacleManager()
        self.score = 0
        self.coins_this_run = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
        return "game"

    def update(self):
        upgrades = self.game_manager.save_system.data["upgrades"]
        
        # Update player
        self.player.update(upgrades)
        
        # Update obstacles
        self.obstacle_manager.update(upgrades)
        
        # Award coins for passed obstacles
        passed_obstacles = self.obstacle_manager.count_passed_obstacles()
        if passed_obstacles > 0:
            coins_earned = passed_obstacles * (1 + upgrades["coin_multiplier"])
            self.coins_this_run += coins_earned
            self.game_manager.save_system.add_coins(coins_earned)
        
        # Update score
        self.score += 1
        
        # Check collisions
        if self.obstacle_manager.check_collisions(self.player):
            return "game_over"
            
        return "game"

    def draw(self, win):
        win.fill(WHITE)
        
        # Draw ground
        pygame.draw.line(win, GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        
        # Draw game objects
        self.player.draw(win)
        self.obstacle_manager.draw(win)
        
        # Draw HUD
        self.draw_hud(win)

    def draw_hud(self, win):
        """Draw heads-up display"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        win.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
        
        # Coins
        coins_text = self.small_font.render(
            f"Coins: {self.game_manager.save_system.data['coins']} (+{self.coins_this_run})", 
            True, GOLD
        )
        win.blit(coins_text, (20, 20))
        
        # Shield status
        if self.player.shield_cooldown > 0:
            cooldown_text = self.small_font.render(f"Shield: {self.player.shield_cooldown//60 + 1}s", True, RED)
            win.blit(cooldown_text, (20, 50))
        elif self.game_manager.save_system.data["upgrades"]["shield"] > 0:
            shield_text = self.small_font.render("Shield: Ready (Press S)", True, BLUE)
            win.blit(shield_text, (20, 50))

class GameOverState(GameState):
    """Game over state"""
    
    def __init__(self, game_manager, final_score, coins_earned):
        super().__init__(game_manager)
        self.final_score = final_score
        self.coins_earned = coins_earned
        self.new_high_score = game_manager.save_system.update_high_score(final_score)
        game_manager.save_system.save_data()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "game"
            elif event.key == pygame.K_m:
                return "menu"
            elif event.key == pygame.K_ESCAPE:
                return "quit"
        return "game_over"

    def draw(self, win):
        win.fill(WHITE)
        
        # Game over text
        game_over_text = self.font.render(f"Game Over! Score: {self.final_score}", True, BLACK)
        win.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
        
        # Coins earned
        coins_text = self.small_font.render(f"Coins Earned This Run: {self.coins_earned}", True, GOLD)
        win.blit(coins_text, (WIDTH//2 - coins_text.get_width()//2, HEIGHT//2 - 40))
        
        # New high score indicator
        if self.new_high_score:
            high_score_text = self.small_font.render("NEW HIGH SCORE!", True, GREEN)
            win.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 - 10))
        
        # Instructions
        restart_text = self.small_font.render("Press R to restart, M for menu, or ESC to quit", True, BLACK)
        win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
