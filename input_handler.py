import sys

import pygame


class InputHandler:
    """Reads keyboard and mouse events and calls the right object."""

    def __init__(self, stats, hero, flow, shooter, play_button):
        self.stats = stats
        self.hero = hero
        self.flow = flow
        self.shooter = shooter
        self.play_button = play_button

    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                self._keydown(event)
            elif event.type == pygame.KEYUP:
                self._keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down(event)

    def _keydown(self, event):
        hero = self.hero
        if event.key == pygame.K_RIGHT:
            hero.moving_right = True
        elif event.key == pygame.K_LEFT:
            hero.moving_left = True
        elif event.key == pygame.K_UP:
            hero.moving_up = True
        elif event.key == pygame.K_DOWN:
            hero.moving_down = True
        elif event.key == pygame.K_SPACE:
            self.shooter.fire()
        elif event.key == pygame.K_p and self.stats.state != "playing":
            self.flow.press_play()
        elif event.key in (pygame.K_F11, pygame.K_f):
            pygame.display.toggle_fullscreen()
        elif event.key == pygame.K_q:
            self._quit()

    def _keyup(self, event):
        hero = self.hero
        if event.key == pygame.K_RIGHT:
            hero.moving_right = False
        elif event.key == pygame.K_LEFT:
            hero.moving_left = False
        elif event.key == pygame.K_UP:
            hero.moving_up = False
        elif event.key == pygame.K_DOWN:
            hero.moving_down = False
        elif event.key == pygame.K_SPACE:
            hero.stop_fire()

    def _mouse_down(self, event):
        if (self.stats.state != "playing"
                and self.play_button.rect.collidepoint(event.pos)):
            self.flow.press_play()

    def _quit(self):
        self.flow.save_high_score()
        sys.exit()