import theme
from monster_profile import REGISTRY
import monsters   # noqa: F401  (loading it registers every monster)
import monsters.flying_wave   # noqa: F401  (level 3: makes sure it is registered)

# ----------------------------------------------------------------------
# WHICH LEVELS ARE IN THE GAME
#   None       -> all the levels (the normal game)
#   [3]        -> only level 3
#   [1, 3]     -> levels 1 and 3 (level 2 is hidden)
#   [2, 3]     -> levels 2 and 3 ...
# The number of a level is `level = N` inside its file in monsters/.
# ----------------------------------------------------------------------
ENABLED_LEVELS = [1,2,3]


class Settings():
    """Stores the general game settings. Monster power lives in monsters/.

    Looks (colors, sizes, pictures) come from theme.py.
    """

    def __init__(self):
        # Screen (overwritten in main.py by the background size).
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = theme.BACKGROUND_COLOR

        # Hero.
        self.hero_speed_factor = 4.3
        self.hero_health = 3
        self.ammo_limit = 12          # set by apply_level
        self.infinite_ammo = False    # set by apply_level
        self.hit_cooldown = 1000      # ms of protection after being hit

        # Bullet (the look comes from theme.py).
        self.bullet_width, self.bullet_height = theme.BULLET_SIZE
        self.bullet_color = theme.BULLET_COLOR
        self.bullet_speed_factor = 7
        self.bullets_allowed = 3      # max bullets on screen at once

        # Rewards.
        self.win_reward = 1000
        self.ammo_bonus = 50              # per remaining bullet

        # Levels = the registered monsters, filtered by ENABLED_LEVELS.
        self.levels = [c for c in REGISTRY
                       if ENABLED_LEVELS is None or c.level in ENABLED_LEVELS]
        if not self.levels:
            raise ValueError(
                "ENABLED_LEVELS = %r matches no level. Registered levels: %r"
                % (ENABLED_LEVELS, [c.level for c in REGISTRY]))
        self.apply_level(0)

    def apply_level(self, index):
        """Create the monster profile of this level."""
        profile = self.levels[index]()
        self.monster_profile = profile
        self.ammo_limit = profile.ammo
        self.infinite_ammo = profile.infinite_ammo

        # Level 3 uses waves of flying monsters instead of one monster.
        self.wave_mode = getattr(profile, "wave_mode", False)

        # The monster's picture for this level (None = use the profile's own).
        if self.wave_mode:
            self.monster_look = None
        elif index < len(theme.MONSTER_LOOKS):
            self.monster_look = theme.MONSTER_LOOKS[index]
        else:
            self.monster_look = None