from monster_profile import MonsterProfile, register
from abilities.fire_attack import FireAttack


@register
class FireMonster(MonsterProfile):
    """المستوى 2: وحش يمتلك قدرة إطلاق الكرات النارية."""

    level = 2
    health = 5
    speed = 5
    chase_speed = 6.5
    dodge_chance = 0.6
    ammo = 22
    infinite_ammo = True
    image = "images/monster_lev2.png"
    scale = 0.25

    def make_ability(self, screen):
        return FireAttack(self, screen)
