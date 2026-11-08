import pygame
from pygame.sprite import Sprite


class Hero(Sprite):
    """The player's character. The picture depends on what the player does."""

    HEIGHT = 90        # height of the hero on the screen (pixels)
    FIRE_TIME = 200    # ms the "fire" picture stays after the fire key is pressed

    # The picture of each state (files inside the images folder).
    # The names are case sensitive on Linux: they must match the files exactly.
    IMAGES = {
        'stop':  'images/Gerero/gereroStop.png',   # nothing is pressed
        'fire':  'images/Gerero/Gerero.png',       # fire key (space)
        'left':  'images/Gerero/left1.png',        # left arrow
        'right': 'images/Gerero/right.png',        # right arrow
        'up':    'images/Gerero/up.png',           # up arrow
    }

    # While True, the terminal shows which picture loaded and which one is
    # used. Set it to False when everything works.
    DEBUG = True

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        self.pictures = self._load_pictures()
        self.image = self.pictures['stop']      # also used by the HUD (lives)

        # The hit box is the same whatever picture is shown.
        w, h = self.image.get_size()
        self.rect = pygame.Rect(0, 0, int(w * 0.8), int(h * 0.9))

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

        self.firing = False        # True while the fire key is held down
        self.fire_until = 0        # the fire picture is shown until this time
        self.last_name = None      # only used by the DEBUG messages

        self.health = self.settings.hero_health
        self.ammo = self.settings.ammo_limit
        self.last_hit_time = -10 ** 9

    def start_fire(self):
        """Called when the fire key is pressed."""
        self.firing = True
        self.fire_until = pygame.time.get_ticks() + self.FIRE_TIME

    def stop_fire(self):
        """Called when the fire key is released."""
        self.firing = False

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
        if now - self.last_hit_time < self.settings.hit_cooldown and (now // 100) % 2 == 0:
            return

        picture = self._current_picture(now)
        self.screen.blit(picture, picture.get_rect(center=self.rect.center))
