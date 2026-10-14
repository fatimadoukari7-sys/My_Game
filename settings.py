class Settings():
    """Stores all settings for the game."""

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

        # Monster.
        self.monster_speed = 5            # faster than the hero
        self.monster_chase_speed = 6.5    # when the hero is out of ammo
        self.monster_dodge_range = 220    # distance at which it notices a bullet
        self.monster_dodge_chance = 0.6   # chance to dodge a bullet
        self.monster_dodge_time = 400     # ms of fast sideways dodge

        # Rewards.
        self.win_reward = 1000
        self.ammo_bonus = 50              # per remaining bullet