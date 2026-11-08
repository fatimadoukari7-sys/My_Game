import pygame.font
import pygame.transform

from health_bar import HealthBar


class HUD():
    """Draws score, health, ammo and status messages."""

    def __init__(self, settings, screen, stats, hero, monster):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.hero = hero
        self.monster = monster
        # Wide bar under the top row, left of the ammo text.
        
        self.monster_bar = HealthBar(screen, left=0, top=0, width=100)

        self.text_color = (30, 130, 230)
        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 80)

        # Small copy of the hero image used as a "heart".
        hw, hh = hero.image.get_size()
        self.heart = pygame.transform.smoothscale(
            hero.image, (max(1, int(hw * 30 / hh)), 30))

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
        # The monster bar is as wide as the high score text, right below it.
        self.monster_bar.rect.width = self.high_score_rect.width
        self.monster_bar.rect.centerx = self.high_score_rect.centerx
        self.monster_bar.rect.top = self.high_score_rect.bottom + 8

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

        # Monster health bar (drawn by its own component, only while playing).
        if self.stats.state == "playing":
            self.monster_bar.draw(self.monster.health, self.monster.max_health)

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
