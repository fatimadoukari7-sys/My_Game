"""Level data only. To add a level, add a dictionary here."""

LEVELS = [
    # Level 1: Pikachu, normal ammo, no fire.
    {"monster_health": 3, "monster_speed": 4, "monster_chase_speed": 5,
     "monster_dodge_chance": 0.4, "ammo": 20,
     "image": "images/pikachu.png", "scale": 1.0,
     "multi_side": False, "infinite_ammo": False, "shoots": False},

    # Level 2: moves like level 1, shoots fire, unlimited ammo.
    {"monster_health": 5, "monster_speed": 5, "monster_chase_speed": 6.5,
     "monster_dodge_chance": 0.6, "ammo": 22,
     "image": "images/monster_lev2.png", "scale": 0.25,
     "multi_side": False, "infinite_ammo": True, "shoots": True},
]