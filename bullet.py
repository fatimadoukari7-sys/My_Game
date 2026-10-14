import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A bullet fired by the hero."""

    def __init__(self, settings, screen, hero):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.color = settings.bullet_color
        self.rect.centerx = hero.rect.centerx
        self.rect.bottom = hero.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.ellipse(self.screen, self.color, self.rect)