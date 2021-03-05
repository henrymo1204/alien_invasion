import pygame as pg
from pygame.sprite import Sprite
from random import randint
import time
from PIL import Image


class AlienBullets:
    def __init__(self, bullet_group, enemy_group, enemy_bullet_group, ship_group, settings, stats, sb, game):
        self.bullets = bullet_group
        self.human_group = enemy_group
        self.human_bullet_group = enemy_bullet_group
        self.ship_group = ship_group
        self.settings = settings
        self.stats = stats
        self.sb = sb
        self.game = game

    def add(self, settings, screen, ship):
        self.bullets.add(Bullet(settings=settings, screen=screen, ship=ship))

    def update(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom >= self.settings.screen_height:
                self.bullets.remove(bullet)
            elif bullet.gone:
                self.bullets.remove(bullet)
        if pg.sprite.groupcollide(self.bullets, self.ship_group, True, False):
            if not self.game.ship.gone:
                self.game.ship.hit = True
        if self.game.ship.gone:
            self.game.ship.gone = False
            self.bullets.empty()
            self.human_bullet_group.empty()
            self.game.reset()
            return
        collisions = pg.sprite.groupcollide(self.bullets, self.human_group, True, False)
        if collisions:
            for barriers in collisions.values():
                for barrier in barriers:
                    barrier.update()
                    barrier.damaged()

    def draw(self):
        for bullet in self.bullets.sprites():
            bullet.draw()


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, settings.bullet_width + 5, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.bottom
        self.y = float(self.rect.y)
        # self.color = settings.bullet_color
        self.color = (255, 0, 0)
        self.speed_factor = settings.bullet_speed_factor
        self.gone = False

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)
