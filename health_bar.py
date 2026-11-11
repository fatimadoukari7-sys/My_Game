import pygame


class HealthBar():
    """A wide health bar fixed at the top of the screen.

    It only knows numbers (health and max health) and where to draw.
    The bar starts full and green, shrinks with every hit and turns red.
    """

    def __init__(self, screen, left, top, width, height=14):
        self.screen = screen
        self.rect = pygame.Rect(left, top, width, height)

        self.back_color = (40, 40, 40)
        self.border_color = (15, 15, 15)
        self.full_color = (60, 220, 90)     # green: full health
        self.low_color = (230, 40, 40)      # red: almost no health

    def _color(self, ratio):
        """Green when full, red when low, a mix in between."""
        t = max(0.0, min((ratio - 0.3) / 0.6, 1.0))    # 0 = red ... 1 = green
        return tuple(int(low + (full - low) * t)
                     for low, full in zip(self.low_color, self.full_color))

    def draw(self, health, max_health):
        if max_health <= 0:
            return
        ratio = max(0.0, min(health / max_health, 1.0))
        radius = self.rect.height // 2

        pygame.draw.rect(self.screen, self.back_color, self.rect,
                         border_radius=radius)

        if ratio > 0:
            fill = self.rect.copy()
            fill.width = max(int(self.rect.width * ratio), self.rect.height)
            pygame.draw.rect(self.screen, self._color(ratio), fill,
                             border_radius=radius)

        pygame.draw.rect(self.screen, self.border_color, self.rect, 2,
                         border_radius=radius)