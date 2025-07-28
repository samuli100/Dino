import json
import os
from constants import SAVE_FILE
import pygame
import random

class SaveSystem:
    """Handles saving and loading game progress"""
    
    def __init__(self):
        self.data = {
            "coins": 0,
            "high_score": 0,
            "upgrades": {
                "jump_boost": 0,
                "coin_multiplier": 0,
                "speed_boost": 0,
                "shield": 0,
                "slow_motion": 0,
                "shield_upgrade": 0,
                "slow_acceleration": 0,
                "air_jump": 0,
                "air_dash": 0,
                "dash_distance": 0,
                "dodge_chance": 0,
                "bonus_health": 0
            }
        }
        self.load_save()

    def load_save(self):
        """Load save data from file"""
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    loaded_data = json.load(f)
                    # Merge with default data to handle new upgrades
                    if "upgrades" in loaded_data:
                        for key in self.data["upgrades"]:
                            if key not in loaded_data["upgrades"]:
                                loaded_data["upgrades"][key] = 0
                    self.data.update(loaded_data)
            except Exception as e:
                print(f"Error loading save: {e}")

    def save_data(self):
        """Save current data to file"""
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_coins(self, amount):
        """Add coins to player's total"""
        self.data["coins"] += amount

    def spend_coins(self, amount):
        """Spend coins if player has enough"""
        if self.data["coins"] >= amount:
            self.data["coins"] -= amount
            return True
        return False

    def update_high_score(self, score):
        """Update high score if new score is higher"""
        if score > self.data["high_score"]:
            self.data["high_score"] = score
            return True
        return False

    def upgrade_item(self, upgrade_name):
        """Upgrade an item by one level"""
        if upgrade_name in self.data["upgrades"]:
            self.data["upgrades"][upgrade_name] += 1