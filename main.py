import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel-Art Dino")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

clock = pygame.time.Clock()
FPS = 60
GROUND_Y = 350

BLOCK_SIZE = 10  # Size of each pixel block

# Dino pixel art (2 frames for animation)
DINO_FRAMES = [
    [
        # frame 0
        [0,1,1,0,0],
        [1,1,1,1,0],
        [1,1,1,1,1],
        [0,1,1,1,0],
        [0,0,1,0,0],
        [0,1,0,1,0],
    ],
    [
        # frame 1 (legs shifted)
        [0,1,1,0,0],
        [1,1,1,1,0],
        [1,1,1,1,1],
        [0,1,1,1,0],
        [0,0,1,0,0],
        [1,0,0,1,0],
    ],
]

# Cactus pixel art
CACTUS_PATTERN = [
    [0,1,0],
    [1,1,1],
    [0,1,0],
    [0,1,0],
    [1,1,1],
]

def draw_pixel_art(win, pattern, top_left_x, top_left_y):
    for y, row in enumerate(pattern):
        for x, val in enumerate(row):
            if val == 1:
                rect = pygame.Rect(
                    top_left_x + x * BLOCK_SIZE,
                    top_left_y + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                pygame.draw.rect(win, BLACK, rect)

class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_force = -15
        self.on_ground = True
        self.anim_frame = 0
        self.anim_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y + len(DINO_FRAMES[0]) * BLOCK_SIZE >= GROUND_Y:
            self.y = GROUND_Y - len(DINO_FRAMES[0]) * BLOCK_SIZE
            self.vel_y = 0
            self.on_ground = True

        if self.on_ground:
            self.anim_timer += 1
            if self.anim_timer > 10:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % len(DINO_FRAMES)

    def get_rect(self):
        width = len(DINO_FRAMES[0][0]) * BLOCK_SIZE
        height = len(DINO_FRAMES[0]) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def draw(self, win):
        draw_pixel_art(win, DINO_FRAMES[self.anim_frame], self.x, self.y)

class Cactus:
    def __init__(self):
        self.x = WIDTH
        self.y = GROUND_Y - len(CACTUS_PATTERN) * BLOCK_SIZE
        self.speed = 6

    def update(self):
        self.x -= self.speed

    def get_rect(self):
        width = len(CACTUS_PATTERN[0]) * BLOCK_SIZE
        height = len(CACTUS_PATTERN) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def draw(self, win):
        draw_pixel_art(win, CACTUS_PATTERN, self.x, self.y)

def main():
    player = Player()
    obstacles = []
    spawn_timer = 0

    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)

        # Draw ground
        pygame.draw.line(WIN, GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.update()
        player.draw(WIN)

        spawn_timer += 1
        if spawn_timer >= 90:
            obstacles.append(Cactus())
            spawn_timer = 0

        for obs in list(obstacles):
            obs.update()
            obs.draw(WIN)
            if obs.x + len(CACTUS_PATTERN[0]) * BLOCK_SIZE < 0:
                obstacles.remove(obs)

            if player.get_rect().colliderect(obs.get_rect()):
                print("Game Over")
                pygame.draw.rect(WIN, (255, 0, 0), player.get_rect(), 3)
                pygame.display.update()
                pygame.time.delay(1000)
                run = False

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
