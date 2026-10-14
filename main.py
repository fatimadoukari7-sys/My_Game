import pygame
from pygame.sprite import Group

from settings import Settings
from hero import Hero
from monster import Monster
from button import Button
from stats import GameStats
from hud import HUD
import game_logic as gl


def run_game():
    pygame.init()
    settings = Settings()

    background = pygame.image.load('417403_980.jpg')
    background_size = background.get_size()
    screen = pygame.display.set_mode(background_size)
    settings.screen_width, settings.screen_height = background_size
    pygame.display.set_caption("Hero vs Monster")

    # The only sound in the game: the gunshot.
    try:
        shoot_sound = pygame.mixer.Sound("music/Crash_Metal_Sweetener_Distant.mp3")
    except (pygame.error, FileNotFoundError):
        shoot_sound = None

    play_button = Button(settings, screen, "Play")
    stats = GameStats(settings)
    hero = Hero(settings, screen)
    monster = Monster(settings, screen)
    hud = HUD(settings, screen, stats, hero)
    bullets = Group()

    clock = pygame.time.Clock()
    y = 0   # scrolling background position

    while True:
        gl.check_events(settings, screen, stats, hud, play_button, hero,
                        monster, bullets, shoot_sound)

        if stats.state == "playing":
            hero.update()
            gl.update_bullets(settings, stats, hud, hero, monster, bullets)
            if stats.state == "playing":
                gl.update_monster(settings, stats, hero, monster, bullets)

        # Scrolling background (two copies stacked vertically).
        y += 5
        if y >= settings.screen_height:
            y -= settings.screen_height
        screen.blit(background, (0, y))
        screen.blit(background, (0, y - settings.screen_height))

        gl.update_screen(settings, screen, stats, hud, hero, monster, bullets,
                         play_button)
        clock.tick(60)


run_game()