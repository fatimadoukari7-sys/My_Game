import pygame
from pygame.sprite import Sprite


class Hero(Sprite):
    """The player's character."""

    def __init__(self, settings, screen, images):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        self.reset()

    # ------------------------------------------------------------------
    def _load(self, path):
        """Load one picture scaled to HEIGHT, or None if it cannot be loaded."""
        try:
            raw = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError) as error:
            print("Hero: could not load '%s' (%s)" % (path, error))
            return None
        w, h = raw.get_size()
        picture = pygame.transform.smoothscale(
            raw, (max(1, int(w * self.HEIGHT / h)), self.HEIGHT))
        if self.DEBUG:
            print("Hero: loaded '%s' (%dx%d)" % (path, w, h))
        return picture

    def _load_pictures(self):
        pictures = {name: self._load(path) for name, path in self.IMAGES.items()}

        if pictures['stop'] is None:    # safety net: the game still runs
            fallback = pygame.Surface((60, self.HEIGHT), pygame.SRCALPHA)
            pygame.draw.ellipse(fallback, (80, 180, 90), fallback.get_rect())
            pictures['stop'] = fallback

        for name in pictures:           # a missing picture -> the stop picture
            if pictures[name] is None:
                pictures[name] = pictures['stop']
        return pictures

    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    def _current_picture(self, now):
        """Choose the picture: fire > right > left > up > stop."""
        if self.firing or now < self.fire_until:
            name = 'fire'
        elif self.moving_right and not self.moving_left:
            name = 'right'
        elif self.moving_left and not self.moving_right:
            name = 'left'
        elif self.moving_up and not self.moving_down:
            name = 'up'
        else:
            name = 'stop'

        if self.DEBUG and name != self.last_name:
            print("Hero: picture ->", name)
            self.last_name = name
        return self.pictures[name]

    def blitme(self):
        now = pygame.time.get_ticks()

        # Blink while protected after a hit.
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.settings.hit_cooldown and (now // 100) % 2 == 0:
            return
        self.screen.blit(self.image, self.rect)