import pygame.font

from colors import RED, GREEN, YELLOW, WHITE


class MessageDisplay:
    """Draws the big messages: win, lose, level complete, title."""

    def __init__(self, settings, screen, stats, hero):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.hero = hero
        self.font = pygame.font.SysFont(None, 80)

    def _center_text(self, text, color, y_offset):
        image = self.font.render(text, True, color)
        rect = image.get_rect()
        rect.centerx = self.screen_rect.centerx
        rect.centery = self.screen_rect.centery + y_offset
        self.screen.blit(image, rect)

    def draw(self):
        state = self.stats.state
        reward = "Reward: +{:,}".format(self.stats.last_reward)

        if state == "playing":
            if self.hero.ammo == 0 and not self.settings.infinite_ammo:
                self._center_text("Out of ammo! Run!", RED, -100)
        elif state == "won":
            self._center_text("YOU WIN!", GREEN, -140)
            self._center_text(reward, YELLOW, -60)
        elif state == "level_complete":
            self._center_text("Level complete!", GREEN, -140)
            self._center_text(reward, YELLOW, -60)
        elif state == "lost":
            self._center_text("GAME OVER", RED, -100)
        elif state == "menu":
            self._center_text("Hero vs Monster", WHITE, -100)