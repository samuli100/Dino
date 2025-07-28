import pygame
from constants import BLOCK_SIZE, get_color

def draw_pixel_art(win, pattern, top_left_x, top_left_y, color=None):
    if color is None:
        color = get_color("VERY_DARK")
    
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