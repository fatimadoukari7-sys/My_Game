import pygame

import theme


class ScrollingBackground:
    """Draws the background picture moving down (two copies stacked)."""

    def __init__(self, screen, image, speed=5):
        self.screen = screen
        self.image = image
        self.speed = speed
        self.height = image.get_height()
        self.y = 0

    def draw(self):
        self.y += self.speed
        if self.y >= self.height:
            self.y -= self.height
        self.screen.blit(self.image, (0, self.y))
        self.screen.blit(self.image, (0, self.y - self.height))


class Renderer:
    """Draws EVERYTHING on the screen, once per frame (the View).

    The game objects (Hero, Monster, Bullet, MonsterFire) only hold
    position, health and movement. How they look is decided here and in theme.py.
    """

    def __init__(self, screen, stats, background, hud, hero, monster,
                 bullets, play_button, waves=None):
        self.waves = waves          # level 3 (flying monsters), optional
        self.screen = screen
        self.stats = stats
        self.background = background
        self.hud = hud
        self.hero = hero
        self.monster = monster
        self.bullets = bullets
        self.play_button = play_button

        self.bullet_picture = self._load_bullet_picture()

    # ------------------------------------------------------------------
    # The frame
    # ------------------------------------------------------------------
    def draw(self):
        self.background.draw()

        for bullet in self.bullets.sprites():
            self._draw_bullet(bullet)
        for fire in self.monster.fires.sprites():
            self._draw_fireball(fire)

        self._draw_sprite(self.hero)
        if self.waves and self.waves.active:
            for enemy in self.waves.enemies.sprites():      # level 3
                self._draw_sprite(enemy)
        else:
            self._draw_sprite(self.monster)                 # levels 1-2
        self.hud.show()

        if self.stats.state != "playing":
            self.play_button.draw_button()

        pygame.display.flip()

    # ------------------------------------------------------------------
    # How each object looks
    # ------------------------------------------------------------------
    def _draw_sprite(self, sprite):
        """The hero and the monster: their current picture at their position."""
        self.screen.blit(sprite.image, sprite.rect)

    def _draw_bullet(self, bullet):
        """A picture if theme.BULLET_IMAGE is set, otherwise a colored ball."""
        if self.bullet_picture:
            self.screen.blit(self.bullet_picture, bullet.rect)
        else:
            pygame.draw.ellipse(self.screen, theme.BULLET_COLOR, bullet.rect)

    def _draw_fireball(self, fire):
        pygame.draw.ellipse(self.screen, theme.FIREBALL_OUTER_COLOR, fire.rect)
        pygame.draw.ellipse(self.screen, theme.FIREBALL_INNER_COLOR,
                            fire.rect.inflate(-10, -10))

    @staticmethod
    def _load_bullet_picture():
        """The bullet picture from the theme, or None (draw a ball)."""
        if not theme.BULLET_IMAGE:
            return None
        try:
            image = pygame.image.load(theme.BULLET_IMAGE).convert_alpha()
            return pygame.transform.smoothscale(image, theme.BULLET_SIZE)
        except (pygame.error, FileNotFoundError) as error:
            print("Renderer: could not load '%s' (%s)" % (theme.BULLET_IMAGE, error))
            return None