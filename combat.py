import pygame


class CombatSystem:
    """Moves bullets and checks every collision between the game objects."""

    def __init__(self, stats, flow, hero, monster, bullets):
        self.stats = stats
        self.flow = flow
        self.hero = hero
        self.monster = monster
        self.bullets = bullets

    def update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Bullets that hit the monster disappear and take away its health.
        hits = pygame.sprite.spritecollide(self.monster, self.bullets, True)
        if hits:
            self.monster.take_damage(len(hits))
            if self.monster.is_dead:        # no health left: the hero wins
                self.bullets.empty()
                self.monster.fires.empty()
                self.flow.win_game()

    def update_monster(self):
        self.monster.update(self.bullets, self.hero)

        # The monster touched the hero.
        if pygame.sprite.collide_rect(self.hero, self.monster):
            if self._hero_died_after_hit():
                return

        # A fireball hit the hero.
        for fire in self.monster.fires.copy():
            if pygame.sprite.collide_rect(self.hero, fire):
                fire.kill()
                if self._hero_died_after_hit():
                    return

    def _hero_died_after_hit(self):
        if self.hero.take_damage() and self.hero.health <= 0:
            self.flow.lose_game()
            return True
        return False