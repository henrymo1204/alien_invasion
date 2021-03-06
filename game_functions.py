import sys
import pygame as pg
from menu import Button, Intro
from high_score import HighScoreScreen


def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pg.K_RIGHT:
        ship.moving_right = True
    elif event.key == pg.K_LEFT:
        ship.moving_left = True
    elif event.key == pg.K_SPACE:
        if not ship.last_bullet_shot:
            ship.last_bullet_shot = pg.time.get_ticks()
            ship.shooting_bullets = True
        elif pg.time.get_ticks() >= ship.last_bullet_shot + settings.bullets_every:
            ship.last_bullet_shot = pg.time.get_ticks()
            ship.shooting_bullets = True
    elif event.key == pg.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pg.K_RIGHT:
        ship.moving_right = False
    elif event.key == pg.K_LEFT:
        ship.moving_left = False
    elif event.key == pg.K_SPACE:
        ship.shooting_bullets = False


def check_play_button(stats, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True


def check_events(settings, screen, stats, play_button, ship, bullets):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(stats=stats, play_button=play_button, mouse_x=mouse_x, mouse_y=mouse_y)
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, settings=settings, screen=screen,
                                 ship=ship, bullets=bullets)
        elif event.type == pg.KEYUP:
            check_keyup_events(event=event, ship=ship)


def startup_screen(settings, stats, screen, menu_aliens, menu_ufos):
    """Display the startup menu on the screen, return False if the user wishes to quit,
    True if they are ready to play"""
    menu = Intro(settings, stats, screen)
    play_button = Button(settings, screen, 'Play Game', y_factor=0.75)
    hs_button = Button(settings, screen, 'High Scores', y_factor=0.85)
    intro = True

    while intro:
        play_button.alter_text_color(*pg.mouse.get_pos())
        hs_button.alter_text_color(*pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                click_x, click_y = pg.mouse.get_pos()
                stats.game_active = play_button.check_button(click_x, click_y)
                intro = not stats.game_active
                if hs_button.check_button(click_x, click_y):
                    ret_hs = high_score_screen(settings, stats, screen)
                    if not ret_hs:
                        return False
        screen.fill(settings.bg_color)
        menu.draw()
        hs_button.draw_button()
        play_button.draw_button()
        menu_aliens.draw()
        menu_ufos.draw()
        pg.display.flip()

    return True


def high_score_screen(settings, stats, screen):
    """Display all high scores in a separate screen with a back button"""
    hs_screen = HighScoreScreen(settings, screen, stats)
    back_button = Button(settings, screen, 'Back To Menu', y_factor=0.85)

    while True:
        back_button.alter_text_color(*pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if back_button.check_button(*pg.mouse.get_pos()):
                    return True
        screen.fill(settings.bg_color)
        hs_screen.show_scores()
        back_button.draw_button()
        pg.display.flip()
