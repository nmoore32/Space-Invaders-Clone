import pygame as pg
from pygame.sprite import Sprite


class Projectile(Sprite):
    """A class for creating projectiles."""

    def __init__(self, ai_game):
        """Initialize projectile attributes."""
        super().__init__()
        self.settings = ai_game.settings
        self.surface = ai_game.display.surface

    def update(self):
        """Move the bullet on the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pg.draw.rect(self.surface, self.color, self.rect)


class ShipBullet(Projectile):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__(ai_game)
        self.ship = ai_game.ship
        self.color = self.settings.ship_bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pg.Rect(0, 0, self.settings.bullet_width,
                            self.settings.bullet_height)
        self.rect.midtop = self.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet on the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y


class AlienBullet(Projectile):
    """A class to manage bullets fired by the aliens."""

    def __init__(self, ai_game, alien):
        """Create a bullet object at the alien's current position."""
        super().__init__(ai_game)
        self.color = self.settings.alien_bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pg.Rect(0, 0, self.settings.bullet_width,
                            self.settings.bullet_height)
        self.rect.midbottom = alien.rect.midbottom

        # Store the bullet's position as a decimal value.
        # Store the x value as well since the demo ai uses this to avoid alien bullets.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet on the screen."""
        # Update the decimal position of the bullet.
        self.y += self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y


class ProjectileHandler():
    """A class to manage projectiles."""
    # This class only has one method other than __init__. However, it allows me initialize all the
    # bullet position updates, bullet removals, and bullet collision checks from one update call.
    # Hence why I don't want to break down its update method into multiple methods or move
    # the checks into the ShipBullet and AlienBullet classes. I also don't what this method in
    # AlienInvasion because it's part of the behind-the-scences logic of how the game works rather
    # than part of the overall main game logic. So, yes, I have a class with two methods, one of
    # which is __init__.

    def __init__(self, ai_game):
        """Initialize attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.display.screen
        self.ship_bullets = ai_game.ship_bullets
        self.alien_bullets = ai_game.alien_bullets

    def update(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.ship_bullets.update()
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.ship_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.ship_bullets.remove(bullet)

        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.screen.get_rect().bottom:
                self.alien_bullets.remove(bullet)

        # Check for collisions
        self.ai_game.collision.check_bullet_alien_collisions()
        self.ai_game.collision.check_bullet_ship_collisions()
        self.ai_game.collision.check_bullet_bullet_collisions()
