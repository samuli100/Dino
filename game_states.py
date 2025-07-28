import pygame
from constants import (UI_TEXT, UI_ACCENT, GRAY, DARK_GRAY, HEIGHT, WHITE, WIDTH, GROUND_Y, 
                      UI_BACKGROUND, MEDIUM_GRAY, LIGHT_GRAY)
from obstacle import ObstacleManager
from player import Player
from background_system import BackgroundManager


class GameState:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)

    def handle_event(self, event):
        return None

    def update(self):
        return None

    def draw(self, win):
        pass


class MenuState(GameState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.background = BackgroundManager()
    
    def update(self):
        self.background.update()
        return None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "game"
            elif event.key == pygame.K_s:
                return "shop"
        return None

    def format_number(self, num):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}k"
        else:
            return str(num)

    def draw(self, win):
        win.fill(WHITE)
        
        self.background.draw(win)
        
        pygame.draw.line(win, MEDIUM_GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        
        title_box_width = 600
        title_box_height = 220
        title_box_x = (WIDTH - title_box_width) // 2
        title_box_y = 80
        
        pygame.draw.rect(win, WHITE, (title_box_x, title_box_y, title_box_width, title_box_height))
        pygame.draw.rect(win, GRAY, (title_box_x, title_box_y, title_box_width, title_box_height), 3)
        
        title = self.title_font.render("ROGUE DINO", True, UI_TEXT)
        subtitle = self.font.render("by samuli100", True, UI_ACCENT)
        
        title_rect = title.get_rect(center=(WIDTH//2, title_box_y + 50))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, title_box_y + 90))
        
        win.blit(title, title_rect)
        win.blit(subtitle, subtitle_rect)
        
        score_mult = self.game_manager.save_system.get_score_multiplier()
        if score_mult > 1:
            mult_text = f"{score_mult}x Score Multiplier Active!"
            mult_surface = self.small_font.render(mult_text, True, DARK_GRAY)
            mult_rect = mult_surface.get_rect(center=(WIDTH//2, title_box_y + 120))
            win.blit(mult_surface, mult_rect)
        
        controls = [
            ("SPACE", "Start Game"),
            ("S", "Shop")
        ]
        
        y_offset = title_box_y + 150
        for key, action in controls:
            key_text = self.small_font.render(f"[{key}]", True, DARK_GRAY)
            action_text = self.small_font.render(action, True, UI_TEXT)
            
            key_width = key_text.get_width()
            total_width = key_width + 10 + action_text.get_width()
            start_x = (WIDTH - total_width) // 2
            
            win.blit(key_text, (start_x, y_offset))
            win.blit(action_text, (start_x + key_width + 10, y_offset))
            y_offset += 25
        
        stats_box_width = 400
        stats_box_height = 100
        stats_box_x = (WIDTH - stats_box_width) // 2
        stats_box_y = 320
        
        pygame.draw.rect(win, UI_BACKGROUND, (stats_box_x, stats_box_y, stats_box_width, stats_box_height))
        pygame.draw.rect(win, GRAY, (stats_box_x, stats_box_y, stats_box_width, stats_box_height), 2)
        
        coins_text = f"Coins: {self.format_number(self.game_manager.save_system.data['coins'])}"
        score_text = f"High Score: {self.format_number(self.game_manager.save_system.data['high_score'])}"
        
        coins_surface = self.small_font.render(coins_text, True, UI_ACCENT)
        score_surface = self.small_font.render(score_text, True, UI_TEXT)
        
        win.blit(coins_surface, (stats_box_x + 20, stats_box_y + 25))
        win.blit(score_surface, (stats_box_x + 20, stats_box_y + 50))


class GameState_Playing(GameState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.background = BackgroundManager()
        self.reset_game()

    def reset_game(self):
        upgrades = self.game_manager.save_system.data["upgrades"]
        self.player = Player(upgrades)
        self.obstacle_manager = ObstacleManager()
        self.background.reset()
        self.base_score = 0
        self.score = 0
        self.coins_this_run = 0
        self.dodge_notification_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
        return None

    def update(self):
        upgrades = self.game_manager.save_system.data["upgrades"]
        
        self.background.update()
        
        self.obstacle_manager.update(upgrades)
        
        self.player.update(upgrades, self.obstacle_manager.current_speed)
        
        passed_obstacles = self.obstacle_manager.count_passed_obstacles()
        if passed_obstacles > 0:
            coins_earned = passed_obstacles * (1 + upgrades["coin_multiplier"])
            self.coins_this_run += coins_earned
            self.game_manager.save_system.add_coins(coins_earned)
        
        self.base_score += 1
        
        score_multiplier = self.game_manager.save_system.get_score_multiplier()
        self.score = self.base_score * score_multiplier
        
        if self.obstacle_manager.check_collisions(self.player, upgrades):
            return "game_over"
        
        if self.dodge_notification_timer > 0:
            self.dodge_notification_timer -= 1
            
        return None

    def format_number(self, num):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}k"
        else:
            return str(num)

    def draw(self, win):
        win.fill(WHITE)
        
        self.background.draw(win)
        
        pygame.draw.line(win, MEDIUM_GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        
        self.player.draw(win)
        self.obstacle_manager.draw(win)
        
        self.draw_hud(win)
        
        if self.dodge_notification_timer > 0:
            dodge_text = self.font.render("LUCKY DODGE!", True, DARK_GRAY)
            dodge_rect = dodge_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            win.blit(dodge_text, dodge_rect)

    def draw_hud(self, win):
        upgrades = self.game_manager.save_system.data["upgrades"]
        
        hud_height = 100
        pygame.draw.rect(win, UI_BACKGROUND, (0, 0, WIDTH, hud_height))
        pygame.draw.line(win, GRAY, (0, hud_height), (WIDTH, hud_height), 1)
        
        score_multiplier = self.game_manager.save_system.get_score_multiplier()
        if score_multiplier > 1:
            score_text = f"Score: {self.format_number(self.score)} ({score_multiplier}x)"
        else:
            score_text = f"Score: {self.format_number(self.score)}"
        
        score_surface = self.font.render(score_text, True, UI_TEXT)
        win.blit(score_surface, (WIDTH - score_surface.get_width() - 20, 15))
        
        coins_text = self.small_font.render(
            f"Coins: {self.format_number(self.game_manager.save_system.data['coins'])} (+{self.coins_this_run})", 
            True, UI_ACCENT
        )
        win.blit(coins_text, (20, 15))
        
        if upgrades["bonus_health"] > 0:
            health_text = f"Health: {self.player.current_health}/{self.player.max_health}"
            health_surface = self.small_font.render(health_text, True, UI_TEXT)
            win.blit(health_surface, (20, 40))
        
        if self.player.shield_cooldown > 0:
            cooldown_seconds = self.player.shield_cooldown // 60 + 1
            cooldown_text = self.small_font.render(f"Shield: {cooldown_seconds}s cooldown", True, GRAY)
            win.blit(cooldown_text, (20, 65))
        elif upgrades["shield"] > 0:
            shield_text = self.small_font.render("Shield: Ready [S]", True, DARK_GRAY)
            win.blit(shield_text, (20, 65))
        
        speed_text = f"Speed: {self.obstacle_manager.current_speed:.1f}"
        speed_surface = self.tiny_font.render(speed_text, True, GRAY)
        win.blit(speed_surface, (WIDTH - speed_surface.get_width() - 20, 45))
        
        hud_y = 40
        if upgrades["air_jump"] > 0:
            air_jump_color = GRAY if self.player.air_jump_used else DARK_GRAY
            air_jump_text = "Air Jump: Used" if self.player.air_jump_used else "Air Jump: Ready"
            air_jump_surface = self.tiny_font.render(air_jump_text, True, air_jump_color)
            win.blit(air_jump_surface, (200, hud_y))
            hud_y += 15
            
        if upgrades["air_dash"] > 0:
            if self.player.dash_cooldown > 0:
                cooldown_seconds = (self.player.dash_cooldown // 60) + 1
                dash_text = f"Air Dash: {cooldown_seconds}s cooldown"
                dash_color = GRAY
            elif (hasattr(self.player, 'returning_to_start') and self.player.returning_to_start):
                dash_text = "Returning to Position"
                dash_color = UI_ACCENT
            elif self.player.air_dash_used:
                dash_text = "Air Dash: Used (land to reset)"
                dash_color = GRAY
            else:
                dash_text = "Air Dash: Ready [D]"
                dash_color = DARK_GRAY
            
            air_dash_surface = self.tiny_font.render(dash_text, True, dash_color)
            win.blit(air_dash_surface, (200, hud_y))
            
        destroyed_count = self.obstacle_manager.get_destroyed_count()
        if destroyed_count > 0:
            destroyed_text = f"Obstacles Destroyed: +{destroyed_count}"
            destroyed_surface = self.tiny_font.render(destroyed_text, True, UI_ACCENT)
            win.blit(destroyed_surface, (400, 40))
        
        controls_text = self.tiny_font.render("SPACE: Jump • S: Shield • D: Air Dash • ESC: Menu", True, GRAY)
        win.blit(controls_text, (WIDTH - controls_text.get_width() - 20, 75))


class GameOverState(GameState):
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

    def format_number(self, num):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}k"
        else:
            return str(num)

    def draw(self, win):
        win.fill(UI_BACKGROUND)
        
        box_width = 500
        box_height = 320
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        
        pygame.draw.rect(win, WHITE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(win, GRAY, (box_x, box_y, box_width, box_height), 3)
        
        if self.new_high_score:
            title_text = "NEW HIGH SCORE!"
            title_color = DARK_GRAY
        else:
            title_text = "GAME OVER"
            title_color = UI_TEXT
            
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(WIDTH//2, box_y + 50))
        win.blit(title_surface, title_rect)
        
        score_text = f"Final Score: {self.format_number(self.final_score)}"
        score_surface = self.font.render(score_text, True, UI_TEXT)
        score_rect = score_surface.get_rect(center=(WIDTH//2, box_y + 100))
        win.blit(score_surface, score_rect)
        
        score_multiplier = self.game_manager.save_system.get_score_multiplier()
        if score_multiplier > 1:
            mult_text = f"({score_multiplier}x Score Multiplier Applied)"
            mult_surface = self.small_font.render(mult_text, True, UI_ACCENT)
            mult_rect = mult_surface.get_rect(center=(WIDTH//2, box_y + 125))
            win.blit(mult_surface, mult_rect)
        
        coins_text = f"Coins Earned: {self.format_number(self.coins_earned)}"
        coins_surface = self.small_font.render(coins_text, True, UI_ACCENT)
        coins_rect = coins_surface.get_rect(center=(WIDTH//2, box_y + 160))
        win.blit(coins_surface, coins_rect)
        
        controls = [
            ("R", "Restart"),
            ("M", "Menu"),
            ("ESC", "Quit")
        ]
        
        y_offset = box_y + 210
        for key, action in controls:
            key_text = self.small_font.render(f"[{key}]", True, DARK_GRAY)
            action_text = self.small_font.render(action, True, UI_TEXT)
            
            key_width = key_text.get_width()
            total_width = key_width + 10 + action_text.get_width()
            start_x = (WIDTH - total_width) // 2
            
            win.blit(key_text, (start_x, y_offset))
            win.blit(action_text, (start_x + key_width + 10, y_offset))
            y_offset += 25