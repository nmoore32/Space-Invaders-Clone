import sys

import pygame as pg


class EventHandler:

    def __init__(self, ai_game):
        """Initialize attributes."""
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.display = ai_game.display
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.ship = ai_game.ship

    def check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.ai_game.quit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_q:
            self.ai_game.quit()
        elif event.key == pg.K_SPACE:
            self.ship.fire_bullet()
        elif event.key == pg.K_e and not self.stats.game_active:
            self.settings.set_difficulty(self.settings.easy)
            self.ai_game.start_game()
        elif event.key == pg.K_n and not self.stats.game_active:
            self.settings.set_difficulty(self.settings.normal)
            self.ai_game.start_game()
        elif event.key == pg.K_h and not self.stats.game_active:
            self.settings.set_difficulty(self.settings.hard)
            self.ai_game.start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _check_button(self, mouse_pos):
        """Set the difficulty setting."""
        if self.display.easy_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty(self.settings.easy)
            self.ai_game.start_game()
        elif self.display.normal_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty(self.settings.normal)
            self.ai_game.start_game()
        elif self.display.hard_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty(self.settings.hard)
            self.ai_game.start_game()
        elif self.display.quit_button.rect.collidepoint(mouse_pos):
            self.ai_game.quit()
