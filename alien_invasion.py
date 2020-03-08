import sys
from math import sqrt
from time import sleep

import pygame as pg
from pygame import mixer

from aliens import AlienFleet
from collision_handler import CollisionHandler
from constants import FPS
from demo import Demo
from screen import Display
from event_handler import EventHandler
from game_stats import GameStats
from projectiles import ProjectileHandler
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        # Initialize pygame settings
        mixer.pre_init(44100, -16, 2, 2048)
        mixer.init()
        pg.init()

        # Create a clock to cap fps
        self.clock = pg.time.Clock()

        # Initialize game settings and display
        self.settings = Settings()
        self.display = Display(self)

        # Create groups to hold bullets, aliens, and explosions
        self.ship_bullets = pg.sprite.Group()
        self.alien_bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self.explosions = pg.sprite.Group()

        # Create an instance to store game statistics, create scoreboard and player ship.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)

        # Initialize the rest of the display settings and create the initial fleet to display
        self.display.initialize_object_attributes(self)
        self.fleet = AlienFleet(self)

        # Create buttons to select difficulty setting
        self.buttons = self.display.create_buttons()

        # Create objects to handle events, projectiles, and collisions
        self.event = EventHandler(self)
        self.projectile = ProjectileHandler(self)
        self.collision = CollisionHandler(self)
        self.demo = Demo(self)

        # Create game over message
        self.display.create_game_over_msg()

        # Load game start, game over, and background sounds
        self.game_start_sound = mixer.Sound('sound_effects/game_start.wav')
        self.game_over_sound = mixer.Sound('sound_effects/game_over.wav')

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Check for and respond to keypresses and mouse clicks
            self.event.check_events()

            if self.stats.game_active:
                self.ship.update()
                self.projectile.update()
                self.fleet.update()
                self.explosions.update()

            self.display.update_screen(self)

            # Start a new level if there are no aliens
            if not self.aliens:
                self.start_new_level()

            # Cap fps at 30 frames per second
            time_passed = self.clock.tick(FPS)

    def start_game(self):
        """Start game play."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.game_over = False
        self.sb.prep_images()

        # Get rid of any remaining aliens, bullets, and explosions.
        self.aliens.empty()
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.explosions.empty()

        # Create a new fleet and center the ship.
        AlienFleet(self)
        self.ship.center_ship()

        # Hide the mouse cursor.
        pg.mouse.set_visible(False)

        # Play the game start sound
        self.game_start_sound.play()
        sleep(0.5)

    def reset_level(self):
        """Reset the current level (occurs when aliens make it to/past the ship)."""
        # Get rid of any remaining aliens, bullets, and explosions.
        self.aliens.empty()
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.explosions.empty()

        # Create a new fleet and center the ship.
        AlienFleet(self)
        self.ship.center_ship()

    def start_new_level(self):
        """Start a new level."""
        # Destroy existing bullets and explosions and create new fleet.
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.explosions.empty()
        AlienFleet(self)
        # Increase game speed if level less than 11 (10 speed increases total)
        if self.stats.level < 11:
            self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()

    def game_over(self):
        """End game play."""
        self.stats.game_active = False
        self.stats.game_over = True
        self.settings.initialize_dynamic_settings()
        self.game_over_sound.play()
        sleep(0.5)
        pg.mouse.set_visible(True)

    def quit(self):
        """Exit the game."""
        self.sb.record_high_score()
        sys.exit()


def main():
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.display.create_start_screen()
    ai.display.display_start_screen(ai.demo)
    ai.run_game()


if __name__ == "__main__":
    main()
