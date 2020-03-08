from random import choice

import pygame as pg
from pygame import mixer
from pygame.sprite import Sprite

from constants import ALIEN_IMG_1, ALIEN_IMG_2, ALIEN_IMG_PANEL_DURATION, ELEMENT_SPACING
from projectiles import AlienBullet


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()

        # AlienInvasion attributes the Alien class methods need access to.
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.display = ai_game.display
        self.screen_rect = self.display.screen.get_rect()
        self.alien_bullets = self.ai_game.alien_bullets
        self.aliens = self.ai_game.aliens

        # Load alien sound effects
        self.alien_bullet_sound = mixer.Sound('sound_effects/laser.wav')

        # Load the alien images (two panel animation)
        self.images = []
        self.images.append(ALIEN_IMG_1)
        self.images.append(ALIEN_IMG_2)

        # Scale the images if necessary based on screen size and set rect attribute
        if self.display.scale_factor != 1:
            self._scale_alien()
        else:
            self.rect = self.images[0].get_rect()

        # Set the first image to use
        self.index = 0
        self.image = self.images[self.index]

        # Initialize variable to track time to determine when to switch between images
        self.clock = pg.time.Clock()
        self.elapsed = 0

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def _scale_alien(self):
        """Scale the aliens size based on screen size."""
        width = int(self.images[0].get_rect().width *
                    self.display.scale_factor)
        height = int(self.images[0].get_rect().height *
                     self.display.scale_factor)
        for i in range(len(self.images)):
            self.images[i] = pg.transform.scale(
                self.images[i], (width, height))
        self.rect = self.images[0].get_rect()

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left, update image, and fire bullets."""
        # Update the aliens horizontal position
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x

        # Increment time elapsed by time since method was last called
        self.elapsed += self.clock.tick()

        # Change alien image to next panel if enough time has elapsed
        if self.elapsed >= ALIEN_IMG_PANEL_DURATION:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.elapsed = 0

        # Attempt to fire a bullet
        self.fire_bullet()

    def fire_bullet(self):
        """Create a new bullet and add it to the alien bullets group."""
        if len(self.alien_bullets) < self.settings.alien_bullets_allowed:
            new_bullet = AlienBullet(
                self.ai_game, choice(self.aliens.sprites()))
            self.alien_bullets.add(new_bullet)
            self.alien_bullet_sound.play()


class AlienFleet():
    """A class to manage an alien fleet."""

    def __init__(self, ai_game):
        """Initialize an alien fleet."""
        # AlienInvasion attributes the AlienFleet class methods need access to
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        self.aliens = ai_game.aliens

        # Create an alien and find the number of aliens in a row.
        alien = Alien(ai_game)
        alien_width, alien_height = alien.rect.size
        # Leave a gap so alien fleet has some room for horizontal movement
        available_space_x = self.settings.screen_width - \
            (ELEMENT_SPACING * alien_width)
        # Number of aliens in row depends on gap defined above and spacing between aliens
        number_aliens_x = available_space_x // (ELEMENT_SPACING * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        # Account for the height of the ship
        available_space_y = (self.settings.screen_height -
                             ((ELEMENT_SPACING) * alien_height) - ship_height)
        # Leave a reasonable space between the bottom row of aliens and the ship
        number_rows = available_space_y // (
            (ELEMENT_SPACING ** 2) * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, ai_game)

    def _create_alien(self, alien_number, row_number, ai_game):
        """Create an alien and place it in the row."""
        alien = Alien(ai_game)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width * (1 + ELEMENT_SPACING * alien_number)
        alien.rect.x = alien.x

        # Ensure top row of aliens is below scoreboard (scoreboard is approximately 2.5 times alien height)
        alien.y = alien_height * (2.5 + ELEMENT_SPACING * row_number)
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def update(self):
        """
        Check if the fleet is at an edge, 
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        self.ai_game.collision.check_alien_ship_collisions()

        # Look for aliens hitting the bottom of the screen.
        self.ai_game.collision.check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
