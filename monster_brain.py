import math
import random


class MonsterBrain:
    """The monster's movement AI: patrol, dodge bullets and chase the hero."""

    def __init__(self, profile, screen_rect):
        self.profile = profile
        self.screen_rect = screen_rect
        self.reset()

    def reset(self):
        self.direction = random.choice((-1, 1))
        self.dodge_until = 0
        self.decisions = {}   # bullet -> did we decide to dodge it?

    def clear_dodge(self):
        self.dodge_until = 0
        self.decisions = {}

    def update(self, monster, bullets, hero, now):
        if hero.ammo == 0 and len(bullets) == 0:
            self._chase(monster, hero)
        else:
            self._patrol(monster, bullets, now)

    def _chase(self, monster, hero):
        dx = hero.rect.centerx - monster.rect.centerx
        dy = hero.rect.centery - monster.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            speed = self.profile.chase_speed
            monster.x += dx / dist * speed
            monster.y += dy / dist * speed

    def _patrol(self, monster, bullets, now):
        self._decide_dodge(monster, bullets, now)

        speed = self.profile.speed
        if now < self.dodge_until:
            speed *= 1.6
        elif random.random() < 0.01:
            self.direction *= -1          # random change of mind

        monster.x += self.direction * speed

        width = monster.rect.width
        if monster.x <= 0:
            monster.x = 0
            self.direction = 1
        elif monster.x + width >= self.screen_rect.right:
            monster.x = self.screen_rect.right - width
            self.direction = -1

        # Drift back to the top area.
        if monster.y > monster.home_y:
            monster.y -= 2
        elif monster.y < monster.home_y:
            monster.y += 2

    def _decide_dodge(self, monster, bullets, now):
        # Forget bullets that no longer exist.
        self.decisions = {b: d for b, d in self.decisions.items() if b.alive()}

        for bullet in bullets:
            coming = (bullet.rect.top > monster.rect.top and
                      bullet.rect.top - monster.rect.bottom < self.profile.dodge_range)
            aligned = (abs(bullet.rect.centerx - monster.rect.centerx) <
                       monster.rect.width * 0.7 + bullet.rect.width)
            if coming and aligned and bullet not in self.decisions:
                dodge = random.random() < self.profile.dodge_chance
                self.decisions[bullet] = dodge
                if dodge:
                    self.dodge_until = now + self.profile.dodge_time
                    # Run away from the bullet.
                    self.direction = 1 if monster.rect.centerx >= bullet.rect.centerx else -1
