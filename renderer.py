import pygame


class ScrollingBackground:
    """Draws the background picture moving down (two copies stacked)."""

    def __init__(self, screen, image, speed=5):
        self.screen = screen
        self.image = image
        self.speed = speed
        self.height = image.get_height()
        self.y = 0

    def draw(self):
        self.y += self.speed
        if self.y >= self.height:
            self.y -= self.height
        self.screen.blit(self.image, (0, self.y))
        self.screen.blit(self.image, (0, self.y - self.height))


class Renderer:
    """Draws everything on the screen, once per frame."""

    def __init__(self, screen, stats, background, hud, hero, monster,
                 bullets, play_button):
        self.screen = screen
        self.stats = stats
        self.background = background
        self.hud = hud
        self.hero = hero
        self.monster = monster
        self.bullets = bullets
        self.play_button = play_button

    def draw(self):
        self.background.draw()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for fire in self.monster.fires.sprites():
            fire.draw()

        self.hero.blitme()
        self.monster.blitme()
        self.hud.show()

        if self.stats.state != "playing":
            self.play_button.draw_button()

        pygame.display.flip()