class GameStats():
    """Tracks the game state and score."""

    def __init__(self, settings):
        self.settings = settings
        self.state = "menu"        # menu / playing / won / lost
        self.last_reward = 0
        self.reset_stats()

        # The high score is never reset during a session.
        self.high_score = self._load_high_score()

    def reset_stats(self):
        self.score = 0
        self.last_reward = 0

    @staticmethod
    def _load_high_score():
        try:
            with open("highest_score.txt", "r") as file:
                return int(file.readline().strip() or 0)
        except (FileNotFoundError, ValueError):
            return 0