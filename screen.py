import ctypes
from itertools import cycle

import pygame
from pygame import transform

from constants import *


class Display:
    """Manages the display for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize the screen."""
        self.ai_game = ai_game
        self.settings = ai_game.settings

        # Enable DPI detection
        ctypes.windll.user32.SetProcessDPIAware()

        # Get information about the users screen size
        infoObject = pygame.display.Info()
        self.width = infoObject.current_w
        self.height = infoObject.current_h

        # Calculate factor for scaling images based on native resolution and screen size
        self.scale_factor = self.width / self.settings.screen_width

        # Change screen size dependent settings
        self.settings.scale_settings(self.scale_factor)

        # Initialize screen
        self.surface = pygame.Surface((self.width, self.height))
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

    def initialize_object_attributes(self, ai_game):
        """Initilize attributes associated with objects created after the Display object itself."""
        self.ship_bullets = ai_game.ship_bullets
        self.alien_bullets = ai_game.alien_bullets
        self.aliens = ai_game.aliens
        self.explosions = ai_game.explosions
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.ship = ai_game.ship

    def create_buttons(self):
        """Create the various buttons to be displayed"""
        # The buttons are created in the center of the screen then offset in the x/y directions by a number of button
        # widths. E.g. The "-1, 0" for the easy button means to shift the button one button width left of center.
        self.easy_button = Button(self.ai_game, "Easy", -1, 0)
        self.normal_button = Button(self.ai_game, "Normal", 0, 0)
        self.hard_button = Button(self.ai_game, "Hard", 1, 0)
        self.quit_button = Button(self.ai_game, "Quit", 0, 1)
        self.buttons = (self.easy_button, self.normal_button,
                        self.hard_button, self.quit_button)

    def create_start_screen(self):
        """Create the game start screen."""
        titleFont = pygame.font.Font(
            TITLE_FONT, int(self.scale_factor * LARGE_FONT))
        font = pygame.font.SysFont(None, int(self.scale_factor * SMALL_FONT))

        # Create and position the title text
        self.title_text = titleFont.render(
            GAME_TITLE, True, DARK_GREEN, self.settings.bg_color)
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = self.screen.get_rect().center
        self.title_text_rect.centery -= self.title_text_rect.height

        # Create and position blinking "press any key" text
        # Render the text to display
        self.on_text = font.render(
            START_GAME_TEXT, True, BLACK, self.settings.bg_color)
        # Position the rect object for the blinking text
        self.blink_rect = self.on_text.get_rect()
        self.blink_rect.center = self.screen.get_rect().center
        self.blink_rect.centery += ELEMENT_SPACING * self.title_text_rect.height
        # Set the off_text surface and fill it in with the background color
        self.off_text = pygame.Surface(self.blink_rect.size)
        self.off_text.fill(self.settings.bg_color)
        # Create an iterator that repreatedly iterates over the two elements "on_text" and "off_text"
        self.blink_surfaces = cycle([self.on_text, self.off_text])
        # Create a variable to store the next value from the iterator
        self.blink_surface = next(self.blink_surfaces)
        # Define a new event (events are represented by integers, with pygame.USEREVENT have the highest value pygame uses)
        self.BLINKEVENT = pygame.USEREVENT + 1
        # Set a timer to trigger a BLINKEVENT
        pygame.time.set_timer(self.BLINKEVENT, BLINK_DURATION)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def display_start_screen(self):
        """Display the game start screen."""

        # Set a timer for displaying demo gameplay
        DEMOEVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(DEMOEVENT, DEMO_GAMEPLAY_TIMER)

        # Set the while loop for the start screen
        while True:
            self.surface.fill(self.settings.bg_color)
            self.surface.blit(self.title_text, self.title_text_rect)

            for event in pygame.event.get():
                # Reset the game state in response to user input in case of demo gameplay
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.ai_game.reset_level()
                    self.stats.reset_stats()
                    self.sb.prep_images()
                    return
                # Blink the start game text at every BLINKEVENT
                if event.type == self.BLINKEVENT:
                    self.blink_surface = next(self.blink_surfaces)
                # Run demo gameplay in response to a DEMOEVENT
                if event.type == DEMOEVENT:
                    self.ai_game.run_demo()

            self.surface.blit(self.blink_surface, self.blink_rect)
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()

    def create_game_over_msg(self):
        """Create the message to display at game over."""
        font = pygame.font.SysFont(None, int(self.scale_factor * LARGE_FONT))

        # Create and position the game over text
        # Render the text to display
        self.game_over_text = font.render(
            GAME_OVER_TEXT, True, BLACK)
        self.game_over_text_rect = self.game_over_text.get_rect()
        self.game_over_text_rect.center = self.screen.get_rect().center
        self.game_over_text_rect.centery -= ELEMENT_SPACING * \
            self.game_over_text_rect.height

    def update_screen(self, ai_game):
        """Update images on the screen, and flip to the new screen."""
        self.surface.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.ship_bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.surface)
        self.explosions.draw(self.surface)

        # Draw the score information.
        self.sb.show_score()

        # Draw the difficulty buttons if the game is inactive.
        if not self.stats.game_active:
            for button in self.buttons:
                button.draw_button()

        # Draw the game over message if appropriate
        if self.stats.game_over:
            self.surface.blit(self.game_over_text, self.game_over_text_rect)

        # Make the most recently drawn screen visible.
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()


class Button:

    def __init__(self, ai_game, msg, x1, y1):
        """Initialize button attributes."""
        self.sf = ai_game.display.scale_factor
        self.screen = ai_game.display.screen
        self.surface = ai_game.display.surface

        # Set the dimensions and properties of the button.
        self.width, self.height = 200 * self.sf, 50 * self.sf
        self.button_color = LIGHT_GREEN
        self.text_color = WHITE
        self.font = pygame.font.SysFont(None, int(self.sf * SMALL_FONT))

        # Build the botton's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen.get_rect().center
        # Move the button to its proper location
        self.rect.x += x1 * self.width
        self.rect.y += y1 * self.height

        # Prep the button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message"""
        self.surface.fill(self.button_color, self.rect)
        self.surface.blit(self.msg_image, self.msg_image_rect)
