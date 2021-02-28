from pygame.sprite import Sprite
import pygame as pg
from timer import Timer


class Barriers:
    def __init__(self, settings, screen, ally_group, ship_height, game):
        self.settings = settings
        self.allies = ally_group
        self.screen = screen
        self.game = game
        self.ship_height = ship_height
        self.create_barriers()

    def create_barriers(self):
        settings, screen = self.settings, self.screen
        barriers = Barrier(settings=settings, screen=self.screen)
        alien_width = barriers.rect.width
        alien_height = barriers.rect.height

        for i in range(3):
            barrier = Barrier(settings=settings, screen=screen, x=alien_width * (1.205 + 3 * i), y=alien_height * 7)
            self.allies.add(barrier)

    def reset(self):
        self.create_barriers()
        for barrier in self.allies:
            barrier.health = 10

    def update(self):
        for barrier in self.allies:
            barrier.update()
            if barrier.gone:
                self.allies.remove(barrier)

    def draw(self):
        for ally in self.allies.sprites(): ally.draw()


class Barrier(Sprite):
    images_boom = [pg.image.load('images/barrier_explosion' + str(i) + '.png') for i in range(10)]

    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, settings, screen, x=0, y=0):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Load the ship image and get its rect.
        self.image = pg.image.load('images/barrier.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.x = self.x = x
        self.rect.y = self.y = y

        self.health = 10
        self.explode = False
        self.timer = Barrier.timer_boom
        self.gone = False

    def update(self):
        if self.health <= 0 and not self.explode:
            self.explode = True
        elif self.health <= 0 and self.explode:
            if self.timer_boom.frame_index() == len(Barrier.images_boom) - 1:
                self.gone = True
                self.timer_boom.reset()

    def draw(self):
        # image = Alien.images[self.number]
        # self.screen.blit(image, self.rect)
        if self.explode:
            image = self.timer.imagerect()
        else:
            image = self.image
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

    # def update(self):
    #     delta = self.settings.ship_speed_factor
    #     if self.moving_right and self.rect.right < self.screen_rect.right: self.center += delta
    #     if self.moving_left  and self.rect.left > 0: self.center -= delta
    #     if self.shooting_bullets:
    #         self.sound.shoot_bullet()
    #         self.bullets.add(settings=self.settings, screen=self.screen, ship=self)
    #         self.shooting_bullets = False
    #         # self.bullets_attempted += 1
    #         # if self.bullets_attempted % self.settings.bullets_every == 0:
    #         #     self.sound.shoot_bullet()
    #         #     self.bullets.add(settings=self.settings, screen=self.screen, ship=self)
    #     self.rect.centerx = self.center

    # def draw(self): self.screen.blit(self.image, self.rect)
