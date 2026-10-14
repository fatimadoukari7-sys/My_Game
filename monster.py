import math
import random

import pygame
from pygame.sprite import Sprite


class Monster(Sprite):
    """The monster the hero fights."""

    IMAGES = [
        'images/pikachu.png',
        'images/bullbasaur.png',
        'images/charmander.png',
        'images/eevee.png',
        'images/jigglypuff.png',
    ]

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.home_y = 70
        self.reset()

    def reset(self):
        """Pick a random look and place the monster at the top center."""
        self.image = pygame.image.load(random.choice(self.IMAGES))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.home_y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.direction = random.choice((-1, 1))
        self.dodge_until = 0
        self.decisions = {}   # bullet -> did we decide to dodge it?

    # ------------------------------------------------------------------
    def update(self, bullets, hero):
        now = pygame.time.get_ticks()

        # Hero has no way to hurt it anymore: hunt him down.
        if hero.ammo == 0 and len(bullets) == 0:
            self._chase(hero)
        else:
            self._patrol(bullets, now)

        self.rect.x = self.x
        self.rect.y = self.y

    def _chase(self, hero):
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            speed = self.settings.monster_chase_speed
            self.x += dx / dist * speed
            self.y += dy / dist * speed

    def _patrol(self, bullets, now):
        self._decide_dodge(bullets, now)

        speed = self.settings.monster_speed
        if now < self.dodge_until:
            speed *= 1.6
        elif random.random() < 0.01:
            self.direction *= -1          # random change of mind

        self.x += self.direction * speed

        width = self.rect.width
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        elif self.x + width >= self.screen_rect.right:
            self.x = self.screen_rect.right - width
            self.direction = -1

        # Drift back to the top area.
        if self.y > self.home_y:
            self.y -= 2
        elif self.y < self.home_y:
            self.y += 2

    def _decide_dodge(self, bullets, now):
        # Forget bullets that no longer exist.
        self.decisions = {b: d for b, d in self.decisions.items() if b.alive()}

        for bullet in bullets:
            coming = (bullet.rect.top > self.rect.top and
                      bullet.rect.top - self.rect.bottom < self.settings.monster_dodge_range)
            aligned = (abs(bullet.rect.centerx - self.rect.centerx) <
                       self.rect.width * 0.7 + bullet.rect.width)
            if coming and aligned and bullet not in self.decisions:
                dodge = random.random() < self.settings.monster_dodge_chance
                self.decisions[bullet] = dodge
                if dodge:
                    self.dodge_until = now + self.settings.monster_dodge_time
                    # Run away from the bullet.
                    self.direction = 1 if self.rect.centerx >= bullet.rect.centerx else -1

    def blitme(self):
        self.screen.blit(self.image, self.rect)