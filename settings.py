from monster_profile import REGISTRY
import monsters   # noqa: F401  (loading it registers every monster)


class Settings():
    """Stores the general game settings. Monster power lives in monsters/."""

    def __init__(self):
        # Screen (overwritten in main.py by the background size).
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (22, 20, 25)

        # Hero.
        self.hero_speed_factor = 4.3
        self.hero_health = 3
        self.ammo_limit = 12          # set by apply_level
        self.infinite_ammo = False    # set by apply_level
        self.hit_cooldown = 1000      # ms of protection after being hit

        # Bullet.
        self.bullet_width = 23
        self.bullet_height = 23
        self.bullet_color = (255, 220, 60)
        self.bullet_speed_factor = 7
        self.bullets_allowed = 3      # max bullets on screen at once

        # Rewards.
        self.win_reward = 1000
        self.ammo_bonus = 50              # per remaining bullet

        # Levels = the registered monsters (same name as before).
        self.levels = REGISTRY
        self.apply_level(0)

    def apply_level(self, index):
        """Create the monster profile of this level."""
        profile = self.levels[index]()
        self.monster_profile = profile
        self.ammo_limit = profile.ammo
        self.infinite_ammo = profile.infinite_ammo
