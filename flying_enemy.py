import random

import pygame
from pygame.sprite import Sprite

import theme


class FlyingEnemy(Sprite):
    """A flying monster (level 3). It enters from the top and flies down,
    drifting toward the hero. One bullet kills it.

    It only holds position and movement: the Renderer draws it.
    """

    _picture = None          # loaded once, shared by all enemies

    def __init__(self, screen_rect, hero, speed):
        super().__init__()
        self.screen_rect = screen_rect
        self.hero = hero
        self.speed = speed

        self.image = self._get_picture()
        self.rect = self.image.get_rect()
        self.x = float(random.randint(0, max(0, screen_rect.width - self.rect.width)))
        self.y = float(-self.rect.height)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    @classmethod
    def _get_picture(cls):
        """The picture of the flying monster, scaled to the theme height."""
        if cls._picture is None:
            image = pygame.image.load(theme.FLYING_ENEMY["image"]).convert_alpha()
            w, h = image.get_size()
            height = theme.FLYING_ENEMY["height"]
            cls._picture = pygame.transform.smoothscale(
                image, (max(1, int(w * height / h)), height))
        return cls._picture

    def update(self):
        self.y += self.speed

        # Drift sideways toward the hero (slower than the fall).
        dx = self.hero.rect.centerx - self.rect.centerx
        step = self.speed * 0.5
        self.x += max(-step, min(step, dx))
        self.x = max(0.0, min(self.x, self.screen_rect.width - self.rect.width))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    @property
    def is_below_screen(self):
        return self.rect.top > self.screen_rect.bottom