class GameStats:
    """Tracks the game state and score (no file access here)."""

    def __init__(self, settings, storage):

        self.settings = settings

        self.state = "menu"

        self.reset_stats()

        # The high score is never reset during a session.
        self.high_score = storage.load()

    def reset_stats(self):

        self.score = 0

        self.last_reward = 0

        self.level = 0