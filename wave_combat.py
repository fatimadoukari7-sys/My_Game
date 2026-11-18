import pygame


class WaveCombat:
    """Level 3 collisions: bullets kill flying monsters, monsters hurt the hero.

    It is the level 3 version of CombatSystem.
    """

    def __init__(self, stats, flow, hero, bullets, waves):
        self.stats = stats
        self.flow = flow
        self.hero = hero
        self.bullets = bullets
        self.waves = waves

    def update(self):
        self._update_bullets()
        if self.stats.state != "playing":
            return
        self.waves.update()
        self._update_hero_hits()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for enemy in self.waves.enemies.copy():
            if pygame.sprite.spritecollide(enemy, self.bullets, True):
                enemy.kill()
                self.waves.add_kill()
                self.flow.add_points(self.waves.points_per_kill)   # score goes up
                if self.waves.complete:         # the goal is reached: the hero wins
                    self.bullets.empty()
                    self.waves.enemies.empty()
                    self.flow.win_game()
                    return

    def _update_hero_hits(self):
        crashed = pygame.sprite.spritecollide(
            self.hero, self.waves.enemies, True, pygame.sprite.collide_rect)
        for _ in crashed:
            if self.hero.take_damage() and self.hero.health <= 0:
                self.flow.lose_game()
                return