import pygame as pg
from settings import Settings
import game_functions as gf
from pygame.sprite import Group

from bullet import Bullets
from ship import Ship
from alien import Aliens
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound import Sound
from alien_bullets import AlienBullets
from barrier import Barriers
from menu import MenuAliens, MenuUfos
from ufo import Ufos
import time
import wave

from vector import Vector
from quaternion import Quaternion
from matrix import Matrix


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        ship_image = pg.image.load('images/ship.bmp')
        self.ship_height = ship_image.get_rect().height
        self.hs = 0
        self.sound = Sound(bg_music="sounds/startrek_louder.wav")
        # self.sound = Sound(bg_music="sounds/startrektheme.wav")
        # self.sound = Sound(bg_music="sounds/beepbeepmusic.wav")
        self.sound.play()
        self.sound.pause_bg()
        self.play_button = self.aliens = self.ufos = self.stats = self.sb = self.bullets = self.ship = self.alienBullets = self.barrier = None
        self.restart()

    def restart(self):
        self.play_button = Button(settings=self.settings, screen=self.screen, msg="Play")

        menu_alien_group = Group()
        menu_ufo_group = Group()
        alien_group = Group()  # group of aliens
        ufo_group = Group()
        barrier_group = Group()  # group of barriers

        human_bullet_group = Group()
        alien_bullet_group = Group()

        ship_group = Group()

        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(settings=self.settings, screen=self.screen, stats=self.stats, sound=self.sound)

        self.alienBullets = AlienBullets(bullet_group=alien_bullet_group, enemy_group=barrier_group,
                                         enemy_bullet_group=human_bullet_group,
                                         settings=self.settings, ship_group=ship_group,
                                         stats=self.stats, sb=self.sb, game=self)
        self.aliens = Aliens(settings=self.settings, screen=self.screen, alien_group=alien_group,
                             ship_height=self.ship_height, game=self, stats=self.stats, sb=self.sb,
                             bullets=self.alienBullets)

        self.ufos = Ufos(settings=self.settings, screen=self.screen, ufo_group=ufo_group,
                         ship_height=self.ship_height, game=self, stats=self.stats, sb=self.sb,
                         bullets=self.alienBullets)

        self.menu_aliens = MenuAliens(settings=self.settings, screen=self.screen, menu_alien_group=menu_alien_group,
                                      ship_height=self.ship_height, game=self, stats=self.stats, sb=self.sb,
                                      bullets=self.alienBullets)

        self.menu_ufos = MenuUfos(settings=self.settings, screen=self.screen, menu_ufo_group=menu_ufo_group,
                                      ship_height=self.ship_height, game=self, stats=self.stats, sb=self.sb,
                                      bullets=self.alienBullets)

        self.barrier = Barriers(settings=self.settings, screen=self.screen, barrier_group=barrier_group,
                                ship_height=self.ship_height, game=self)

        self.bullets = Bullets(bullet_group=human_bullet_group, alien_bullet_group=alien_bullet_group,
                               enemy_group=alien_group, ufo_group=ufo_group, barrier_group=barrier_group,
                               settings=self.settings, aliens=self.aliens, ufos=self.ufos, stats=self.stats, sb=self.sb,
                               barriers=self.barrier)
        self.ship = Ship(screen=self.screen, settings=self.settings, bullets=self.bullets,
                         sound=self.sound)  # add ship group
        ship_group.add(self.ship)
        self.settings.init_dynamic_settings()
        #self.stats.high_score = self.hs
        #self.sb.prep_high_score()

    def play(self):
        while True:
            gf.check_events(settings=self.settings, screen=self.screen, stats=self.stats,
                            play_button=self.play_button, ship=self.ship, bullets=self.bullets)
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.aliens.update()
                self.ufos.update()
                self.alienBullets.update()
                self.barrier.update()
                time.sleep(0.01)

                self.screen.fill(self.settings.bg_color)
                self.ship.draw()
                self.bullets.draw()
                self.aliens.draw()
                self.ufos.draw()
                self.alienBullets.draw()
                self.barrier.draw()
                self.sb.show_score()
            if not self.stats.game_active:
                self.play_button.draw()
                self.sound.pause_bg()
                # self.menu_aliens.draw()
                quit_game = not gf.startup_screen(settings=self.settings, stats=self.stats, screen=self.screen,
                                                  menu_aliens=self.menu_aliens, menu_ufos=self.menu_ufos)
                if quit_game:
                    pg.quit()
                    break
            else:
                if not self.sound.playing_bg: self.sound.unpause_bg()
            pg.display.flip()

    def reset(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.aliens.empty()
            self.ufos.ufos.empty()
            self.aliens.create_fleet()
            self.bullets.bullets.empty()
            self.ship.center_ship()
            self.barrier.reset()
            time.sleep(1)
        else:
            self.stats.game_active = False
            self.sound.pause_bg()
            self.stats.save_high_score()
            self.restart()


def main():
    g = Game()
    g.play()
    # Vector.run_tests()
    # Quaternion.run_tests()
    # Matrix.run_tests()
    # Alien.run_tests()


if __name__ == '__main__':
    main()

    # def sum_(*args):
    #     total = 0
    #     for el in args:
    #         total += el
    #     return total
    #
    #
    # def print_dict(**kwargs):
    #     i = 0
    #     for k, v in kwargs.items():
    #         print(f'{k}:{v}', end='')
    #         if i < len(kwargs.items()): print(', ', end='')
    #         i += 1
    #     print('\n')
    #
    #
    # def print_list_and_dict(msg, *args, **kwargs):
    #     print(f"printing '{msg}' ...")
    #     print('printing list first... ', end='')
    #     if len(args) == 0: print('list is empty', end='')
    #     for el in args:
    #         print(el, end=' ')
    #     print('\nprinting dict second... ', end='')
    #     i = 0
    #     if len(kwargs.items()) == 0: print('dictionary is empty', end='')
    #     for k, v in kwargs.items():
    #         print(f'{k}:{v}', end='')
    #         if i < len(kwargs.items()): print(', ', end='')
    #         i += 1
    #     print('\n')
    #
    #
    # def make_person(lname, fname, age, zip):
    #     person = {'lname': lname, 'fname': fname, 'age': age, 'zip': zip}
    #     return person.copy()

    # print(sum_(1, 2))
    # print(sum_(1, 2, 3))
    # print(sum_(1, 2, 3, 4))
    # print(sum_(1, 2, 3, 4, 5))
    # print(sum_(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    # print(sum_(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
    #
    # print('\n')
    # print_dict(name='Star Trek', year=2430, ship='Enterprise', captain='James T. Kirk')
    #
    # print_list_and_dict("1, 2, 3, 4, 5", 1, 2, 3, 4, 5)
    # print_list_and_dict("1, 2, 3, 4, five=5", 1, 2, 3, 4, five=5)
    # print_list_and_dict("1, 2, 3, four=4, five=5", 1, 2, 3, four=4, five=5)
    # print_list_and_dict("1, 2, three=3, four=4, five=5", 1, 2, three=3, four=4, five=5)
    # print_list_and_dict("1, two=2, three=3, four=4, five=5", 1, two=2, three=3, four=4, five=5)
    # print_list_and_dict("one=1, two=2, three=3, four=4, five=5", one=1, two=2, three=3, four=4, five=5)
    #
    # # ORDER DOESN'T MATTER if you use DICTIONARIES, but it DOES MATTER if you use LISTS
    # print_list_and_dict("ORDER DOESN'T MATTER if you use DICTIONARIES1, 2, five=5, four=4, three=3",
    #                     1, 2, five=5, four=4, three=3)

    # CANNOT PUT list (aka positional) items after dictionary (aka keyword) items
    # print_list_and_dict("WILL NOT COMPILE -- ORDER DOESN'T MATTER if you use DICTIONARIES1, 2, five=5, four=4, three=3",
    #                     1, five=5, four=4, three=3, 2)

    # guy = {'lname': 'xxx', 'fname': 'xxx', 'age': 0, 'zip': 90000}
    # joe = guy.copy()
    # joe['lname'] = 'smith';  joe['fname'] = 'joe';  joe['age'] = 23;  joe['zip'] = 60000;
    # print(joe)
    # mike = make_person('Johnson', 'Mike', 25, 70000)
    # mike['salary'] = 150000
    # print(f'{mike["fname"]} is {mike}')
