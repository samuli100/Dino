import pygame
from constants import VERY_DARK, BLOCK_SIZE

def draw_pixel_art(win, pattern, top_left_x, top_left_y, color=VERY_DARK):
    """Utility function to draw pixel art patterns"""
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