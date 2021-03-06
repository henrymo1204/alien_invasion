import pygame as pg
from pygame.sprite import Sprite
from timer import Timer

class Ship(Sprite):
    images_boom = [pg.image.load('images/ship_explosion' + str(i) + '.png') for i in range(10)]

    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, settings, screen, sound, bullets=None):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.sound = sound

        # Load the ship image and get its rect.
        self.image = pg.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.center = 0
        self.center_ship()

        self.moving_right = False
        self.moving_left = False
        self.bullets = bullets
        self.shooting_bullets = False

        self.hit = False
        self.explode = False
        self.gone = False
        self.timer = Ship.timer_boom

        self.last_bullet_shot = None


    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

    def update(self):
        if self.hit and not self.explode:
            self.explode = True
        elif self.hit and self.explode:
            if self.timer_boom.frame_index() == len(Ship.images_boom) - 1:
                self.gone = True
                self.explode = False
                self.hit = False
                self.timer_boom.reset()
        else:
            delta = self.settings.ship_speed_factor
            if self.moving_right and self.rect.right < self.screen_rect.right: self.center += delta
            if self.moving_left and self.rect.left > 0: self.center -= delta
            if self.shooting_bullets:
                self.sound.shoot_bullet()
                self.bullets.add(settings=self.settings, screen=self.screen, ship=self)
                self.shooting_bullets = False
                # self.bullets_attempted += 1
                # if self.bullets_attempted % self.settings.bullets_every == 0:
                #     self.sound.shoot_bullet()
                #     self.bullets.add(settings=self.settings, screen=self.screen, ship=self)
            self.rect.centerx = self.center

    def draw(self):
        if self.explode:
            image = self.timer.imagerect()
            rect = image.get_rect()
            rect.centerx, rect.centery = self.rect.centerx, self.rect.centery
            self.screen.blit(image, rect)
        else:
            self.screen.blit(self.image, self.rect)
