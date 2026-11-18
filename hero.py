import pygame
from pygame.sprite import Sprite


class Hero(Sprite):
    """The hero: position, health, ammo. Pictures come from HeroImages.

    It does not draw itself: the Renderer draws it.
    """

    FIRE_FLASH = 150   # ms to keep the "fire" picture after shooting

    def __init__(self, settings, screen, images):
        super().__init__()
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.images = images

        self.image = images.default
        self.rect = self.image.get_rect()   # must exist before reset()
        self.reset()

    def reset(self):
        self.image = self.images.default
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.firing = False
        self.fire_until = 0
        self.last_hit = -10 ** 9

        self.health = self.settings.hero_health
        self.ammo = self.settings.ammo_limit

    def start_fire(self):
        self.firing = True
        self.fire_until = pygame.time.get_ticks() + self.FIRE_FLASH

    def stop_fire(self):
        self.firing = False

    def take_damage(self):
        """Lose one life. Returns False during the protection time."""
        now = pygame.time.get_ticks()
        if now - self.last_hit < self.settings.hit_cooldown:
            return False
        self.last_hit = now
        self.health -= 1
        return True

    def update(self):
        speed = self.settings.hero_speed_factor
        if self.moving_right:
            self.x += speed
        if self.moving_left:
            self.x -= speed
        if self.moving_up:
            self.y -= speed
        if self.moving_down:
            self.y += speed

        self.image = self.images.choose(self, pygame.time.get_ticks())
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        # Stay inside the screen.
        self.rect.clamp_ip(self.screen_rect)
        self.x, self.y = float(self.rect.centerx), float(self.rect.centery)