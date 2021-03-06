import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from random import randint, choice


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
        self.last_UFO_appeared = None


    def create_fleet(self):
        settings, screen = self.settings, self.screen
        ufos = Ufo(settings=settings, screen=self.screen)
        ufo_width = ufos.rect.width
        ufo_height = ufos.rect.height
        ufos_per_row = 1
        rows_per_screen = 1

        # now = pg.time.get_ticks()%30000
        # (now%15000)
        x = y = 0
        Ufo.images_boom.clear()
        ufo = Ufo(settings=settings, screen=screen, number=y // 2, bullets=self.bullets, shooting=True)
        ufo.append_score()
        self.ufos.add(ufo)


    def add(self, ufo):
        self.ufos.add(ufo)

    def remove(self, ufo):
        self.ufos.ufos.remove(ufo)

    def change_direction(self):
        self.settings.fleet_direction *= -1

    def check_edges(self):
        for ufo in self.ufos:
            if ufo.check_edges():
                Ufo.images_boom.clear()
                return True
        return False

    def update(self):
        self.ufos.update()
        num = randint(15000, 25000)
        now = pg.time.get_ticks()
        if self.last_UFO_appeared is None:
            num = randint(0, 1000)
            if num == 1:
                self.create_fleet()
                self.last_UFO_appeared = pg.time.get_ticks()
        elif now > self.last_UFO_appeared + num:
            self.create_fleet()
            self.last_UFO_appeared = pg.time.get_ticks()

        if self.check_edges():
            for ufo in self.ufos.copy():
                ufo.update()
                self.ufos.remove(ufo)

        for ufo in self.ufos.copy():
            ufo.update()
            if ufo.reallydead:
                self.ufos.remove(ufo)

    def draw(self):
        for ufo in self.ufos.sprites(): ufo.draw()



class Ufo(Sprite):  # INHERITS from SPRITE
    images = [[pg.image.load('images/ufo' + str(i) + '.png') for i in range(2)]]
    images_boom = []

    timers = []
    for i in range(1):
        timers.append(Timer(frames=images[i], wait=700))

    def __init__(self, settings, screen, number=0, speed=0, bullets=None, shooting=False):
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

        self.ufo_direction = self.settings.ufo_fleet_direction * (choice([-1, 1]))


        self.rect.x = self.x = 0 if self.ufo_direction > 0 else settings.screen_width - 80
        self.rect.y = self.y = 80 # TESTING normal value 10
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        self.x = float(self.rect.x)


        self.score = None
        self.possible_ufo_points = [500, 1000, 1500, 2000]

    def get_score(self): #get_score
        """get random score from possible ufo"""
        self.score = choice(self.possible_ufo_points)
        return self.score

    def append_score(self):
        score = self.get_score()
        if score == 500:
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point500_1.png'))
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point500_1.png'))
        elif score == 1000:
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point1000_1.png'))
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point1000_1.png'))
        elif score == 1500:
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point1500_1.png'))
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point1500_1.png'))
        elif score == 2000:
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point2000_1.png'))
            Ufo.images_boom.append(pg.image.load('images/ufo_points/ufo_point2000_1.png'))
        #print('appended ', score)

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right > rscreen.right or r.left < 0

    def update(self):
        if self.dead and not self.timer_switched:
            self.timer = Timer(frames=Ufo.images_boom, wait=500, looponce=True)
            self.timer_switched = True
        elif self.dead and self.timer_switched:
            #print("switched to boom timer", self.timer_boom.frame_index(), len(Ufo.images_boom))
            if self.timer.frame_index() == len(Ufo.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.timer.reset()
                Ufo.images_boom.clear()
        if not self.timer_switched:
            delta = self.settings.ufo_speed * self.ufo_direction
            self.rect.x += delta
            self.x = self.rect.x
            #print(delta)

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
