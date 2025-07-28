import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()  

WIDTH_CELLS = simpledialog.askinteger("Pixel Art Editor", "Enter grid width (e.g., 16):", minvalue=4, maxvalue=64)
HEIGHT_CELLS = simpledialog.askinteger("Pixel Art Editor", "Enter grid height (e.g., 16):", minvalue=4, maxvalue=64)
if not WIDTH_CELLS or not HEIGHT_CELLS:
    sys.exit()

PIXEL_SIZE = 30
WIDTH = WIDTH_CELLS * PIXEL_SIZE
HEIGHT = HEIGHT_CELLS * PIXEL_SIZE + 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Art Grid Editor")
font = pygame.font.SysFont(None, 24)

grid = [[0 for _ in range(WIDTH_CELLS)] for _ in range(HEIGHT_CELLS)]

done_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 30)

running = True
while running:
    screen.fill(WHITE)

    for y in range(HEIGHT_CELLS):
        for x in range(WIDTH_CELLS):
            rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            color = BLACK if grid[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    pygame.draw.rect(screen, BLUE, done_button_rect)
    text_surf = font.render("Done", True, WHITE)
    screen.blit(text_surf, (done_button_rect.x + 25, done_button_rect.y + 5))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if done_button_rect.collidepoint(mx, my):
                print("[  # Exported pixel art")
                for row in grid:
                    print("    [" + ",".join(str(cell) for cell in row) + "],")
                print("]")
                print("\nYou can now copy this array into your game.")
                running = False

            elif my < HEIGHT_CELLS * PIXEL_SIZE:
                gx = mx // PIXEL_SIZE
                gy = my // PIXEL_SIZE
                if 0 <= gx < WIDTH_CELLS and 0 <= gy < HEIGHT_CELLS:
                    if event.button == 1:
                        grid[gy][gx] = 1
                    elif event.button == 3:
                        grid[gy][gx] = 0

pygame.quit()
sys.exit()
