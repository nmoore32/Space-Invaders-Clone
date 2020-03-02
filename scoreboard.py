import pygame.ftfont
from pygame.sprite import Group

from constants import BLACK, ELEMENT_EDGE_OFFSET, SCREEN_EDGE_OFFSET, SMALL_FONT
from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.display.screen
        self.surface = ai_game.display.surface
        self.sf = ai_game.display.scale_factor
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = BLACK
        self.font = pygame.font.SysFont(None, int(self.sf * SMALL_FONT))

        # Prepare the initial score images.
        self.prep_images()

    def prep_images(self):
        """Prepare the images to be used for scoring."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        # Round the score to the nearest 10
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen.get_rect().right - SCREEN_EDGE_OFFSET
        self.score_rect.top = SCREEN_EDGE_OFFSET

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen.get_rect().centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + ELEMENT_EDGE_OFFSET

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = ELEMENT_EDGE_OFFSET + ship_number * ship.rect.width
            ship.rect.y = ELEMENT_EDGE_OFFSET
            self.ships.add(ship)

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.surface.blit(self.score_image, self.score_rect)
        self.surface.blit(self.high_score_image, self.high_score_rect)
        self.surface.blit(self.level_image, self.level_rect)
        self.ships.draw(self.surface)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def record_high_score(self):
        high_score = round(self.stats.high_score, -1)
        try:
            outf = open("highscore_alien_invasion.txt", "w")
            outf.write(f"{high_score}")
            outf.close()
        except:
            print("Error recording high score.")
