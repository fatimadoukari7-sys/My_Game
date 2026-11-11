import pygame.font
import pygame.transform

from health_bar import HealthBar

TEXT_COLOR = (30, 130, 230)
RED = (230, 40, 40)
GREEN = (60, 220, 90)
YELLOW = (255, 220, 60)
WHITE = (255, 255, 255)


class HUD:
    """Draws score, health, ammo, level, monster bar and messages."""

    def __init__(self, settings, screen, stats, hero, monster):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.hero = hero
        self.monster = monster

        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 80)
        self.monster_bar = HealthBar(screen, 0, 0, 200)

        # Small copy of the hero image used as a "heart".
        hw, hh = hero.image.get_size()
        self.heart = pygame.transform.smoothscale(
            hero.image, (max(1, int(hw * 30 / hh)), 30))

        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        text = "Score: {:,}".format(int(self.stats.score))
        self.score_image = self.font.render(text, True, TEXT_COLOR)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        text = "High Score: {:,}".format(int(self.stats.high_score))
        self.high_score_image = self.font.render(text, True, TEXT_COLOR)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 10

    def _center_text(self, text, color, y_offset):
        image = self.big_font.render(text, True, color)
        rect = image.get_rect()
        rect.centerx = self.screen_rect.centerx
        rect.centery = self.screen_rect.centery + y_offset
        self.screen.blit(image, rect)

    def show(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # Ammo (hidden on levels with infinite ammo).
        if not self.settings.infinite_ammo:
            ammo = self.hero.ammo
            color = RED if ammo < 3 else TEXT_COLOR
            ammo_image = self.font.render("Ammo: " + str(ammo), True, color)
            ammo_rect = ammo_image.get_rect()
            ammo_rect.right = self.screen_rect.right - 20
            ammo_rect.top = self.score_rect.bottom + 10
            self.screen.blit(ammo_image, ammo_rect)

        # Health.
        for i in range(max(self.hero.health, 0)):
            self.screen.blit(self.heart, (10 + i * 35, 10))

        # Level.
        level_text = "Level: {}/{}".format(
            self.stats.level + 1, len(self.settings.levels))
        self.screen.blit(self.font.render(level_text, True, TEXT_COLOR), (10, 50))

        # Monster health bar (only while playing).
        state = self.stats.state
        if state == "playing":
            bar = self.monster_bar
            bar.rect.centerx = self.high_score_rect.centerx
            bar.rect.top = self.high_score_rect.bottom + 8
            bar.draw(self.monster.health, self.monster.max_health)

        # Messages.
        if state == "playing":
            if self.hero.ammo == 0 and not self.settings.infinite_ammo:
                self._center_text("Out of ammo! Run!", RED, -100)
        elif state == "won":
            self._center_text("YOU WIN!", GREEN, -140)
            self._center_text("Reward: +{:,}".format(self.stats.last_reward),
                              YELLOW, -60)
        elif state == "level_complete":
            self._center_text("Level complete!", GREEN, -140)
            self._center_text("Reward: +{:,}".format(self.stats.last_reward),
                              YELLOW, -60)
        elif state == "lost":
            self._center_text("GAME OVER", RED, -100)
        elif state == "menu":
            self._center_text("Hero vs Monster", WHITE, -100)