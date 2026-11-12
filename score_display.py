import pygame.font

from colors import TEXT_COLOR


class ScoreDisplay:
    """Draws the score and the high score."""

    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.font = pygame.font.SysFont(None, 40)
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        text = "Score: {:,}".format(int(self.stats.score))
        self.score_image = self.font.render(text, True, TEXT_COLOR)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        text = "High Score: {:,}".format(int(self.stats.high_score))
        self.high_score_image = self.font.render(text, True, TEXT_COLOR)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 10

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)