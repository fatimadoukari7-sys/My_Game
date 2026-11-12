from monster_profile import MonsterProfile, register


@register
class Pikachu(MonsterProfile):

    level = 1
    health = 3
    speed = 4
    chase_speed = 5
    dodge_chance = 0.4
    ammo = 20

    image = "images/pikachu.png"
    scale = 1.0
