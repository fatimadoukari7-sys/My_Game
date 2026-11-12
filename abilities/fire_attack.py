from monster_gun import MonsterGun


class FireAttack:
    """قدرة إطلاق الكرات النارية."""

    def __init__(self, profile, screen):
        self.gun = MonsterGun(profile, screen)

    @property
    def fires(self):
        return self.gun.fires

    def reset(self, now):
        self.gun.reset(now)

    def update(self, monster, hero, now):
        self.gun.try_fire(monster, hero, now)
