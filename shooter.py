from bullet import Bullet


class Shooter:
    """Creates the hero's bullets and uses up ammo."""

    def __init__(self, settings, screen, stats, hero, bullets, shoot_sound):
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.hero = hero
        self.bullets = bullets
        self.shoot_sound = shoot_sound

    def fire(self):
        """Fire one bullet if the hero still has ammo (always, if unlimited)."""
        if self.stats.state != "playing":
            return
        self.hero.start_fire()                       # show the "fire" picture
        if self.hero.ammo > 0 and len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self.settings, self.screen, self.hero))
            if not self.settings.infinite_ammo:
                self.hero.ammo -= 1
            if self.shoot_sound:
                self.shoot_sound.play()