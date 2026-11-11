import pygame
from pygame.sprite import Sprite

from monster_brain import MonsterBrain
from monster_entrance import MonsterEntrance
from monster_gun import MonsterGun


class Monster(Sprite):
    """The monster: image, position and health.

    How it moves, how it enters and when it shoots are handled by
    MonsterBrain, MonsterEntrance and MonsterGun.
    """

    HOME_Y = 70

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        self.brain = MonsterBrain(settings, self.screen_rect)
        self.entrance = MonsterEntrance(settings, self.screen_rect)
        self.gun = MonsterGun(settings, screen)
        self.fires = self.gun.fires

        self.reset()

    def reset(self):
        """Load the level's image and place the monster."""
        self.image = self._load_image()
        self.rect = self.image.get_rect()
        self.home_y = self.HOME_Y
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.home_y
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.max_health = self.settings.monster_health
        self.health = self.max_health

        self.brain.reset()
        self.entrance.reset()
        self.gun.reset(pygame.time.get_ticks())

        # Levels with several entrances: first appearance from a random side.
        if self.settings.monster_multi_side:
            self._enter_from_side()

    def _load_image(self):
        image = pygame.image.load(self.settings.monster_image).convert_alpha()
        scale = self.settings.monster_scale
        if scale != 1:
            w, h = image.get_size()
            image = pygame.transform.smoothscale(image, (int(w * scale), int(h * scale)))
        return image

    # ------------------------------------------------------------------
    def take_damage(self, amount=1):
        """Lose health points (never below zero)."""
        self.health = max(0, self.health - amount)
        # After every hit the monster comes back from another side.
        if self.settings.monster_multi_side and self.health > 0:
            self._enter_from_side()

    @property
    def is_dead(self):
        return self.health <= 0

    def _enter_from_side(self):
        self.entrance.start(self)
        self.brain.clear_dodge()

        self.max_health = self.settings.monster_health
        self.health = self.max_health

    def take_damage(self, amount=1):
        """Lose health points (never below zero)."""
        self.health = max(0, self.health - amount)

    @property
    def is_dead(self):
        return self.health <= 0

    # ------------------------------------------------------------------
    def update(self, bullets, hero):
        now = pygame.time.get_ticks()

        # Level 2: disappear and reappear from time to time.
        if (self.settings.monster_multi_side and not self.entrance.active
                and self.entrance.is_time_to_jump(now)):
            self._enter_from_side()

        if self.entrance.active:
            self.entrance.move(self)
        else:
            self.brain.update(self, bullets, hero, now)

        if self.settings.monster_shoots and not self.entrance.active:
            self.gun.try_fire(self, hero, now)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.fires.update()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
