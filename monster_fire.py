import math

import pygame
from pygame.sprite import Sprite


class MonsterFire(Sprite):
    """A fireball shot by the monster toward the hero.

    Its size and speed come from the monster profile (monsters/).
    It does not draw itself: the Renderer draws it using the colors of theme.py.
    """

    def __init__(self, profile, screen, monster, hero):
        super().__init__()
        self.screen_rect = screen.get_rect()
        size = profile.fire_size
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = monster.rect.center

        # Aim at the hero's position at the moment of firing.
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        speed = profile.fire_speed
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