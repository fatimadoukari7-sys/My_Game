from pygame.sprite import Group

from monster_fire import MonsterFire


class MonsterGun:
    """Decides WHEN the monster shoots and keeps its fireballs."""

    FIRST_SHOT_DELAY = 1500

    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.fires = Group()
        self.next_shot = 0

    def reset(self, now):
        self.fires.empty()
        self.next_shot = now + self.FIRST_SHOT_DELAY

    def try_fire(self, monster, hero, now):
        if now >= self.next_shot:
            self.fires.add(MonsterFire(self.settings, self.screen, monster, hero))
            self.next_shot = now + self.settings.monster_fire_interval