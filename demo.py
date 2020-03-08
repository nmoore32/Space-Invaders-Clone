from math import sqrt

import pygame as pg

from constants import FPS


class Demo():
    """A class to manage demo gameplay."""

    def __init__(self, ai_game):
        """Initialize references to objects the class needs access to."""
        self.ai_game = ai_game
        self.clock = ai_game.clock
        self.settings = ai_game.settings
        self.display = ai_game.display
        self.alien_bullets = ai_game.alien_bullets
        self.aliens = ai_game.aliens
        self.explosions = ai_game.explosions
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.ship = ai_game.ship
        self.fleet = ai_game.fleet
        self.projectile = ai_game.projectile

    def run_demo(self):
        """Run demo gameplay."""
        self.stats.game_active = True
        self.stats.game_demo = True
        # Reset everything so each time the demo starts it's a fresh game
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.sb.prep_images()
        self.ai_game.reset_level()

        while True:
            # Run ai script
            self.run_demo_ai()

            # Run the usual game while loop (minus checking for events)
            self.ship.update()
            self.projectile.update()
            self.fleet.update()
            self.explosions.update()
            self.display.update_screen(self)

            if not self.aliens:
                self.ai_game.start_new_level()

            # Cap fps at 30 frames per second
            time_passed = self.clock.tick(FPS)

            # End the demo gameplay in response to a keypress or mouse button
            for event in pg.event.get():
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    self.stats.game_active = False
                    self.stats.game_demo = False
                    return

            # End the demo when the ship is on its last life (before it triggers a game over)
            if self.stats.ships_left == 0:
                self.stats.game_active = False
                self.stats.game_demo = False
                return

    def run_demo_ai(self):
        """A simple ai script for the ship."""

        # Don't run the demo ai if there are no aliens (e.g. while waiting for next level)
        if not self.aliens:
            return

        #  Determine the nearest alien (if there are any aliens).
        nearest_alien = None
        for alien in self.aliens:
            if nearest_alien == None:
                nearest_alien = alien
            elif (sqrt((alien.x - self.ship.x) ** 2 + (alien.y - self.ship.y) ** 2) <
                    sqrt((nearest_alien.x - self.ship.x) ** 2 + (nearest_alien.y - self.ship.y) ** 2)):
                nearest_alien = alien

        # The ship will move toward the nearest alien until it's two ship-widths away
        if nearest_alien.x - self.ship.x - 2 * self.ship.rect.width > 0:
            self.ship.moving_right = True
            self.ship.moving_left = False
        elif nearest_alien.x - self.ship.x + 2 * self.ship.rect.width < 0:
            self.ship.moving_right = False
            self.ship.moving_left = True
        else:
            self.ship.moving_right = False
            self.ship.moving_left = False

        # If there are bullets close to the ship, it will priotize moving away from them
        if self.alien_bullets:
            for bullet in self.alien_bullets:
                if 0 < bullet.x - self.ship.rect.centerx < 1.5 * self.ship.rect.width:
                    self.ship.moving_left = True
                    self.ship.moving_right = False
                elif -1.5 * self.ship.rect.width < bullet.x - self.ship.rect.centerx <= 0:
                    self.ship.moving_left = False
                    self.ship.moving_right = True
                # This last condition is to stop the ship from jittering if there's a bullet between it and the nearest alien.
                elif (1.5 * self.ship.rect.width <= abs(bullet.x - self.ship.rect.centerx)
                      <= 1.6 * self.ship.rect.width):
                    self.ship.moving_left = False
                    self.ship.moving_right = False

        # Have the ship fire bullets as long as it is close to nearest alien
        if (- 2 * self.ship.rect.width <= abs(nearest_alien.x - self.ship.rect.centerx) <=
                2 * self.ship.rect.width):
            self.ship.fire_bullet()
