import pygame
from pygame.sprite import Group

from settings import Settings
from high_score_storage import HighScoreStorage
from stats import GameStats
from hero_images import HeroImages
from hero import Hero
from monster import Monster
from button import Button
from hud import HUD
from game_flow import GameFlow
from shooter import Shooter
from input_handler import InputHandler
from combat import CombatSystem
from renderer import Renderer, ScrollingBackground


def create_screen(settings, background_size):
    """The game is drawn at the background size and pygame scales it."""
    try:
        screen = pygame.display.set_mode(
            background_size, pygame.SCALED | pygame.RESIZABLE)
    except pygame.error:
        screen = pygame.display.set_mode(background_size)
    settings.screen_width, settings.screen_height = background_size
    pygame.display.set_caption("Hero vs Monster")
    return screen


def load_shoot_sound():
    try:
        return pygame.mixer.Sound("music/Crash_Metal_Sweetener_Distant.mp3")
    except (pygame.error, FileNotFoundError):
        return None


def run_game():
    pygame.init()
    settings = Settings()

    background_image = pygame.image.load('417403_980.jpg')
    screen = create_screen(settings, background_image.get_size())
    shoot_sound = load_shoot_sound()

    # Objects.
    storage = HighScoreStorage()
    stats = GameStats(settings, storage)
    hero = Hero(settings, screen, HeroImages())
    monster = Monster(settings, screen)
    bullets = Group()
    play_button = Button(settings, screen, "Play")
    hud = HUD(settings, screen, stats, hero, monster)

    # Systems.
    flow = GameFlow(settings, stats, storage, hud, hero, monster, bullets)
    shooter = Shooter(settings, screen, stats, hero, bullets, shoot_sound)
    inputs = InputHandler(stats, hero, flow, shooter, play_button)
    combat = CombatSystem(stats, flow, hero, monster, bullets)
    renderer = Renderer(screen, stats, ScrollingBackground(screen, background_image),
                        hud, hero, monster, bullets, play_button)

    clock = pygame.time.Clock()
    while True:
        inputs.process()
        if stats.state == "playing":
            hero.update()
            combat.update_bullets()
            if stats.state == "playing":
                combat.update_monster()

        renderer.draw()
        clock.tick(60)


if __name__ == "__main__":
    run_game()