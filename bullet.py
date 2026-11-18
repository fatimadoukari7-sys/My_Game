import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A bullet fired by the hero: a position that moves up.

    It does not draw itself and does not know its color or picture:
    the Renderer draws it using theme.py.
    """

    def __init__(self, settings, screen, hero):
        super().__init__()

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = hero.rect.centerx
        self.rect.bottom = hero.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.speed_factor
        self.rect.y = self.y