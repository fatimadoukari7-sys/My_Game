import pygame
from pygame.sprite import Sprite


class Hero(Sprite):
    """The player's character."""

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load('images/mega-ball.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.reset()

    def reset(self):
        """Put the hero at the bottom center with full health and ammo."""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.health = self.settings.hero_health
        self.ammo = self.settings.ammo_limit
        self.last_hit_time = -10 ** 9

    def update(self):
        speed = self.settings.hero_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += speed
        if self.moving_left and self.rect.left > 0:
            self.center_x -= speed
        if self.moving_up and self.rect.top > 0:
            self.center_y -= speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += speed

        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

    def take_damage(self):
        """Lose one health point unless still protected. Return True if hit."""
        now = pygame.time.get_ticks()
        if now - self.last_hit_time > self.settings.hit_cooldown:
            self.health -= 1
            self.last_hit_time = now
            return True
        return False

    def blitme(self):
        # Blink while protected after a hit.
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.settings.hit_cooldown and (now // 100) % 2 == 0:
            return
        self.screen.blit(self.image, self.rect)