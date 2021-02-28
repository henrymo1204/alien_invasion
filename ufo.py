import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from random import randint


class Ufos:
    def __init__(self, settings, screen, ufo_group, ship_height, game, stats, sb, bullets=None):
        self.settings = settings
        self.ufos = ufo_group
        self.screen = screen
        self.game = game
        self.ship_height = ship_height
        self.bullets = bullets
        self.stats = stats
        self.sb = sb

        self.last_bullet_shot = None

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        ufo = Ufo(settings=settings, screen=self.screen)
        ufo_width = ufo.rect.width
        ufo_height = ufo.rect.height
        ufos_per_row = 1
        rows_per_screen = 1

        #now = pg.time.get_ticks()%30000
        #(now%15000)
        for y in range(rows_per_screen):
            for x in range(ufos_per_row):
                # if y == 5:
                ufo = Ufo(settings=settings, screen=screen, number=y // 2, x=ufo_width * (4 + 1.5 * x), y=ufo_height * (1 + y), bullets=self.bullets, shooting=True)
                # else:
                #     alien = Alien(settings=settings, screen=screen, number=y // 2, x=alien_width * (4 + 1.5 * x),
                #                   y=alien_height * (1 + y), bullets=self.bullets)
                # alien = Alien(settings=settings, screen=screen, x=alien_width * (1 + 2 * x), y=alien_height * (1 + 2 * y))
                self.ufos.add(ufo)


    #def ufos_per_row(self, settings, alien_width): return 1
    #    space_x = settings.screen_width - 2 * alien_width
    #    return int(space_x / (2 * alien_width))

    #def rows_per_screen(self, settings, alien_height): return 1
        # space_y = settings.screen_height - (alien_height) - self.ship_height
        # # space_y = settings.screen_height - (3 * alien_height) - self.ship_height
        # return int(space_y / (alien_height))
        # # return int(space_y / (2 * alien_height))

    def add(self, ufo): self.ufos.add(ufo)

    def remove(self, ufo): self.ufos.ufos.remove(ufo)

    def change_direction(self):
    #    for alien in self.aliens:
    #        alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_edges(self):
        for ufo in self.ufos:
            if ufo.check_edges(): return True
        return False

    #def check_aliens_bottom(self):
    #    r = self.screen.get_rect()
    #    for alien in self.aliens.sprites():
    #        if alien.rect.bottom > r.bottom:
    #           return True
    #   return False

    def update(self):
        self.ufos.update()
        print(pg.time.get_ticks())
        num = randint(30000, 35000)
        now = pg.time.get_ticks()
        if self.last_bullet_shot is None:
            num = randint(0, 1000)
            if num == 1:
                self.create_fleet()
                self.last_bullet_shot = pg.time.get_ticks()
        elif now > self.last_bullet_shot + num:
            self.create_fleet()
            self.last_bullet_shot = pg.time.get_ticks()




        if self.check_edges():
            for ufo in self.ufos.copy():
                ufo.update()
                self.ufos.remove(ufo)


        # for y in range(rows_per_screen):
        #     for x in range(aliens_per_row):
        # row = 5
        for ufo in self.ufos.copy():
            ufo.update()
            if ufo.rect.bottom <= 0 or ufo.reallydead:
                self.ufos.remove(ufo)

    def draw(self):
        for ufo in self.ufos.sprites(): ufo.draw()


class Ufo(Sprite):   # INHERITS from SPRITE
    images = [[pg.image.load('images/ufo' + str(i) + '.png') for i in range(2)]]
    images_boom = [pg.image.load('images/alien_explosion' + str(i) + '.png') for i in range(9)]

    timers = []
    for i in range(1):
        timers.append(Timer(frames=images[i], wait=700))

    def __init__(self, settings, screen, number=0, x=1, y=0, speed=0, bullets=None, shooting=False):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.number = number
        self.update_requests = 0
        self.dead = False
        self.reallydead = False
        self.timer_switched = False
        self.shooting_bullets = shooting
        self.bullets = bullets

        # self.image = pg.image.load('images/alien.bmp')
        # self.rect = self.image.get_rect()
        # self.images = ['images/invader' + str(number) + str(i) + '.png' for i in range(2)]
        # print(self.images)
        # self.frames = [pg.image.load(self.images[i]) for i in range(len(self.images))]
        self.timer = Ufo.timers[number]
        # self.timer = Timer(frames=self.frames, wait=700)
        self.rect = self.timer.imagerect().get_rect()

        self.rect.x = self.x = 10
        self.rect.y = self.y = settings.screen_height * 0.1
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.speed = speed

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right >= rscreen.right or r.left <= 0

    def update(self):

        #num = randint(0, 5000)
        #if self.shooting_bullets:
        #    if num == 1:
        #        self.bullets.add(settings=self.settings, screen=self.screen, ship=self)
        if self.dead and not self.timer_switched:
            self.timer = Timer(frames=Ufo.images_boom, wait=100, looponce=True)
            self.timer_switched = True
        elif self.dead and self.timer_switched:
            # print("switched to boom timer", self.timer_boom.frame_index(), len(Alien.images_boom))
            if self.timer.frame_index() == len(Ufo.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.timer.reset()
        if not self.timer_switched:
            delta = self.settings.ufo_speed * self.settings.ufo_fleet_direction
            self.rect.x += delta
            self.x = self.rect.x

    def draw(self):
        # image = Ufo.images[self.number]
        # self.screen.blit(image, self.rect)
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

    @staticmethod
    def run_tests():
        print(Ufo.images)
