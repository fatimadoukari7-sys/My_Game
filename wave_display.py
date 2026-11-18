import pygame.font

import theme
from colors import TEXT_COLOR


class WaveDisplay:
    """Level 3 information: how many monsters were killed out of the goal."""

    def __init__(self, screen, stats, waves):
        self.screen = screen
        self.stats = stats
        self.waves = waves
        self.font = pygame.font.SysFont(None, theme.FONT_SMALL)

    def draw(self, anchor_rect):
        """anchor_rect: the high score rect, the text is placed under it."""
        if self.stats.state != "playing":
            return
        text = theme.TEXTS["kills"].format(self.waves.kills, self.waves.goal)
        image = self.font.render(text, True, TEXT_COLOR)
        rect = image.get_rect()
        rect.centerx = anchor_rect.centerx
        rect.top = anchor_rect.bottom + 8
        self.screen.blit(image, rect)