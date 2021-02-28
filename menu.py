import pygame as pg

from pygame.sysfont import SysFont
from pygame.sprite import Sprite
from timer import Timer

class Button:
    """Represents a click-able button style text, with altering text color"""
    def __init__(self, settings, screen, msg, y_factor=0.65):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.alt_color = (255, 215, 0)
        self.font = SysFont(None, 48)
        self.y_factor = y_factor

        # Prep button message
        self.msg = msg
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(self.text_color)

    def check_button(self, mouse_x, mouse_y):
        """Check if the given button has been pressed"""
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    def alter_text_color(self, mouse_x, mouse_y):
        """Change text color if the mouse coordinates collide with the button"""
        if self.check_button(mouse_x, mouse_y):
            self.prep_msg(self.alt_color)
        else:
            self.prep_msg(self.text_color)

    def prep_msg(self, color):
        """Turn msg into a rendered image and center it on the button"""
        self.msg_image = self.font.render(self.msg, True, color, self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = (self.settings.screen_width // 2)
        self.msg_image_rect.centery = int(self.settings.screen_height * self.y_factor)

    def draw_button(self):
        """blit message to the screen"""
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Title:
    """Represents the title text to be displayed on screen"""
    def __init__(self, bg_color, screen, text, text_size=56, text_color=(255, 255, 255)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = SysFont("Broadway", text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def draw(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)


class Points:
    """Represents the subtitle text displayed on screen"""
    def __init__(self, bg_color, screen, text, text_size=48, text_color=(255, 255, 255)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = SysFont(None, text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def draw(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)

class Intro:
    """Contains information and methods relating to the start menu"""
    def __init__(self, settings, stats, screen):
        # settings, settings, stats
        self.settings = settings
        self.game_stats = stats
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # text/image information
        self.title = Title(settings.bg_color, self.screen, 'ALIEN', text_size=72)
        self.subtitle = Title(settings.bg_color, self.screen, 'INVASION', text_size=68, text_color=(0, 255, 0))
        self.point_alien1 = Points(settings.bg_color, self.screen, '=   111', text_size=48)
        self.point_alien2 = Points(settings.bg_color, self.screen, '=   222', text_size=48)
        self.point_alien3 = Points(settings.bg_color, self.screen, '=   333', text_size=48)
        self.point_alien4 = Points(settings.bg_color, self.screen, '=   444', text_size=48)

        self.prep_image()

    def prep_image(self):
        """Render the title as an image"""
        # title ALIEN
        self.title.prep_image()
        self.title.image_rect.centerx = self.screen_rect.centerx
        self.title.image_rect.top = self.screen_rect.top
        # subtitle INVASION
        self.subtitle.prep_image()
        self.subtitle.image_rect.centerx = self.screen_rect.centerx
        self.subtitle.image_rect.top = self.title.image_rect.bottom
        # Alien1 Point
        self.point_alien1.prep_image()
        self.point_alien1.image_rect.centerx = self.screen_rect.centerx + 50
        self.point_alien1.image_rect.top = self.subtitle.image_rect.bottom + 50
        # Alien2 Point
        self.point_alien2.prep_image()
        self.point_alien2.image_rect.centerx = self.screen_rect.centerx + 50
        self.point_alien2.image_rect.top = self.subtitle.image_rect.bottom + 130
        # Alien3 Point
        self.point_alien3.prep_image()
        self.point_alien3.image_rect.centerx = self.screen_rect.centerx + 50
        self.point_alien3.image_rect.top = self.subtitle.image_rect.bottom + 210
        self.point_alien4.prep_image()
        self.point_alien4.image_rect.centerx = self.screen_rect.centerx + 50
        self.point_alien4.image_rect.top = self.subtitle.image_rect.bottom + 290

    def draw(self):
        """Draw the title to the screen"""
        self.title.draw()
        self.subtitle.draw()
        self.point_alien1.draw()
        self.point_alien2.draw()
        self.point_alien3.draw()
        self.point_alien4.draw()


class MenuAliens:
    def __init__(self, settings, screen, menu_alien_group, ship_height, game, stats, sb, bullets=None):
        self.settings = settings
        self.aliens = menu_alien_group
        self.screen = screen
        self.game = game
        self.ship_height = ship_height
        self.bullets = bullets
        self.stats = stats
        self.sb = sb
        self.create_fleet()

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        alien = Alien(settings=settings, screen=self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height + 15
        aliens_per_row = 1
        rows_per_screen = 3

        for y in range(rows_per_screen):
            for x in range(aliens_per_row):
                alien = Alien(settings=settings, screen=screen, number=y, x=alien_width * (4 + 1.5 * x), y=alien_height * (1.4 * (1 + y)), bullets=self.bullets, shooting=True)
                self.aliens.add(alien)

    def add(self, alien): self.aliens.add(alien)

    def remove(self, alien): self.aliens.aliens.remove(alien)

    def change_direction(self):
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): return True
        return False

    def check_aliens_bottom(self):
        r = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom > r.bottom:
                return True
        return False

    def update(self):
        self.aliens.update()
        if self.check_edges(): self.change_direction()
        if self.check_aliens_bottom() or pg.sprite.spritecollideany(self.game.ship, self.aliens):
            # print("Resetting game")
            self.game.reset()
            return

        # for y in range(rows_per_screen):
        #     for x in range(aliens_per_row):
        # row = 5
        for alien in self.aliens.copy():
            alien.update()
            if alien.rect.bottom <= 0 or alien.reallydead:
                self.aliens.remove(alien)
                self.explosion_group.remove(alien)

    def draw(self):
        for alien in self.aliens.sprites(): alien.draw()


class Alien(Sprite):   # INHERITS from SPRITE
    images = [[pg.image.load('images/three_eye_alien' + str(i) + '.png') for i in range(8)],
              [pg.image.load('images/two_eye_alien' + str(i) + '.png') for i in range(4)],
              [pg.image.load('images/one_eye_alien' + str(i) + '.png') for i in range(4)]]

    timers = []
    for i in range(3):
        timers.append(Timer(frames=images[i], wait=700))

    def __init__(self, settings, screen, number=0, x=0, y=0, speed=0, bullets=None, shooting=False):
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

        self.timer = Alien.timers[number]

        # Location of the alien in Menu
        self.rect = self.timer.imagerect().get_rect()
        self.rect.x = self.x = 500
        self.rect.y = self.y = y + 110
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.speed = speed

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right >= rscreen.right or r.left <= 0

    def update(self):
        if self.dead and not self.timer_switched:
            self.timer = Timer(frames=Alien.images_boom, wait=100, looponce=True)
            self.timer_switched = True
        elif self.dead and self.timer_switched:
            # print("switched to boom timer", self.timer_boom.frame_index(), len(Alien.images_boom))
            if self.timer.frame_index() == len(Alien.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.timer.reset()
        if not self.timer_switched:
            delta = self.settings.alien_speed * self.settings.fleet_direction
            self.rect.x += delta
            self.x = self.rect.x

    def draw(self):
        # image = Alien.images[self.number]
        # self.screen.blit(image, self.rect)
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

    @staticmethod
    def run_tests():
        print(Alien.images)
