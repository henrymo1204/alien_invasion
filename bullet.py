import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from random import randint


class Bullets:
    def __init__(self, bullet_group, alien_bullet_group, enemy_group, barrier_group, settings, aliens, stats, sb):
        self.bullets = bullet_group
        self.alien_bullets = alien_bullet_group
        self.alien_group = enemy_group
        self.barrier_group = barrier_group
        self.settings = settings
        self.aliens = aliens
        self.stats = stats
        self.sb = sb

    def add(self, settings, screen, ship):
        self.bullets.add(Bullet(settings=settings, screen=screen, ship=ship))

    def update(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            elif bullet.gone:
                self.bullets.remove(bullet)
                # self.alien_bullets.remove(alienBullet)
            for alienBullet in self.alien_bullets.copy():
                if bullet.rect.colliderect(alienBullet):
                    bullet.collide = True
                    alienBullet.gone = True

        collisions = pg.sprite.groupcollide(self.bullets, self.alien_group, True, False)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    alien.dead = True
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.check_high_score(self.stats.score)
                self.sb.prep_score()
        elif pg.sprite.groupcollide(self.bullets, self.barrier_group, True, False):
            print('hit')
        if len(self.alien_group) == 0:
            self.bullets.empty()
            self.alien_bullets.empty()
            self.settings.increase_speed()
            self.aliens.create_fleet()
            self.stats.level += 1
            self.sb.prep_level()

    def draw(self):
        for bullet in self.bullets.sprites():
            bullet.draw()


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    images_boom = [pg.image.load('images/bullet_explosion' + str(i) + '.png') for i in range(10)]

    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        # self.color = settings.bullet_color
        self.color = (0, 255, 0)
        self.speed_factor = settings.bullet_speed_factor
        self.collide = False
        self.explode = False
        self.gone = False
        self.timer = Bullet.timer_boom

    def update(self):
        if self.collide and not self.explode:
            self.explode = True
        elif self.collide and self.explode:
            if self.timer_boom.frame_index() == len(Bullet.images_boom) - 1:
                self.gone = True
                self.explode = False
                self.collide = False
                self.timer_boom.reset()
        else:
            self.y -= self.speed_factor
            self.rect.y = self.y


    def draw(self):
        if self.collide:
            image = self.timer.imagerect()
            rect = image.get_rect()
            rect.centerx, rect.centery = self.rect.centerx, self.rect.y
            self.screen.blit(image, rect)
        else:
            pg.draw.rect(self.screen, self.color, self.rect)
