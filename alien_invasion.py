import sys
from math import sqrt
from time import sleep

import pygame
from pygame import mixer

from aliens import AlienFleet
from collision_handler import CollisionHandler
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
        pygame.init()

        # Initialize game settings and display
        self.settings = Settings()
        self.display = Display(self)

        # Create groups to hold bullets, aliens, and explosions
        self.ship_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

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

        # Create game over message
        self.display.create_game_over_msg()

        # Load game start, game over, and background sounds
        self.game_start_sound = mixer.Sound('sound_effects/game_start.wav')
        self.game_over_sound = mixer.Sound('sound_effects/game_over.wav')
        pygame.mixer.music.load('music/background_music.wav')

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Check for and respond to keypresses and mouse clicks.
            self.event.check_events()

            if self.stats.game_active:
                self.ship.update()
                self.projectile.update()
                self.fleet.update()
                self.explosions.update()

            self.display.update_screen(self)

    def run_demo(self):
        """Run demo gameplay."""
        self.stats.game_active = True
        self.stats.game_demo = True
        # Reset everything so each time the demo starts it's a fresh game
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.sb.prep_images()
        self.reset_level()

        while True:
            # Run ai script
            self.run_demo_ai()

            # Run the usual game while loop (minus checking for events)
            self.ship.update()
            self.projectile.update()
            self.fleet.update()
            self.explosions.update()
            self.display.update_screen(self)

            # End the demo gameplay in response to a keypress or mouse button
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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

        #  Determine the nearest alien.
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
                if 0 < bullet.x - self.ship.x < 1.5 * self.ship.rect.width:
                    self.ship.moving_left = True
                    self.ship.moving_right = False
                elif -1.5 * self.ship.rect.width < bullet.x - self.ship.x <= 0:
                    self.ship.moving_left = False
                    self.ship.moving_right = True
                # This last condition is to stop the ship from jittering if there's a bullet between it and the nearest alien.
                elif abs(bullet.x - self.ship.x) == 1.5 * self.ship.rect.width:
                    self.ship.moving_left = False
                    self.ship.moving_right = False

        # Have the ship fire bullets as long as it is close to nearest alien
        if - 2 * self.ship.rect.width <= abs(nearest_alien.x - self.ship.x) <= 2 * self.ship.rect.width:
            self.ship.fire_bullet()

    def start_game(self):
        """Start game play."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.game_over = False
        self.sb.prep_images()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.ship_bullets.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center the ship.
        AlienFleet(self)
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Play the game start sound and background music
        self.game_start_sound.play()
        pygame.mixer.music.set_volume(1)
        sleep(0.5)
        pygame.mixer.music.play(-1)

    def reset_level(self):
        """Reset the current level (occurs when aliens make it to/past the ship)."""
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.ship_bullets.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center the ship.
        AlienFleet(self)
        self.ship.center_ship()

        # Unpause background music
        pygame.mixer.music.unpause()

    def start_new_level(self):
        """Start a new level."""
        # Destroy existing bullets and create new fleet.
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        AlienFleet(self)
        self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.sb.prep_level()

        # Restart the background music
        pygame.mixer.music.rewind()

    def game_over(self):
        """End game play."""
        self.stats.game_active = False
        self.stats.game_over = True
        self.settings.initialize_dynamic_settings()
        # Music file completes current play before stopping, immediate stopping of music done by setting volume to 0
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.stop()
        self.game_over_sound.play()
        sleep(0.5)
        pygame.mouse.set_visible(True)

    def quit(self):
        """Exit the game."""
        self.sb.record_high_score()
        sys.exit()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.display.create_start_screen()
    ai.display.display_start_screen()
    ai.run_game()
