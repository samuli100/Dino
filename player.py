import pygame

class Player:
    def __init__(self):
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(midbottom=(100, 350))
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_force = -15
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= 350:
            self.rect.bottom = 350
            self.vel_y = 0
            self.on_ground = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)
