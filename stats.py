class GameStats():
    """Tracks the game state and score (no file access here)."""

    def __init__(self, settings, storage):
        self.settings = settings
        self.state = "menu"   # menu / playing / won / lost / level_complete
        self.reset_stats()

<<<<<<< HEAD
        # The high score is never reset during a session.ه
        self.high_score = self._load_high_score()
=======
        # The high score is never reset during a session.
        self.high_score = storage.load()
>>>>>>> 5f7dd43 (Update My Game)

    def reset_stats(self):
        self.score = 0
        self.last_reward = 0
<<<<<<< HEAD

    @staticmethod
    def _load_high_score():
        try:
            with open("highest_score.txt", "r") as file:
                return int(file.readline().strip() or 0)
        except (FileNotFoundError, ValueError):
            return 0
=======
        self.level = 0   # index into settings.levels (0 = level 1)
>>>>>>> 5f7dd43 (Update My Game)
