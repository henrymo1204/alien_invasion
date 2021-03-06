class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (30, 30, 30)

        self.ship_limit = 2
        self.bullet_width = 5
        self.bullet_height = 30
        self.bullet_color = 255, 0, 0
        self.bullets_every = 300

        self.fleet_drop_speed = 10
        self.debounce = 0.0001

        self.score_scale = 1.5
        self.one_eye_alien_points = 50
        self.two_eye_alien_points = 100
        self.three_eye_alien_points = 500
        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        self.ship_speed_factor = 9
        self.bullet_speed_factor = 5
        self.alien_speed = 1
        self.ufo_speed = 1
        self.fleet_direction = 1
        self.ufo_fleet_direction = 1
        self.alien_points = 50
        self.speedup_scale = 1.1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.bullet_speed_factor *= scale
        self.alien_speed *= scale
