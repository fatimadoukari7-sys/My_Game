from pygame.sprite import Group


class NoEntrance:
    """وحش بلا دخول عشوائي (Null Object): لا يفعل شيئاً."""
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
    """وحش لا يطلق النار (Null Object)."""

    def __init__(self):
        self.fires = Group()

    def reset(self, now):
        self.fires.empty()

    def try_fire(self, monster, hero, now):
        pass


REGISTRY = []   # قائمة كلاسات الوحوش، مرتبة حسب level


def register(cls):
    """ديكوريتر: يسجل الوحش تلقائياً ويرتب القائمة حسب رقم المستوى."""
    REGISTRY.append(cls)
    REGISTRY.sort(key=lambda c: c.level)
    return cls


class MonsterProfile:
    """كل ما يخص وحشاً واحداً: قوته وسلوكه. هنا القيم الافتراضية."""

    level = 0               # رقم المستوى (1 = الأول) يحدد الترتيب

    # القوة
    health = 3
    speed = 4
    chase_speed = 5
    dodge_chance = 0.4
    dodge_range = 220       # المسافة التي يلاحظ عندها الرصاصة
    dodge_time = 400        # ms من المراوغة السريعة

    # الشكل
    image = None
    scale = 1.0

    # البطل في هذا المستوى
    ammo = 20
    infinite_ammo = False

    # الدخول العشوائي (يستعمل فقط إذا كان make_entrance حقيقياً)
    jump_min = 3000
    jump_max = 6000

    # النار (تستعمل فقط إذا كان make_gun حقيقياً)
    fire_size = 24
    fire_speed = 5
    fire_interval = 1500

    def make_entrance(self, screen_rect):
        return NoEntrance()

    def make_gun(self, screen):
        return NoGun()