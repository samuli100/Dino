import pygame
import math
from constants import (UI_BACKGROUND, UI_BORDER, UI_TEXT, UI_ACCENT, BUTTON_HOVER, 
                      MEDIUM_GRAY, GRAY, DARK_GRAY, WHITE, LIGHT_GRAY)


class ShopItem:
    """Represents a shop item with its properties"""
    
    def __init__(self, name, description, base_cost, unlock_score, max_level):
        self.name = name
        self.description = description
        self.base_cost = base_cost
        self.unlock_score = unlock_score
        self.max_level = max_level

    def get_cost(self, current_level):
        """Calculate cost based on current level"""
        return self.base_cost + (current_level * self.base_cost // 2)

    def is_unlocked(self, high_score):
        """Check if item is unlocked"""
        return high_score >= self.unlock_score

    def is_maxed(self, current_level):
        """Check if item is at max level"""
        return current_level >= self.max_level


class Shop:
    """Shop system for upgrades with tabbed interface"""
    
    def __init__(self, save_system):
        self.save_system = save_system
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)
        
        # Initialize shop items
        self.items = {
            "jump_boost": ShopItem("Jump Boost", "Higher jumps for better obstacle clearing", 10, 0, 5),
            "coin_multiplier": ShopItem("Coin Multiplier", "2x coins per cactus passed", 25, 100, 3),
            "speed_boost": ShopItem("Speed Boost", "Faster movement and higher scores", 20, 200, 3),
            "shield": ShopItem("Shield", "Press S for temporary protection", 50, 500, 1),
            "slow_motion": ShopItem("Slow Motion", "Slower obstacles, easier timing", 75, 750, 4)
        }
        
        # Tab system
        self.items_per_tab = 4
        self.current_tab = 0
        self.selected_item = 0
        self.tab_transition_offset = 0
        self.transitioning = False
        self.transition_speed = 15
        
        # Get item lists for tabs
        self.item_list = list(self.items.items())
        self.total_tabs = math.ceil(len(self.item_list) / self.items_per_tab)

    def get_current_tab_items(self):
        """Get items for current tab"""
        start_idx = self.current_tab * self.items_per_tab
        end_idx = start_idx + self.items_per_tab
        return self.item_list[start_idx:end_idx]

    def try_buy_upgrade(self, upgrade_name):
        """Attempt to buy an upgrade"""
        if upgrade_name not in self.items:
            return False
            
        item = self.items[upgrade_name]
        current_level = self.save_system.data["upgrades"][upgrade_name]
        
        # Check conditions
        if not item.is_unlocked(self.save_system.data["high_score"]):
            return False
        if item.is_maxed(current_level):
            return False
            
        cost = item.get_cost(current_level)
        if not self.save_system.spend_coins(cost):
            return False
            
        # Purchase successful
        self.save_system.upgrade_item(upgrade_name)
        self.save_system.save_data()
        return True

    def handle_event(self, event):
        """Handle shop input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                return "menu"
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Purchase selected item
                current_items = self.get_current_tab_items()
                if self.selected_item < len(current_items):
                    upgrade_name = current_items[self.selected_item][0]
                    self.try_buy_upgrade(upgrade_name)
            elif event.key == pygame.K_UP:
                self.selected_item = max(0, self.selected_item - 1)
            elif event.key == pygame.K_DOWN:
                current_items = self.get_current_tab_items()
                self.selected_item = min(len(current_items) - 1, self.selected_item + 1)
            elif event.key == pygame.K_LEFT and not self.transitioning:
                if self.current_tab > 0:
                    self.start_transition(-1)
            elif event.key == pygame.K_RIGHT and not self.transitioning:
                if self.current_tab < self.total_tabs - 1:
                    self.start_transition(1)
        return None

    def start_transition(self, direction):
        """Start tab transition animation"""
        self.transitioning = True
        self.transition_direction = direction
        self.tab_transition_offset = 0

    def update(self):
        """Update shop animations"""
        if self.transitioning:
            self.tab_transition_offset += self.transition_speed * self.transition_direction
            
            if abs(self.tab_transition_offset) >= 400:  # Full transition width
                self.current_tab += self.transition_direction
                self.current_tab = max(0, min(self.total_tabs - 1, self.current_tab))
                self.transitioning = False
                self.tab_transition_offset = 0
                self.selected_item = 0  # Reset selection

    def draw_tab_indicator(self, win):
        """Draw tab indicator dots"""
        if self.total_tabs <= 1:
            return
            
        dot_size = 8
        dot_spacing = 20
        total_width = (self.total_tabs - 1) * dot_spacing
        start_x = (800 - total_width) // 2
        y = 370
        
        for i in range(self.total_tabs):
            x = start_x + i * dot_spacing
            color = UI_ACCENT if i == self.current_tab else LIGHT_GRAY
            pygame.draw.circle(win, color, (x, y), dot_size)

    def draw_card(self, win, x, y, width, height, item_name, item, current_level, is_selected):
        """Draw a shop item card"""
        # Determine card state and colors
        is_unlocked = item.is_unlocked(self.save_system.data["high_score"])
        is_maxed = item.is_maxed(current_level)
        can_afford = True
        
        if is_unlocked and not is_maxed:
            cost = item.get_cost(current_level)
            can_afford = self.save_system.data["coins"] >= cost
        
        # Card background and selection
        if is_selected:
            # Selected card gets a highlight
            pygame.draw.rect(win, UI_ACCENT, (x - 3, y - 3, width + 6, height + 6))
        
        if not is_unlocked:
            bg_color = LIGHT_GRAY
            border_color = MEDIUM_GRAY
        elif is_maxed:
            bg_color = WHITE
            border_color = DARK_GRAY
        elif can_afford:
            bg_color = WHITE
            border_color = UI_ACCENT if is_selected else GRAY
        else:
            bg_color = UI_BACKGROUND
            border_color = UI_BORDER
        
        # Draw card
        pygame.draw.rect(win, bg_color, (x, y, width, height))
        pygame.draw.rect(win, border_color, (x, y, width, height), 3 if is_selected else 2)
        
        # Item name
        name_color = GRAY if not is_unlocked else UI_TEXT
        name_text = self.font.render(item.name, True, name_color)
        win.blit(name_text, (x + 20, y + 15))
        
        # Level indicator
        level_text = f"Level {current_level}/{item.max_level}"
        level_color = DARK_GRAY if is_maxed else UI_ACCENT
        level_surface = self.small_font.render(level_text, True, level_color)
        win.blit(level_surface, (x + 20, y + 45))
        
        # Description
        desc_color = GRAY if not is_unlocked else UI_TEXT
        desc_surface = self.tiny_font.render(item.description, True, desc_color)
        win.blit(desc_surface, (x + 20, y + 75))
        
        # Cost or status
        if not is_unlocked:
            status_text = f"Unlock at score {item.unlock_score}"
            status_color = GRAY
        elif is_maxed:
            status_text = "MAXED OUT"
            status_color = DARK_GRAY
        else:
            cost = item.get_cost(current_level)
            status_text = f"Cost: {cost} coins"
            status_color = UI_ACCENT if can_afford else GRAY
        
        status_surface = self.small_font.render(status_text, True, status_color)
        win.blit(status_surface, (x + 20, y + 95))
        
        # Purchase hint for selected item
        if is_selected and is_unlocked and not is_maxed and can_afford:
            hint_text = "[SPACE] to purchase"
            hint_surface = self.tiny_font.render(hint_text, True, UI_ACCENT)
            hint_x = x + width - hint_surface.get_width() - 15
            hint_y = y + height - hint_surface.get_height() - 10
            win.blit(hint_surface, (hint_x, hint_y))

    def draw_tab_content(self, win, offset_x=0):
        """Draw the current tab's content"""
        current_items = self.get_current_tab_items()
        
        # Card dimensions
        card_width = 350
        card_height = 120
        margin_x = 25
        margin_y = 20
        start_y = 140
        
        for i, (upgrade_name, item) in enumerate(current_items):
            current_level = self.save_system.data["upgrades"][upgrade_name]
            
            # Calculate position (2 columns)
            col = i % 2
            row = i // 2
            x = 50 + col * (card_width + margin_x) + offset_x
            y = start_y + row * (card_height + margin_y)
            
            is_selected = (i == self.selected_item)
            self.draw_card(win, x, y, card_width, card_height, upgrade_name, item, current_level, is_selected)

    def draw(self, win):
        """Draw the shop interface"""
        # Update animations
        self.update()
        
        win.fill(UI_BACKGROUND)
        
        # Header section
        header_height = 120
        pygame.draw.rect(win, WHITE, (0, 0, 800, header_height))
        pygame.draw.line(win, UI_BORDER, (0, header_height), (800, header_height), 2)
        
        # Title
        title = self.title_font.render("UPGRADE SHOP", True, UI_TEXT)
        title_x = 50
        title_y = 25
        win.blit(title, (title_x, title_y))
        
        # Coins display
        coins_text = f"Coins: {self.save_system.data['coins']}"
        coins_surface = self.font.render(coins_text, True, UI_ACCENT)
        coins_x = 800 - coins_surface.get_width() - 50
        coins_y = 30
        win.blit(coins_surface, (coins_x, coins_y))
        
        # Tab indicator
        if self.total_tabs > 1:
            tab_text = f"Tab {self.current_tab + 1} of {self.total_tabs}"
            tab_surface = self.small_font.render(tab_text, True, GRAY)
            tab_x = 400 - tab_surface.get_width() // 2
            tab_y = 65
            win.blit(tab_surface, (tab_x, tab_y))
        
        # Instructions
        instructions = "↑↓ Navigate • ←→ Switch tabs • SPACE Purchase • M/ESC Menu"
        inst_surface = self.small_font.render(instructions, True, GRAY)
        inst_x = 50
        inst_y = 85
        win.blit(inst_surface, (inst_x, inst_y))
        
        # Draw tab content with transition
        if self.transitioning:
            # Draw current tab
            self.draw_tab_content(win, -self.tab_transition_offset)
            
            # Draw next/previous tab
            next_tab_offset = 400 * self.transition_direction - self.tab_transition_offset
            
            # Temporarily switch to the target tab for drawing
            old_tab = self.current_tab
            target_tab = self.current_tab + self.transition_direction
            if 0 <= target_tab < self.total_tabs:
                self.current_tab = target_tab
                self.draw_tab_content(win, next_tab_offset)
                self.current_tab = old_tab
        else:
            # Normal drawing
            self.draw_tab_content(win)
        
        # Draw tab indicator dots
        self.draw_tab_indicator(win)