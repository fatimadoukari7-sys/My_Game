import pygame


class GameFlow:
    """Controls the game state: start, next level, win, lose, score, high score."""

    def __init__(self, settings, stats, storage, hud, hero, monster, bullets,
                 waves=None):

        self.settings = settings
        self.stats = stats
        self.storage = storage
        self.hud = hud
        self.hero = hero
        self.monster = monster
        self.bullets = bullets
        self.waves = waves

    def load_level(self):
        """Apply the settings of stats.level and start playing it."""

        self.settings.apply_level(self.stats.level)

        pygame.mouse.set_visible(False)

        self.stats.state = "playing"

        self.hero.reset()
        self.monster.reset()

        if self.waves:
            self.waves.reset()

        self.bullets.empty()

        self.hud.prep_images()

    def start_game(self):
        """Start a brand new game from level 1."""

        self.stats.reset_stats()

        self.load_level()

    def press_play(self):
        """Play button / P key: next level if one was just finished."""

        if self.stats.state == "level_complete":

            self.stats.level += 1
            self.load_level()

        else:

            self.start_game()

    def add_points(self, points):

     print("ADD POINTS FUNCTION CALLED")
     print("POINTS RECEIVED:", points)
     print("SCORE BEFORE:", self.stats.score)

     self.stats.score += points

     print("SCORE AFTER:", self.stats.score)

     self.hud.prep_score()

     if self.stats.score > self.stats.high_score:
        self.stats.high_score = self.stats.score
        self.hud.prep_high_score()
    def win_game(self):
        """Finish the level and reward the player."""

        stats, settings = self.stats, self.settings

        last_level = stats.level >= len(settings.levels) - 1

        stats.state = "won" if last_level else "level_complete"

        # No ammo bonus on levels with unlimited ammo.
        ammo_bonus = (
            0 if settings.infinite_ammo
            else self.hero.ammo * settings.ammo_bonus
        )

        stats.last_reward = settings.win_reward + ammo_bonus

        stats.score += stats.last_reward

        self.hud.prep_score()

        self._update_high_score()

        pygame.mouse.set_visible(True)

    def lose_game(self):

        self.stats.state = "lost"

        pygame.mouse.set_visible(True)

    def _update_high_score(self):

        if self.stats.score > self.stats.high_score:

            self.stats.high_score = self.stats.score

            self.hud.prep_high_score()

        self.save_high_score()

    def save_high_score(self):

        self.storage.save(self.stats.high_score)