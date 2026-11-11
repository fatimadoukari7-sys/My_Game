class HighScoreStorage:
    """Reads and writes the high score file. Nothing else."""

    def __init__(self, path="highest_score.txt"):
        self.path = path

    def load(self):
        try:
            with open(self.path, "r") as file:
                return int(file.readline().strip() or 0)
        except (FileNotFoundError, ValueError):
            return 0

    def save(self, score):
        with open(self.path, "w") as file:
            file.write(str(int(score)))