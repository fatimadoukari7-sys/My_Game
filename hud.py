import pygame.font
import pygame.transform

from health_bar import HealthBar

from health_bar import HealthBar

TEXT_COLOR = (30, 130, 230)
RED = (230, 40, 40)
GREEN = (60, 220, 90)
YELLOW = (255, 220, 60)
WHITE = (255, 255, 255)


class ScoreDisplay:
    """The score, top right."""

    def __init__(self, screen, stats, font):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.font = font
        self.prep()

    def prep(self):
        text = "Score: " + "{:,}".format(int(self.stats.score))
        self.image = self.font.render(text, True, TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.right = self.screen_rect.right - 20
        self.rect.top = 10

    def show(self):
        self.screen.blit(self.image, self.rect)


class HighScoreDisplay:
    """The high score, top center."""

    def __init__(self, screen, stats, font):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.font = font
        self.prep()

    def prep(self):
        text = "High Score: " + "{:,}".format(int(self.stats.high_score))
        self.image = self.font.render(text, True, TEXT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = 10

    def show(self):
        self.screen.blit(self.image, self.rect)


class MonsterBarDisplay:
    """The monster health bar, right below the high score (only while playing)."""

    def __init__(self, screen, stats, monster, anchor_display):
        self.stats = stats
        self.monster = monster
        self.anchor = anchor_display       # the bar follows this display
        self.bar = HealthBar(screen, left=0, top=0, width=100)

    def show(self):
        if self.stats.state != "playing":
            return
        anchor = self.anchor.rect
        self.bar.rect.width = anchor.width
        self.bar.rect.centerx = anchor.centerx
        self.bar.rect.top = anchor.bottom + 8
        self.bar.draw(self.monster.health, self.monster.max_health)


class AmmoDisplay:
    """The ammo counter (hidden on levels with infinite ammo)."""

    def __init__(self, settings, screen, hero, font, score_display):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.hero = hero
        self.font = font
        self.score_display = score_display

    def show(self):
        if self.settings.infinite_ammo:
            return
        ammo = self.hero.ammo
        color = RED if ammo < 3 else TEXT_COLOR
        image = self.font.render("Ammo: " + str(ammo), True, color)
        rect = image.get_rect()
        rect.right = self.screen_rect.right - 20
        rect.top = self.score_display.rect.bottom + 10
        self.screen.blit(image, rect)


class HealthDisplay:
    """The hero's lives, drawn as small hero pictures."""

    def __init__(self, screen, hero):
        self.screen = screen
        self.hero = hero
        hw, hh = hero.image.get_size()
        self.heart = pygame.transform.smoothscale(
            hero.image, (max(1, int(hw * 30 / hh)), 30))

    def show(self):
        for i in range(max(self.hero.health, 0)):
            self.screen.blit(self.heart, (10 + i * 35, 10))


class LevelDisplay:
    def __init__(self, settings, screen, stats, font):
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.font = font

    def show(self):
        text = "Level: {}/{}".format(self.stats.level + 1, len(self.settings.levels))
        self.screen.blit(self.font.render(text, True, TEXT_COLOR), (10, 50))


class MessageDisplay:
    """The big centered messages (win, game over, ...)."""

    def __init__(self, settings, screen, stats, hero):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.hero = hero

        self.text_color = (30, 130, 230)
        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 80)

        # Small copy of the hero image used as a "heart".
        self.heart = pygame.transform.scale(hero.image, (30, 30))

        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        score_str = "{:,}".format(int(self.stats.score))
        self.score_image = self.font.render("Score: " + score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        high_str = "{:,}".format(int(self.stats.high_score))
        self.high_score_image = self.font.render("High Score: " + high_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 10

    def _center_text(self, text, color, y_offset):
        image = self.font.render(text, True, color)
        rect = image.get_rect()
        rect.centerx = self.screen_rect.centerx
        rect.centery = self.screen_rect.centery + y_offset
        self.screen.blit(image, rect)

    def show(self):
        # Score and high score.
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # Ammo (red when low).
        ammo = self.hero.ammo
        color = (230, 40, 40) if ammo < 3 else self.text_color
        ammo_image = self.font.render("Ammo: " + str(ammo), True, color)
        ammo_rect = ammo_image.get_rect()
        ammo_rect.right = self.screen_rect.right - 20
        ammo_rect.top = self.score_rect.bottom + 10
        self.screen.blit(ammo_image, ammo_rect)

        # Health.
        for i in range(max(self.hero.health, 0)):
            self.screen.blit(self.heart, (10 + i * 35, 10))

        # Status messages.
        state = self.stats.state
        reward = "Reward: +{:,}".format(self.stats.last_reward)
        if state == "playing":
            if self.hero.ammo == 0 and not self.settings.infinite_ammo:
                self._center_text("Out of ammo! Run!", RED, -100)
        elif state == "won":
            self._center_text("YOU WIN!", GREEN, -140)
            self._center_text(reward, YELLOW, -60)
        elif state == "lost":
            self._center_text("GAME OVER", RED, -100)
        elif state == "menu":
            self._center_text("Hero vs Monster", (255, 255, 255), -100)