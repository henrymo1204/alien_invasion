from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame as pg
from timer import Timer
from copy import copy
from random import randint
from PIL import Image


class Barriers:
    def __init__(self, settings, screen, barrier_group, ship_height, game):
        self.settings = settings
        self.barriers = barrier_group
        self.screen = screen
        self.game = game
        self.ship_height = ship_height
        self.create_barriers()

    def create_barriers(self):
        settings, screen = self.settings, self.screen

        for i in range(4):
            barrier = Barrier(settings=settings, screen=screen, x=250 * (1+i) - 80, y=700)
            self.barriers.add(barrier.group())

    def reset(self):
        self.create_barriers()

    def update(self):
        for barrier in self.barriers:
            if barrier.health <= 0:
                self.barriers.remove(barrier)

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()


class Barrier(Sprite):
    block = pg.image.load('images/block.png')
    block_rect = block.get_rect()
    barrier_width = 7
    barrier_height = 5

    def __init__(self, settings, screen, x=0, y=0):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Load the ship image and get its rect.
        self.image = pg.image.load('images/block.png')
        self.rect = copy(Barrier.block.get_rect())
        self.screen_rect = screen.get_rect()

        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.barrier_group = Group()
        self.create_barrier()

    def create_barrier(self):
        w, h = Barrier.block_rect.width, Barrier.block_rect.height
        rect = copy(self.rect)
        for x in range(Barrier.barrier_width):
            for y in range(Barrier.barrier_height):
                r = copy(rect)
                image = self.image
                r.y += h * y
                r.x += w * x
                self.barrier_group.add(Block(screen=self.screen, image=image, rect=r))

    def group(self):
        return self.barrier_group

    def draw(self):
        for block in self.barrier_group:
            block.draw()


class Block(Sprite):
    images_boom = [pg.image.load('images/barrier_explosion' + str(i) + '.png') for i in range(10)]

    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, screen, image, rect):
        super().__init__()
        self.image = image
        self.screen = screen
        self.rect = rect
        self.health = 5

    def damaged(self):
        if self.health >= 0:
            self.health -= 1

    def update(self):
        pil_image = pg.image.tostring(self.image, 'RGBA', False)
        img = Image.frombytes('RGBA', (16, 15), pil_image)
        img = img.convert('RGBA')
        data = img.getdata()

        newData = []
        for item in data:
            num = randint(0, 5)
            if num == 1:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)

        mode = img.mode
        size = img.size
        data = img.tobytes()

        py_image = pg.image.fromstring(data, size, mode)

        self.image = py_image

    def draw(self):
        self.screen.blit(self.image, self.rect)
