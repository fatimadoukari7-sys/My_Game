import pygame.font
import pygame.transform

from colors import RED, TEXT_COLOR


class StatusDisplay:
    """Draws hearts, ammo and the level number."""

    def __init__(self, settings, screen, stats, hero):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.hero = hero
        self.font = pygame.font.SysFont(None, 40)
        self.heart = self._make_heart(hero.image)

    @staticmethod
    def _make_heart(image):
        """Small copy of the hero image used as a heart."""
        w, h = image.get_size()
        return pygame.transform.smoothscale(
            image, (max(1, int(w * 30 / h)), 30))

    def draw(self, anchor_rect):
        """anchor_rect: the score rect, the ammo is drawn under it."""
        self._draw_hearts()
        self._draw_level()
        self._draw_ammo(anchor_rect)

    def _draw_hearts(self):
        for i in range(max(self.hero.health, 0)):
            self.screen.blit(self.heart, (10 + i * 35, 10))

    def _draw_level(self):
        text = "Level: {}/{}".format(
            self.stats.level + 1, len(self.settings.levels))
        self.screen.blit(self.font.render(text, True, TEXT_COLOR), (10, 50))

    def _draw_ammo(self, anchor_rect):
        if self.settings.infinite_ammo:
            return
        ammo = self.hero.ammo
        color = RED if ammo < 3 else TEXT_COLOR
        image = self.font.render("Ammo: " + str(ammo), True, color)
        rect = image.get_rect()
        rect.right = self.screen_rect.right - 20
        rect.top = anchor_rect.bottom + 10
        self.screen.blit(image, rect)