import pygame as pg
from pygame.sprite import Sprite
from pygame import mixer

from constants import SCREEN_EDGE_OFFSET, SHIP_IMG
from projectiles import ShipBullet


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.display = ai_game.display
        self.screen = self.display.screen
        self.surface = self.display.surface
        self.ship_bullets = ai_game.ship_bullets
        self.ship_bullet_sound = mixer.Sound('sound_effects/laser.wav')

        # Load the ship image and get its rect.
        self.image = SHIP_IMG
        self.rect = self.image.get_rect()

        # Scale the image if necessary based on screen size
        if self.display.scale_factor != 1:
            self._scale_ship()

        # Store a decimal value for the ship's position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def _scale_ship(self):
        """Scale the ship image based on screen size."""
        width = int(self.rect.width * self.display.scale_factor)
        height = int(self.rect.height * self.display.scale_factor)
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen.get_rect().right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.surface.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.centerx = self.screen.get_rect().centerx
        # Place it slightly above the bottom of the screen
        self.rect.bottom = self.screen.get_rect().bottom - SCREEN_EDGE_OFFSET
        self.x = float(self.rect.x)

    def fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.ship_bullets) < self.settings.ship_bullets_allowed:
            new_bullet = ShipBullet(self.ai_game)
            self.ship_bullets.add(new_bullet)
            self.ship_bullet_sound.play()
