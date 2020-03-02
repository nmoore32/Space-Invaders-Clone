from time import sleep

import pygame
from pygame import mixer

from explosion import Explosion


class CollisionHandler:
    """A class to manage collisions."""

    def __init__(self, ai_game):
        """Initialize attributes the class needs access to"""
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.display.screen
        self.ship_bullets = ai_game.ship_bullets
        self.alien_bullets = ai_game.alien_bullets
        self.aliens = ai_game.aliens
        self.explosions = ai_game.explosions
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.ship = ai_game.ship
        self.lose_life_sound = mixer.Sound('sound_effects/lose_life.wav')

    def check_bullet_alien_collisions(self):
        """Response to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.ship_bullets, self.aliens, True, True)

        # Increase score and generate explosions if appropriate
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    self.explosions.add(
                        Explosion(self.ai_game, alien))
            self.sb.prep_score()
            # Don't increase the high score during demo gameplay
            if not self.stats.game_demo:
                self.sb.check_high_score()

        # Start a new level if there are no more aliens
        if not self.aliens and not self.explosions:
            self.ai_game.start_new_level()

    def check_bullet_ship_collisions(self):
        """Response to bullet-ship collisions."""
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

    def check_alien_ship_collisions(self):
        """Check for collisions between aliens and the ship."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def check_bullet_bullet_collisions(self):
        """Check for collisions between ship bullets and alien bullets."""
        # Remove any bullets that have collided.
        collisions = pygame.sprite.groupcollide(
            self.ship_bullets, self.alien_bullets, True, True)

    def check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Pause the background music and play sound effect for getting hit
            pygame.mixer.music.pause()
            self.lose_life_sound.play()

            # Pause
            sleep(2)

            # Reset the current level
            self.ai_game.reset_level()
        else:
            self.ai_game.game_over()
