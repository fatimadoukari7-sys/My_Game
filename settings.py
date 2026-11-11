from levels import LEVELS


class Settings():
    """Stores the game settings and applies the settings of a level."""

    def __init__(self):
        # Screen (overwritten in main.py by the background size).
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (22, 20, 25)

        # Hero.
        self.hero_speed_factor = 4.3
        self.hero_health = 3
        self.ammo_limit = 12          # total bullets the hero has
        self.hit_cooldown = 1000      # ms of protection after being hit

        # Bullet.
        self.bullet_width = 23
        self.bullet_height = 23
        self.bullet_color = (255, 220, 60)
        self.bullet_speed_factor = 7
        self.bullets_allowed = 3      # max bullets on screen at once

        # Monster (general).
        self.monster_dodge_range = 220    # distance at which it notices a bullet
        self.monster_dodge_time = 400     # ms of fast sideways dodge
        self.monster_jump_min = 3000      # ms between re-entrances (level 2)
        self.monster_jump_max = 6000
        self.monster_fire_size = 24
        self.monster_fire_speed = 5
        self.monster_fire_interval = 1500  # ms between fireballs

        # Rewards.
        self.win_reward = 1000
        self.ammo_bonus = 50              # per remaining bullet

        # Levels.
        self.levels = LEVELS
        self.apply_level(0)

    def apply_level(self, index):
        """Copy the settings of one level into the game settings."""
        level = self.levels[index]
        self.monster_health = level["monster_health"]
        self.monster_speed = level["monster_speed"]
        self.monster_chase_speed = level["monster_chase_speed"]
        self.monster_dodge_chance = level["monster_dodge_chance"]
        self.ammo_limit = level["ammo"]
        self.monster_image = level["image"]
        self.monster_scale = level["scale"]
        self.monster_multi_side = level["multi_side"]
        self.infinite_ammo = level["infinite_ammo"]
        self.monster_shoots = level["shoots"]