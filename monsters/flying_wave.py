"""Level 3: waves of flying monsters. Kill 20 to win.

The picture is chosen in theme.py (FLYING_ENEMY).
"""

import theme
from monster_profile import MonsterProfile, register


@register
class FlyingWave(MonsterProfile):

    level = 3
    wave_mode = True            # tells the game to use waves, not one monster

    kills_to_win = 20           # the win condition
    points_per_kill = 50        # score for every flying monster killed
    start_count = 2             # monsters on the screen at the start
    max_count = 6               # never more than this at the same time
    kills_per_extra = 4         # one more monster every 4 kills
    base_speed = 2.0            # starting speed
    speed_gain = 0.12           # speed added with every kill

    ammo = 20
    infinite_ammo = True        # the hero needs many bullets in this level

    # The single Monster object still exists but is not used in this level.
    image = theme.FLYING_ENEMY["image"]