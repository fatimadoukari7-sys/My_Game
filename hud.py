from score_display import ScoreDisplay
from status_display import StatusDisplay
from message_display import MessageDisplay
from monster_bar_display import MonsterBarDisplay
from wave_display import WaveDisplay


class HUD:
    """The information panel: puts the display parts together."""

    def __init__(self, settings, screen, stats, hero, monster, waves=None):
        self.stats = stats
        self.waves = waves

        self.score = ScoreDisplay(screen, stats)
        self.status = StatusDisplay(settings, screen, stats, hero)
        self.messages = MessageDisplay(settings, screen, stats, hero)
        self.monster_bar = MonsterBarDisplay(screen, stats, monster)
        self.wave_display = WaveDisplay(screen, stats, waves) if waves else None

    def prep_images(self):
        self.score.prep_score()
        self.score.prep_high_score()

    def prep_score(self):
        self.score.prep_score()

    def prep_high_score(self):
        self.score.prep_high_score()

    def show(self):
        self.score.draw()
        self.status.draw(self.score.score_rect)
        if self.waves and self.waves.active:
            self.wave_display.draw(self.score.high_score_rect)     # level 3
        else:
            self.monster_bar.draw(self.score.high_score_rect)      # levels 1-2
        self.messages.draw()