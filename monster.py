import pygame
from pygame.sprite import Sprite, Group

from monster_brain import MonsterBrain


class Monster(Sprite):

    HOME_Y = 70

    def __init__(self, settings, screen):
        super().__init__()

        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        self.reset()

    def reset(self):

        self.profile = self.settings.monster_profile

        self.brain = MonsterBrain(
            self.profile,
            self.screen_rect
        )

        self.entrance = self.profile.make_entrance(
            self.screen_rect
        )

        # Create the monster's ability.
        self.ability = self.profile.make_ability(
            self.screen
        )

        if self.ability is not None:
            self.fires = self.ability.fires
        else:
            self.fires = Group()

        # Create the damage strategy.
        self.damage_strategy = (
            self.profile.make_damage_strategy()
        )

        self.image = self._load_image()
        self.rect = self.image.get_rect()

        self.home_y = self.HOME_Y

        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.home_y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.max_health = self.profile.health
        self.health = self.max_health

        if self.ability is not None:
            self.ability.reset(pygame.time.get_ticks())

        self._enter_from_side()

    def _load_image(self):

        image = pygame.image.load(
            self.profile.image
        ).convert_alpha()

        scale = self.profile.scale

        if scale != 1:
            width, height = image.get_size()

            image = pygame.transform.smoothscale(
                image,
                (
                    int(width * scale),
                    int(height * scale)
                )
            )

        return image

    def take_damage(self, attack=1):

        # Calculate damage using the selected strategy.
        damage = self.damage_strategy.calculate_damage(
            attack
        )

        self.health = max(
            0,
            self.health - damage
        )

        if self.health > 0:
            self._enter_from_side()

    @property
    def is_dead(self):
        return self.health <= 0

    def _enter_from_side(self):

        self.entrance.start(self)
        self.brain.clear_dodge()

    def update(self, bullets, hero):

        now = pygame.time.get_ticks()

        if (
            not self.entrance.active
            and self.entrance.is_time_to_jump(now)
        ):
            self._enter_from_side()

        if self.entrance.active:

            self.entrance.move(self)

        else:

            self.brain.update(
                self,
                bullets,
                hero,
                now
            )

            if self.ability is not None:
                self.ability.update(
                    self,
                    hero,
                    now
                )

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.fires.update()

    def blitme(self):

        self.screen.blit(
            self.image,
            self.rect
        )
