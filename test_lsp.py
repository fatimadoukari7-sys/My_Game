import pygame

from settings import Settings
from monster_profile import MonsterProfile


def test_monster_profiles():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((800, 600))

    for monster_class in settings.levels:

        monster = monster_class()

        # Both monsters must respect the parent contract.
        assert isinstance(monster, MonsterProfile)

        assert monster.health > 0
        assert monster.speed > 0
        assert monster.image is not None

        # Both monsters must provide a valid gun.
        gun = monster.make_gun(screen)

        assert hasattr(gun, "fires")
        assert hasattr(gun, "reset")
        assert hasattr(gun, "try_fire")

        print(monster_class.__name__, "respects MonsterProfile")

    pygame.quit()


if __name__ == "__main__":
    test_monster_profiles()