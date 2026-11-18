import pygame

import theme


class HeroImages:
    """Loads the hero pictures and chooses which one to show.

    Which files to load and how big they are: see theme.py.
    """

    def __init__(self):
        self.height = theme.HERO_HEIGHT
        self.pictures = self._load_all()

    def _load(self, path):
        """Load one picture scaled to the hero height, or None if it cannot be loaded."""
        try:
            raw = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError) as error:
            print("HeroImages: could not load '%s' (%s)" % (path, error))
            return None
        w, h = raw.get_size()
        return pygame.transform.smoothscale(
            raw, (max(1, int(w * self.height / h)), self.height))

    def _load_all(self):
        pictures = {name: self._load(path)
                    for name, path in theme.HERO_IMAGES.items()}

        if pictures['stop'] is None:    # safety net: the game still runs
            fallback = pygame.Surface((60, self.height), pygame.SRCALPHA)
            pygame.draw.ellipse(fallback, theme.HERO_FALLBACK_COLOR,
                                fallback.get_rect())
            pictures['stop'] = fallback

        for name in pictures:           # a missing picture -> the stop picture
            if pictures[name] is None:
                pictures[name] = pictures['stop']
        return pictures

    def choose(self, hero, now):
        """Choose the picture: fire > right > left > up > stop."""
        if hero.firing or now < hero.fire_until:
            name = 'fire'
        elif hero.moving_right and not hero.moving_left:
            name = 'right'
        elif hero.moving_left and not hero.moving_right:
            name = 'left'
        elif hero.moving_up and not hero.moving_down:
            name = 'up'
        else:
            name = 'stop'
        return self.pictures[name]

    @property
    def default(self):
        return self.pictures['stop']