from constants import LIGHT_GRAY, PURPLE, RED, SCREEN_HEIGHT, SCREEN_WIDTH


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.bg_color = LIGHT_GRAY

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.ship_bullet_color = PURPLE
        self.alien_bullet_color = RED
        self.ship_bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # Difficulty settings (initial speeds multiplied by speedup_scale ** diff)
        self.easy = 1
        self.normal = 2
        self.hard = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.alien_bullets_allowed = 1

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def scale_settings(self, scale_factor):
        """ Scale the bullet size and rate of fleet movement down the screen based on screen size."""
        self.bullet_width *= scale_factor
        self.bullet_height *= scale_factor
        self.fleet_drop_speed *= scale_factor

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, difficulty):
        """Set the games difficulty."""
        self.alien_bullets_allowed *= difficulty
