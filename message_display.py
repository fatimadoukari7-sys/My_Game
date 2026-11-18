import pygame.font

import theme
from colors import RED, GREEN, YELLOW, WHITE


class MessageDisplay:
    """Draws the big messages: win, lose, level complete, title."""

    def __init__(self, settings, screen, stats, hero):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.hero = hero
        self.font = pygame.font.SysFont(None, theme.FONT_BIG)

    def _center_text(self, text, color, y_offset):
        image = self.font.render(text, True, color)
        rect = image.get_rect()
        rect.centerx = self.screen_rect.centerx
        rect.centery = self.screen_rect.centery + y_offset
        self.screen.blit(image, rect)

    def draw(self):
        texts = theme.TEXTS
        state = self.stats.state
        reward = texts["reward"].format(self.stats.last_reward)

        if state == "playing":
            if self.hero.ammo == 0 and not self.settings.infinite_ammo:
                self._center_text(texts["out_of_ammo"], RED, -100)
        elif state == "won":
            self._center_text(texts["win"], GREEN, -140)
            self._center_text(reward, YELLOW, -60)
        elif state == "level_complete":
            self._center_text(texts["level_complete"], GREEN, -140)
            self._center_text(reward, YELLOW, -60)
        elif state == "lost":
            self._center_text(texts["game_over"], RED, -100)
        elif state == "menu":
            self._center_text(texts["title"], WHITE, -100)