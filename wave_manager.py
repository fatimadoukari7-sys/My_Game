import pygame
from pygame.sprite import Group

from flying_enemy import FlyingEnemy


class WaveManager:
    """Level 3: creates the flying monsters and makes the game harder.

    The more the hero kills, the more monsters are on the screen and the
    faster they fly. The numbers come from the level's profile
    (monsters/flying_wave.py). It does not check collisions (WaveCombat does)
    and it does not draw (Renderer does).
    """

    FIRST_DELAY = 800      # ms before the first monster
    SPAWN_GAP = 700        # ms between two new monsters

    def __init__(self, settings, screen, hero):
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.hero = hero

        self.enemies = Group()
        self.active = False
        self.kills = 0
        self.goal = 0
        self.points_per_kill = 0
        self.profile = None
        self.next_spawn = 0
        self.reset()

    def reset(self):
        """Called every time a level starts."""
        self.profile = self.settings.monster_profile
        self.active = getattr(self.profile, "wave_mode", False)
        self.kills = 0
        self.goal = getattr(self.profile, "kills_to_win", 20)
        self.points_per_kill = getattr(self.profile, "points_per_kill", 0)
        self.enemies.empty()
        self.next_spawn = pygame.time.get_ticks() + self.FIRST_DELAY

    # ------------------------------------------------------------------
    @property
    def wanted_count(self):
        """How many monsters should be flying now."""
        p = self.profile
        return min(p.max_count, p.start_count + self.kills // p.kills_per_extra)

    @property
    def speed(self):
        """How fast they fly now."""
        p = self.profile
        return p.base_speed + p.speed_gain * self.kills

    @property
    def complete(self):
        return self.kills >= self.goal

    def add_kill(self):
        self.kills += 1

    # ------------------------------------------------------------------
    def update(self):
        if not self.active:
            return

        for enemy in self.enemies.copy():
            enemy.speed = self.speed
            enemy.update()
            if enemy.is_below_screen:      # missed: it just disappears
                enemy.kill()

        now = pygame.time.get_ticks()
        if len(self.enemies) < self.wanted_count and now >= self.next_spawn:
            self.enemies.add(FlyingEnemy(self.screen_rect, self.hero, self.speed))
            self.next_spawn = now + self.SPAWN_GAP