import pygame as pg
from pygame import gfxdraw, mixer
from pygame.sprite import Sprite

from constants import EXPLOSION_DURATION, RED


class Explosion(Sprite):
    """A Class to manage explosions."""

    def __init__(self, ai_game, alien):
        """Initialize attributes and draw the explosion."""
        super().__init__()
        self.explosions = ai_game.explosions

        # Set the surface for the explosion equal to height of the aliens
        self.height = int(alien.rect.height)
        self.radius = int(alien.rect.height / 2)
        self.image = pg.Surface(
            (self.height, self.height), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = alien.rect.center

        # Track time in order to specify duration of explosion
        self.clock = pg.time.Clock()
        self.last_update = 0

        # Draw the explosion
        pg.gfxdraw.aacircle(self.image, self.radius,
                            self.radius, self.radius, RED)
        pg.gfxdraw.filled_circle(
            self.image, self.radius, self.radius, self.radius, RED)

        # Load and play explosion sound
        self.explosion_sound = mixer.Sound('sound_effects/explosion.wav')
        self.explosion_sound.play()

    def update(self):
        """Update the explosion."""
        # Remove the explosion after a set amount of time
        self.last_update += self.clock.tick()
        if self.last_update > EXPLOSION_DURATION:
            self.explosions.remove(self)

    def blitme(self):
        """Draw the explosion."""
        self.surface.blit(self.image, self.rect)
