import pygame
from constants import BLACK, GRAY, WHITE, GREEN


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
    """Shop system for upgrades"""
    
    def __init__(self, save_system):
        self.save_system = save_system
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize shop items
        self.items = {
            "jump_boost": ShopItem("Jump Boost", "Higher jumps", 10, 0, 5),
            "coin_multiplier": ShopItem("Coin Multiplier", "2x coins per cactus", 25, 100, 3),
            "speed_boost": ShopItem("Speed Boost", "Faster movement", 20, 200, 3),
            "shield": ShopItem("Shield", "Press S for protection", 50, 500, 1),
            "slow_motion": ShopItem("Slow Motion", "Slower obstacles", 75, 750, 4)
        }

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
            elif event.key >= pygame.K_1 and event.key <= pygame.K_5:
                item_index = event.key - pygame.K_1
                item_names = list(self.items.keys())
                if item_index < len(item_names):
                    self.try_buy_upgrade(item_names[item_index])
        return None

    def draw(self, win):
        """Draw the shop interface"""
        win.fill(WHITE)
        
        # Title
        title = self.font.render(f"SHOP - Coins: {self.save_system.data['coins']}", True, BLACK)
        win.blit(title, (50, 30))
        
        # Instructions
        instructions = self.small_font.render("Press number keys (1-5) to buy, M or ESC to return to menu", True, BLACK)
        win.blit(instructions, (50, 70))
        
        # Draw items
        y_pos = 110
        for i, (upgrade_name, item) in enumerate(self.items.items()):
            current_level = self.save_system.data["upgrades"][upgrade_name]
            
            # Determine color and text
            if not item.is_unlocked(self.save_system.data["high_score"]):
                color = GRAY
                text = f"{i+1}. {item.name} - Level {current_level}/{item.max_level} (Unlock at score {item.unlock_score})"
            elif item.is_maxed(current_level):
                color = GREEN
                text = f"{i+1}. {item.name} - Level {current_level}/{item.max_level} (MAXED)"
            else:
                color = BLACK
                cost = item.get_cost(current_level)
                text = f"{i+1}. {item.name} - Level {current_level}/{item.max_level} - Cost: {cost} coins"
            
            # Draw item text
            rendered = self.small_font.render(text, True, color)
            win.blit(rendered, (50, y_pos))
            
            # Draw description
            desc = self.small_font.render(f"   {item.description}", True, GRAY)
            win.blit(desc, (50, y_pos + 20))
            
            y_pos += 50