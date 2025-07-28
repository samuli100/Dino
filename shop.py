import pygame
import math
from constants import get_colors


class ShopItem:
    def __init__(self, name, description, base_cost, unlock_requirements, max_level):
        self.name = name
        self.description = description
        self.base_cost = base_cost
        self.unlock_requirements = unlock_requirements
        self.max_level = max_level

    def get_cost(self, current_level):
        if current_level >= self.max_level:
            return 0
        multiplier = 1.5 + (current_level * 0.3)
        return int(self.base_cost * multiplier)

    def is_level_unlocked(self, level, high_score):
        if level == 0:
            return high_score >= self.unlock_requirements[0]
        if level < len(self.unlock_requirements):
            return high_score >= self.unlock_requirements[level]
        return False

    def is_next_level_unlocked(self, current_level, high_score):
        next_level = current_level + 1
        if next_level > self.max_level:
            return False
        return self.is_level_unlocked(next_level - 1, high_score)

    def get_next_unlock_requirement(self, current_level):
        next_level = current_level + 1
        if next_level > self.max_level:
            return None
        if next_level - 1 < len(self.unlock_requirements):
            return self.unlock_requirements[next_level - 1]
        return None

    def is_maxed(self, current_level):
        return current_level >= self.max_level


class Shop:
    def __init__(self, save_system):
        self.save_system = save_system
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)
        
        self.items = {
            "jump_boost": ShopItem(
                "Jump Boost", 
                "Higher jumps for better obstacle clearing", 
                10, 
                [0, 1000, 2000, 5000, 10000],
                5
            ),
            "coin_multiplier": ShopItem(
                "Coin Multiplier", 
                "Extra coins per obstacle passed", 
                25, 
                [500, 2000, 5000, 15000, 35000, 70000, 120000, 180000, 250000],
                9
            ),
            "speed_boost": ShopItem(
                "Speed Boost", 
                "Faster movement and higher scores", 
                20, 
                [1000, 3000, 7000],
                3
            ),
            "shield": ShopItem(
                "Shield", 
                "Press S for temporary protection", 
                50, 
                [5000],
                1
            ),
            "slow_motion": ShopItem(
                "Slow Motion", 
                "Slower obstacles, easier timing", 
                75, 
                [10000, 15000, 25000, 40000],
                4
            ),
            "shield_upgrade": ShopItem(
                "Shield Enhance", 
                "Better shield duration and cooldown", 
                100, 
                [15000, 20000, 30000, 50000, 75000, 100000],
                6
            ),
            "slow_acceleration": ShopItem(
                "Steady Pace", 
                "Slower game speed increase", 
                80, 
                [20000, 35000, 60000, 100000],
                4
            ),
            "score_multiplier": ShopItem(
                "Score Multiplier", 
                "10x/100x/1000x points per obstacle!", 
                500, 
                [25000, 250000, 2500000],
                3
            ),
            "air_jump": ShopItem(
                "Air Jump", 
                "Small jump while airborne", 
                120, 
                [50000],
                1
            ),
            "air_dash": ShopItem(
                "Air Dash", 
                "Press D to dash horizontally in air", 
                150, 
                [100000],
                1
            ),
            "dash_distance": ShopItem(
                "Dash Distance", 
                "Longer air dash distance", 
                200, 
                [150000, 300000, 500000],
                3
            ),
            "dodge_chance": ShopItem(
                "Lucky Dodge", 
                "Chance to survive cactus collision", 
                300, 
                [200000, 400000, 800000, 1600000, 3200000],
                5
            ),
            "bonus_health": ShopItem(
                "Extra Life", 
                "Survive one extra hit", 
                500, 
                [500000, 5000000],
                2
            )
        }
        
        self.cols = 2
        self.items_per_tab = 4
        self.current_tab = 0
        self.selected_row = 0
        self.selected_col = 0
        self.tab_transition_offset = 0
        self.transitioning = False
        self.transition_speed = 15
        
        self.item_list = list(self.items.items())
        self.total_tabs = math.ceil(len(self.item_list) / self.items_per_tab)

    def get_current_tab_items(self):
        start_idx = self.current_tab * self.items_per_tab
        end_idx = start_idx + self.items_per_tab
        return self.item_list[start_idx:end_idx]

    def get_selected_item_index(self):
        return self.selected_row * self.cols + self.selected_col

    def get_selected_item_name(self):
        current_items = self.get_current_tab_items()
        item_index = self.get_selected_item_index()
        if item_index < len(current_items):
            return current_items[item_index][0]
        return None

    def move_selection(self, direction):
        current_items = self.get_current_tab_items()
        rows_in_tab = math.ceil(len(current_items) / self.cols)
        
        if direction == "up":
            if self.selected_row > 0:
                self.selected_row -= 1
        elif direction == "down":
            if self.selected_row < rows_in_tab - 1:
                test_index = (self.selected_row + 1) * self.cols + self.selected_col
                if test_index < len(current_items):
                    self.selected_row += 1
        elif direction == "left":
            if self.selected_col > 0:
                self.selected_col -= 1
            elif self.current_tab > 0:
                self.start_transition(-1)
                self.selected_col = self.cols - 1
        elif direction == "right":
            if self.selected_col < self.cols - 1:
                test_index = self.selected_row * self.cols + (self.selected_col + 1)
                if test_index < len(current_items):
                    self.selected_col += 1
                elif self.current_tab < self.total_tabs - 1:
                    self.start_transition(1)
                    self.selected_col = 0
            elif self.current_tab < self.total_tabs - 1:
                self.start_transition(1)
                self.selected_col = 0

    def try_buy_upgrade(self, upgrade_name):
        if upgrade_name not in self.items:
            return False
            
        item = self.items[upgrade_name]
        current_level = self.save_system.data["upgrades"][upgrade_name]
        high_score = self.save_system.data["high_score"]
        
        if item.is_maxed(current_level):
            return False
            
        if not item.is_next_level_unlocked(current_level, high_score):
            return False
            
        cost = item.get_cost(current_level)
        if not self.save_system.spend_coins(cost):
            return False
            
        self.save_system.upgrade_item(upgrade_name)
        self.save_system.save_data()
        return True

    def format_number(self, num):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}k"
        else:
            return str(num)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                return "menu"
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                upgrade_name = self.get_selected_item_name()
                if upgrade_name:
                    self.try_buy_upgrade(upgrade_name)
            elif event.key == pygame.K_UP:
                self.move_selection("up")
            elif event.key == pygame.K_DOWN:
                self.move_selection("down")
            elif event.key == pygame.K_LEFT:
                self.move_selection("left")
            elif event.key == pygame.K_RIGHT:
                self.move_selection("right")
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  
                self.move_selection("up")
            elif event.y < 0:  
                self.move_selection("down")
        return None

    def start_transition(self, direction):
        if not self.transitioning:
            self.transitioning = True
            self.transition_direction = direction
            self.tab_transition_offset = 0

    def update(self):
        if self.transitioning:
            self.tab_transition_offset += self.transition_speed * self.transition_direction
            
            if abs(self.tab_transition_offset) >= 400:
                self.current_tab += self.transition_direction
                self.current_tab = max(0, min(self.total_tabs - 1, self.current_tab))
                self.transitioning = False
                self.tab_transition_offset = 0
                
                current_items = self.get_current_tab_items()
                rows_in_tab = math.ceil(len(current_items) / self.cols)
                self.selected_row = min(self.selected_row, rows_in_tab - 1)
                
                while (self.selected_row * self.cols + self.selected_col >= len(current_items) and 
                       (self.selected_row > 0 or self.selected_col > 0)):
                    if self.selected_col > 0:
                        self.selected_col -= 1
                    else:
                        self.selected_row -= 1
                        self.selected_col = self.cols - 1

    def draw_tab_indicator(self, win):
        if self.total_tabs <= 1:
            return
        
        colors = get_colors()
        dot_size = 8
        dot_spacing = 20
        total_width = (self.total_tabs - 1) * dot_spacing
        start_x = (800 - total_width) // 2
        y = 370
        
        for i in range(self.total_tabs):
            x = start_x + i * dot_spacing
            color = colors["UI_ACCENT"] if i == self.current_tab else colors["LIGHT_GRAY"]
            pygame.draw.circle(win, color, (x, y), dot_size)

    def draw_card(self, win, x, y, width, height, item_name, item, current_level, is_selected):
        colors = get_colors()
        high_score = self.save_system.data["high_score"]
        is_maxed = item.is_maxed(current_level)
        
        next_level_unlocked = item.is_next_level_unlocked(current_level, high_score)
        can_afford = True
        
        if next_level_unlocked and not is_maxed:
            cost = item.get_cost(current_level)
            can_afford = self.save_system.data["coins"] >= cost
        
        if is_selected:
            pygame.draw.rect(win, colors["UI_ACCENT"], (x - 3, y - 3, width + 6, height + 6))
        
        if not next_level_unlocked and not is_maxed:
            bg_color = colors["LIGHT_GRAY"]
            border_color = colors["MEDIUM_GRAY"]
        elif is_maxed:
            bg_color = colors["WHITE"]
            border_color = colors["DARK_GRAY"]
        elif can_afford:
            bg_color = colors["WHITE"]
            border_color = colors["UI_ACCENT"] if is_selected else colors["GRAY"]
        else:
            bg_color = colors["UI_BACKGROUND"]
            border_color = colors["UI_BORDER"]
        
        pygame.draw.rect(win, bg_color, (x, y, width, height))
        pygame.draw.rect(win, border_color, (x, y, width, height), 3 if is_selected else 2)
        
        name_color = colors["GRAY"] if not next_level_unlocked and not is_maxed else colors["UI_TEXT"]
        name_text = self.font.render(item.name, True, name_color)
        win.blit(name_text, (x + 15, y + 10))
        
        level_text = f"Level {current_level}/{item.max_level}"
        level_color = colors["DARK_GRAY"] if is_maxed else colors["UI_ACCENT"]
        level_surface = self.small_font.render(level_text, True, level_color)
        win.blit(level_surface, (x + 15, y + 35))
        
        desc_color = colors["GRAY"] if not next_level_unlocked and not is_maxed else colors["UI_TEXT"]
        desc_surface = self.tiny_font.render(item.description, True, desc_color)
        win.blit(desc_surface, (x + 15, y + 60))
        
        if is_maxed:
            status_text = "MAXED OUT"
            status_color = colors["DARK_GRAY"]
        elif not next_level_unlocked:
            next_unlock = item.get_next_unlock_requirement(current_level)
            if next_unlock:
                status_text = f"Unlock at {self.format_number(next_unlock)} score"
                status_color = colors["GRAY"]
            else:
                status_text = "MAX LEVEL"
                status_color = colors["GRAY"]
        else:
            cost = item.get_cost(current_level)
            status_text = f"Cost: {self.format_number(cost)} coins"
            status_color = colors["UI_ACCENT"] if can_afford else colors["GRAY"]
        
        status_surface = self.small_font.render(status_text, True, status_color)
        win.blit(status_surface, (x + 15, y + 80))
        
        if is_selected and next_level_unlocked and not is_maxed and can_afford:
            hint_text = "[SPACE] to purchase"
            hint_surface = self.tiny_font.render(hint_text, True, colors["UI_ACCENT"])
            hint_x = x + width - hint_surface.get_width() - 10
            hint_y = y + height - hint_surface.get_height() - 5
            win.blit(hint_surface, (hint_x, hint_y))
        
        if item_name == "score_multiplier" and current_level > 0:
            multiplier_values = [10, 100, 1000]
            if current_level <= len(multiplier_values):
                mult_text = f"{multiplier_values[current_level-1]}x Score!"
                mult_surface = self.tiny_font.render(mult_text, True, colors["DARK_GRAY"])
                mult_x = x + width - mult_surface.get_width() - 10
                mult_y = y + 15
                win.blit(mult_surface, (mult_x, mult_y))

    def draw_tab_content(self, win, offset_x=0):
        current_items = self.get_current_tab_items()
        
        available_width = 800 - 100  
        card_width = min(350, (available_width - 25) // 2)  
        card_height = 110
        margin_x = (available_width - (card_width * 2)) // 3 
        margin_y = 20
        start_y = 140
        
        for i, (upgrade_name, item) in enumerate(current_items):
            current_level = self.save_system.data["upgrades"][upgrade_name]
            
            col = i % self.cols
            row = i // self.cols
            x = 50 + col * (card_width + margin_x) + offset_x
            y = start_y + row * (card_height + margin_y)
            
            is_selected = (row == self.selected_row and col == self.selected_col)
            self.draw_card(win, x, y, card_width, card_height, upgrade_name, item, current_level, is_selected)

    def draw(self, win):
        self.update()
        
        colors = get_colors()
        
        win.fill(colors["UI_BACKGROUND"])
        
        header_height = 120
        pygame.draw.rect(win, colors["WHITE"], (0, 0, 800, header_height))
        pygame.draw.line(win, colors["UI_BORDER"], (0, header_height), (800, header_height), 2)
        
        title = self.title_font.render("UPGRADE SHOP", True, colors["UI_TEXT"])
        win.blit(title, (50, 25))
        
        coins_text = f"Coins: {self.format_number(self.save_system.data['coins'])}"
        score_text = f"High Score: {self.format_number(self.save_system.data['high_score'])}"
        
        coins_surface = self.font.render(coins_text, True, colors["UI_ACCENT"])
        score_surface = self.small_font.render(score_text, True, colors["UI_TEXT"])
        
        max_text_width = 250
        if coins_surface.get_width() > max_text_width:
            coins_surface = self.small_font.render(coins_text, True, colors["UI_ACCENT"])
        if score_surface.get_width() > max_text_width:
            score_surface = self.tiny_font.render(score_text, True, colors["UI_TEXT"])
        
        win.blit(coins_surface, (800 - coins_surface.get_width() - 50, 25))
        win.blit(score_surface, (800 - score_surface.get_width() - 50, 55))
        
        if self.total_tabs > 1:
            tab_text = f"Tab {self.current_tab + 1} of {self.total_tabs}"
            tab_surface = self.small_font.render(tab_text, True, colors["GRAY"])
            tab_x = 400 - tab_surface.get_width() // 2
            win.blit(tab_surface, (tab_x, 65))
        
        instructions = "Arrow Keys Navigate • SPACE Purchase • M/ESC Menu • Mouse Wheel Scroll"
        inst_surface = self.small_font.render(instructions, True, colors["GRAY"])
        
        if inst_surface.get_width() > 700:
            inst_surface = self.tiny_font.render(instructions, True, colors["GRAY"])
        
        win.blit(inst_surface, (50, 85))
        
        if self.transitioning:
            self.draw_tab_content(win, -self.tab_transition_offset)
            
            next_tab_offset = 400 * self.transition_direction - self.tab_transition_offset
            old_tab = self.current_tab
            target_tab = self.current_tab + self.transition_direction
            if 0 <= target_tab < self.total_tabs:
                self.current_tab = target_tab
                self.draw_tab_content(win, next_tab_offset)
                self.current_tab = old_tab
        else:
            self.draw_tab_content(win)
        
        self.draw_tab_indicator(win)