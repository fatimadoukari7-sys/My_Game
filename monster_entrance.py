import math
import random

import pygame


class MonsterEntrance:
    """Level 2 behavior: the monster leaves and re-enters from a random side."""

    MARGIN = 20

    def __init__(self, settings, screen_rect):
        self.settings = settings
        self.screen_rect = screen_rect
        self.active = False       # True while the monster is flying in
        self.target_x = 0.0
        self.target_y = 0.0
        self.next_jump = 0

    def reset(self):
        self.active = False

    def is_time_to_jump(self, now):
        return now >= self.next_jump

    def start(self, monster):
        """Place the monster outside the screen and choose where it lands."""
        width, height = monster.rect.size
        right_limit = max(self.MARGIN, self.screen_rect.right - width - self.MARGIN)
        self.target_x = random.randint(self.MARGIN, right_limit)
        self.target_y = random.randint(70, int(self.screen_rect.height * 0.4))

        side = random.choice(("top", "left", "right"))
        if side == "top":
            monster.x, monster.y = self.target_x, -height
        elif side == "left":
            monster.x, monster.y = -width, self.target_y
        else:
            monster.x, monster.y = self.screen_rect.right, self.target_y

        self.active = True
        monster.rect.x = int(monster.x)
        monster.rect.y = int(monster.y)

        self.next_jump = pygame.time.get_ticks() + random.randint(
            self.settings.monster_jump_min, self.settings.monster_jump_max)

    def move(self, monster):
        """Fly toward the landing point."""
        dx = self.target_x - monster.x
        dy = self.target_y - monster.y
        dist = math.hypot(dx, dy)
        speed = self.settings.monster_speed * 1.6
        if dist <= speed:
            monster.x, monster.y = self.target_x, self.target_y
            monster.home_y = self.target_y
            self.active = False
        else:
            monster.x += dx / dist * speed
            monster.y += dy / dist * speed