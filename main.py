import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino - Enhanced")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

clock = pygame.time.Clock()
FPS = 60
GROUND_Y = 350

BLOCK_SIZE = 4  # Smaller blocks for higher resolution

# Enhanced Dino pixel art (4 frames for smoother animation)
# Based on your custom first frame design
DINO_FRAMES = [
    [
        # Frame 0 - Standing/Running 1 (your design)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
    ],
    [
        # Frame 1 - Running 2 (left leg lifted)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
    ],
    [
        # Frame 2 - Running 3 (both legs in air/transition)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
    ],
    [
        # Frame 3 - Running 4 (right leg lifted)
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    ]
]

# Enhanced Cactus pixel art patterns (multiple types)
CACTUS_PATTERNS = [
    # Small cactus
    [
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
    ],
    # Tall cactus
    [
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
        [0,0,1,1,0,0],
    ],
    # Wide cactus with multiple arms
    [
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,1,0,0],
        [0,0,1,1,1,1,1,1],
        [0,0,1,1,1,1,1,1],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
    ]
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

        # Animate only when on ground (running)
        if self.on_ground:
            self.anim_timer += 1
            if self.anim_timer > 8:  # Faster animation for smoother running
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
        self.pattern = random.choice(CACTUS_PATTERNS)
        self.x = WIDTH
        self.y = GROUND_Y - len(self.pattern) * BLOCK_SIZE
        self.speed = 6

    def update(self):
        self.x -= self.speed

    def get_rect(self):
        width = len(self.pattern[0]) * BLOCK_SIZE
        height = len(self.pattern) * BLOCK_SIZE
        return pygame.Rect(self.x, self.y, width, height)

    def draw(self, win):
        draw_pixel_art(win, self.pattern, self.x, self.y)

def main():
    player = Player()
    obstacles = []
    spawn_timer = 0
    score = 0
    font = pygame.font.Font(None, 36)

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

        # Spawn obstacles with varying intervals
        spawn_timer += 1
        spawn_interval = random.randint(80, 120)  # Random spawn timing
        if spawn_timer >= spawn_interval:
            obstacles.append(Cactus())
            spawn_timer = 0

        # Update score
        score += 1

        for obs in list(obstacles):
            obs.update()
            obs.draw(WIN)
            if obs.x + len(obs.pattern[0]) * BLOCK_SIZE < 0:
                obstacles.remove(obs)

            # Check collision with more precise hit detection
            player_rect = player.get_rect()
            obs_rect = obs.get_rect()
            
            # Shrink hitboxes slightly for more forgiving gameplay
            player_rect.inflate_ip(-8, -8)
            obs_rect.inflate_ip(-4, -4)
            
            if player_rect.colliderect(obs_rect):
                print(f"Game Over! Score: {score}")
                # Draw collision indicator
                pygame.draw.rect(WIN, (255, 0, 0), player.get_rect(), 3)
                
                # Display game over screen
                game_over_text = font.render(f"Game Over! Score: {score}", True, BLACK)
                restart_text = font.render("Press R to restart or ESC to quit", True, BLACK)
                WIN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
                WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))
                pygame.display.update()
                
                # Wait for restart or quit
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            waiting = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                # Restart game
                                player = Player()
                                obstacles = []
                                spawn_timer = 0
                                score = 0
                                waiting = False
                            elif event.key == pygame.K_ESCAPE:
                                run = False
                                waiting = False

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        WIN.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()