import math

import pygame
from pygame.sprite import Sprite


class MonsterFire(Sprite):
    """A fireball shot by the monster toward the hero."""

    def __init__(self, settings, screen, monster, hero):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        size = settings.monster_fire_size
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = monster.rect.center

        # Aim at the hero's position at the moment of firing.
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        speed = settings.monster_fire_speed
        self.vx = dx / dist * speed
        self.vy = dy / dist * speed
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if not self.screen_rect.colliderect(self.rect):
            self.kill()

    def draw(self):
        pygame.draw.ellipse(self.screen, (255, 120, 20), self.rect)
        pygame.draw.ellipse(self.screen, (255, 230, 90), self.rect.inflate(-10, -10))