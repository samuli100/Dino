import pygame
import random

class Obstacle:
    def __init__(self):
        self.image = pygame.Surface((20, 50))
        self.image.fill((34, 139, 34))
        self.rect = self.image.get_rect(midbottom=(random.randint(800, 1000), 350))
        self.speed = 6

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
