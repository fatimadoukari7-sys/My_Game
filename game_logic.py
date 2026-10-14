import sys

import pygame

from bullet import Bullet


# ----------------------------------------------------------------------
# Game flow
# ----------------------------------------------------------------------
def start_game(settings, stats, hud, hero, monster, bullets):
    """Start (or restart) a round."""
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.state = "playing"

    hero.reset()
    monster.reset()
    bullets.empty()

    hud.prep_images()


def win_game(settings, stats, hud, hero):
    stats.state = "won"
    stats.last_reward = settings.win_reward + hero.ammo * settings.ammo_bonus
    stats.score += stats.last_reward
    hud.prep_score()
    check_high_score(stats, hud)
    update_high_score(stats)
    pygame.mouse.set_visible(True)


def lose_game(stats):
    stats.state = "lost"
    pygame.mouse.set_visible(True)


def check_high_score(stats, hud):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        hud.prep_high_score()


def update_high_score(stats):
    with open("highest_score.txt", "w") as file:
        file.write(str(int(stats.high_score)))


# ----------------------------------------------------------------------
# Events
# ----------------------------------------------------------------------
def fire_bullet(settings, screen, stats, hero, bullets, shoot_sound):
    """Fire one bullet if the hero still has ammo."""
    if stats.state != "playing":
        return
    if hero.ammo > 0 and len(bullets) < settings.bullets_allowed:
        bullets.add(Bullet(settings, screen, hero))
        hero.ammo -= 1
        if shoot_sound:
            shoot_sound.play()


def check_keydown_events(event, settings, screen, stats, hud, hero, monster,
                         bullets, shoot_sound):
    if event.key == pygame.K_RIGHT:
        hero.moving_right = True
    elif event.key == pygame.K_LEFT:
        hero.moving_left = True
    elif event.key == pygame.K_UP:
        hero.moving_up = True
    elif event.key == pygame.K_DOWN:
        hero.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, stats, hero, bullets, shoot_sound)
    elif event.key == pygame.K_p and stats.state != "playing":
        start_game(settings, stats, hud, hero, monster, bullets)
    elif event.key == pygame.K_q:
        update_high_score(stats)
        sys.exit()


def check_keyup_events(event, hero):
    if event.key == pygame.K_RIGHT:
        hero.moving_right = False
    elif event.key == pygame.K_LEFT:
        hero.moving_left = False
    elif event.key == pygame.K_UP:
        hero.moving_up = False
    elif event.key == pygame.K_DOWN:
        hero.moving_down = False


def check_events(settings, screen, stats, hud, play_button, hero, monster,
                 bullets, shoot_sound):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_high_score(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, stats, hud, hero,
                                 monster, bullets, shoot_sound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, hero)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if stats.state != "playing" and play_button.rect.collidepoint(event.pos):
                start_game(settings, stats, hud, hero, monster, bullets)


# ----------------------------------------------------------------------
# Updates
# ----------------------------------------------------------------------
def update_bullets(settings, stats, hud, hero, monster, bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # A bullet hit the monster: the hero wins.
    if pygame.sprite.spritecollideany(monster, bullets):
        bullets.empty()
        win_game(settings, stats, hud, hero)


def update_monster(settings, stats, hero, monster, bullets):
    monster.update(bullets, hero)

    # The monster touched the hero.
    if pygame.sprite.collide_rect(hero, monster):
        if hero.take_damage() and hero.health <= 0:
            lose_game(stats)


def update_screen(settings, screen, stats, hud, hero, monster, bullets, play_button):
    """Draw everything (the background is drawn in main.py)."""
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    hero.blitme()
    monster.blitme()
    hud.show()

    if stats.state != "playing":
        play_button.draw_button()

    pygame.display.flip()