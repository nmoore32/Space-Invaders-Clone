class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False
        self.game_demo = False
        self.game_over = False

        # High score should never be reset.
        try:
            inf = open("highscore_alien_invasion.txt")
            parts = inf.readline().split()
            self.high_score = int(parts[0])
            inf.close()
        except:
            self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
