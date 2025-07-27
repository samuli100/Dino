import pygame
from constants import (UI_TEXT, UI_ACCENT, GRAY, DARK_GRAY, HEIGHT, WHITE, WIDTH, GROUND_Y, 
                      UI_BACKGROUND, MEDIUM_GRAY, LIGHT_GRAY)
from obstacle import ObstacleManager
from player import Player
from background_system import BackgroundManager


class GameState:
    """Base class for game states"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)

    def handle_event(self, event):
        """Handle events - to be overridden"""
        return None

    def update(self):
        """Update state - to be overridden"""
        return None

    def draw(self, win):
        """Draw state - to be overridden"""
        pass


class MenuState(GameState):
    """Main menu state"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.background = BackgroundManager()
    
    def update(self):
        """Update menu background"""
        self.background.update()
        return None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "game"
            elif event.key == pygame.K_s:
                return "shop"
        return None

    def draw(self, win):
        # Sky gradient background
        win.fill(WHITE)
        
        # Draw background elements
        self.background.draw(win)
        
        # Draw ground
        pygame.draw.line(win, MEDIUM_GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        
        # Main title box
        title_box_width = 600
        title_box_height = 200
        title_box_x = (WIDTH - title_box_width) // 2
        title_box_y = 80
        
        # Title background
        pygame.draw.rect(win, WHITE, (title_box_x, title_box_y, title_box_width, title_box_height))
        pygame.draw.rect(win, GRAY, (title_box_x, title_box_y, title_box_width, title_box_height), 3)
        
        # Game title
        title = self.title_font.render("CHROME DINO", True, UI_TEXT)
        subtitle = self.font.render("Enhanced Edition", True, UI_ACCENT)
        
        title_rect = title.get_rect(center=(WIDTH//2, title_box_y + 50))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, title_box_y + 90))
        
        win.blit(title, title_rect)
        win.blit(subtitle, subtitle_rect)
        
        # Controls
        controls = [
            ("SPACE", "Start Game"),
            ("S", "Shop")
        ]
        
        y_offset = title_box_y + 130
        for key, action in controls:
            key_text = self.small_font.render(f"[{key}]", True, DARK_GRAY)
            action_text = self.small_font.render(action, True, UI_TEXT)
            
            key_width = key_text.get_width()
            total_width = key_width + 10 + action_text.get_width()
            start_x = (WIDTH - total_width) // 2
            
            win.blit(key_text, (start_x, y_offset))
            win.blit(action_text, (start_x + key_width + 10, y_offset))
            y_offset += 25
        
        # Stats box
        stats_box_width = 400
        stats_box_height = 100
        stats_box_x = (WIDTH - stats_box_width) // 2
        stats_box_y = 300
        
        pygame.draw.rect(win, UI_BACKGROUND, (stats_box_x, stats_box_y, stats_box_width, stats_box_height))
        pygame.draw.rect(win, GRAY, (stats_box_x, stats_box_y, stats_box_width, stats_box_height), 2)
        
        # Stats
        coins_text = f"Coins: {self.game_manager.save_system.data['coins']}"
        score_text = f"High Score: {self.game_manager.save_system.data['high_score']}"
        
        coins_surface = self.small_font.render(coins_text, True, UI_ACCENT)
        score_surface = self.small_font.render(score_text, True, UI_TEXT)
        
        win.blit(coins_surface, (stats_box_x + 20, stats_box_y + 25))
        win.blit(score_surface, (stats_box_x + 20, stats_box_y + 50))


class GameState_Playing(GameState):
    """Main gameplay state"""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.background = BackgroundManager()
        self.reset_game()

    def reset_game(self):
        """Reset game for new play session"""
        upgrades = self.game_manager.save_system.data["upgrades"]
        self.player = Player(upgrades)
        self.obstacle_manager = ObstacleManager()
        self.background.reset()
        self.score = 0
        self.coins_this_run = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
        return None

    def update(self):
        upgrades = self.game_manager.save_system.data["upgrades"]
        
        # Update background
        self.background.update()
        
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
            
        return None

    def draw(self, win):
        # Sky background
        win.fill(WHITE)
        
        # Draw background elements
        self.background.draw(win)
        
        # Draw ground line
        pygame.draw.line(win, MEDIUM_GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        
        # Draw game objects
        self.player.draw(win)
        self.obstacle_manager.draw(win)
        
        # Draw HUD
        self.draw_hud(win)

    def draw_hud(self, win):
        """Draw heads-up display"""
        # HUD background panel
        hud_height = 80
        pygame.draw.rect(win, UI_BACKGROUND, (0, 0, WIDTH, hud_height))
        pygame.draw.line(win, GRAY, (0, hud_height), (WIDTH, hud_height), 1)
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, UI_TEXT)
        win.blit(score_text, (WIDTH - score_text.get_width() - 20, 15))
        
        # Coins
        coins_text = self.small_font.render(
            f"Coins: {self.game_manager.save_system.data['coins']} (+{self.coins_this_run})", 
            True, UI_ACCENT
        )
        win.blit(coins_text, (20, 15))
        
        # Shield status
        if self.player.shield_cooldown > 0:
            cooldown_seconds = self.player.shield_cooldown // 60 + 1
            cooldown_text = self.small_font.render(f"Shield: {cooldown_seconds}s cooldown", True, GRAY)
            win.blit(cooldown_text, (20, 40))
        elif self.game_manager.save_system.data["upgrades"]["shield"] > 0:
            shield_text = self.small_font.render("Shield: Ready [S]", True, DARK_GRAY)
            win.blit(shield_text, (20, 40))
        
        # Controls hint
        controls_text = self.tiny_font.render("SPACE: Jump • S: Shield • ESC: Menu", True, GRAY)
        win.blit(controls_text, (WIDTH - controls_text.get_width() - 20, 55))


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
        return None

    def draw(self, win):
        win.fill(UI_BACKGROUND)
        
        # Game over box
        box_width = 500
        box_height = 300
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        
        pygame.draw.rect(win, WHITE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(win, GRAY, (box_x, box_y, box_width, box_height), 3)
        
        # Game over title
        if self.new_high_score:
            title_text = "NEW HIGH SCORE!"
            title_color = DARK_GRAY
        else:
            title_text = "GAME OVER"
            title_color = UI_TEXT
            
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(WIDTH//2, box_y + 50))
        win.blit(title_surface, title_rect)
        
        # Score
        score_text = f"Final Score: {self.final_score}"
        score_surface = self.font.render(score_text, True, UI_TEXT)
        score_rect = score_surface.get_rect(center=(WIDTH//2, box_y + 100))
        win.blit(score_surface, score_rect)
        
        # Coins earned
        coins_text = f"Coins Earned: {self.coins_earned}"
        coins_surface = self.small_font.render(coins_text, True, UI_ACCENT)
        coins_rect = coins_surface.get_rect(center=(WIDTH//2, box_y + 140))
        win.blit(coins_surface, coins_rect)
        
        # Controls
        controls = [
            ("R", "Restart"),
            ("M", "Menu"),
            ("ESC", "Quit")
        ]
        
        y_offset = box_y + 190
        for key, action in controls:
            key_text = self.small_font.render(f"[{key}]", True, DARK_GRAY)
            action_text = self.small_font.render(action, True, UI_TEXT)
            
            key_width = key_text.get_width()
            total_width = key_width + 10 + action_text.get_width()
            start_x = (WIDTH - total_width) // 2
            
            win.blit(key_text, (start_x, y_offset))
            win.blit(action_text, (start_x + key_width + 10, y_offset))
            y_offset += 25