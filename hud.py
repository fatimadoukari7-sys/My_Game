import pygame.font
import pygame.transform


class HUD():
    """Draws score, health, ammo and status messages."""

    def __init__(self, settings, screen, stats, hero):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
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
        image = self.big_font.render(text, True, color)
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
        if state == "playing":
            if self.hero.ammo == 0:
                self._center_text("Out of ammo! Run!", (230, 40, 40), -100)
        elif state == "won":
            self._center_text("YOU WIN!", (60, 220, 90), -140)
            self._center_text("Reward: +{:,}".format(self.stats.last_reward),
                              (255, 220, 60), -60)
        elif state == "lost":
            self._center_text("GAME OVER", (230, 40, 40), -100)
        elif state == "menu":
            self._center_text("Hero vs Monster", (255, 255, 255), -100)