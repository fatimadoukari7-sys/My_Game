from pygame.sprite import Group

from damage.damage_strategy import NormalDamage


class NoEntrance:

    active = False

    def reset(self):
        pass

    def is_time_to_jump(self, now):
        return False

    def start(self, monster):
        pass

    def move(self, monster):
        pass


class NoGun:

    def __init__(self):
        self.fires = Group()

    def reset(self, now):
        self.fires.empty()

    def try_fire(self, monster, hero, now):
        pass


REGISTRY = []


def register(cls):
    REGISTRY.append(cls)
    REGISTRY.sort(key=lambda c: c.level)
    return cls


class MonsterProfile:

    level = 0
    health = 3
    speed = 4
    chase_speed = 5
    dodge_chance = 0.4
    dodge_range = 220
    dodge_time = 400
    image = None
    scale = 1.0
    ammo = 20
    infinite_ammo = False
    jump_min = 3000
    jump_max = 6000
    fire_size = 24
    fire_speed = 5
    fire_interval = 1500

    def make_entrance(self, screen_rect):
        return NoEntrance()

    def make_gun(self, screen):
        return NoGun()

    def make_ability(self, screen):
        return None

    def make_damage_strategy(self):
        return NormalDamage()