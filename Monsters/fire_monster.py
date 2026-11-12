from monster_profile import MonsterProfile, register
from monster_gun import MonsterGun


@register
class FireMonster(MonsterProfile):
    """المستوى 2: يطلق النار، وذخيرة البطل غير محدودة."""
    level = 2
    health = 5
    speed = 5
    chase_speed = 6.5
    dodge_chance = 0.6
    ammo = 22
    infinite_ammo = True
    image = "images/monster_lev2.png"
    scale = 0.25

    def make_gun(self, screen):
        return MonsterGun(self, screen)