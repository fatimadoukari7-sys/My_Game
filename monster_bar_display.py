from health_bar import HealthBar


class MonsterBarDisplay:
    """Draws the monster's health bar. Knows where to put it, not how to draw it."""

    def __init__(self, screen, stats, monster):
        self.stats = stats
        self.monster = monster
        self.bar = HealthBar(screen, 0, 0, 200)

    def draw(self, anchor_rect):
        """anchor_rect: the high score rect, the bar is placed under it."""
        if self.stats.state != "playing":
            return
        self.bar.rect.centerx = anchor_rect.centerx
        self.bar.rect.top = anchor_rect.bottom + 8
        self.bar.draw(self.monster.health, self.monster.max_health)