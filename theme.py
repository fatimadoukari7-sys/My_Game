"""THE LOOK OF THE GAME - the only file you edit to change the appearance.

Pictures, sounds, colors, fonts and texts are all here.
The game logic (combat, game_flow, shooter, monster_brain ...) never reads
a file name or a color directly: it only uses what the display classes
take from this file.

Resources are in independent folders:
    resources/images/hero/         the player pictures
    resources/images/monsters/     the monster pictures
    resources/images/bullets/      the bullet picture (optional)
    resources/images/backgrounds/  the background pictures
    resources/sounds/              the sounds
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resource(*parts):
    """Full path of a file inside the resources folder."""
    return os.path.join(BASE_DIR, "resources", *parts)


# ----------------------------------------------------------------------
# Window and texts
# ----------------------------------------------------------------------
WINDOW_CAPTION = "Hero vs Monster"

TEXTS = {
    "title": "Hero vs Monster",
    "play_button": "Play",
    "win": "YOU WIN!",
    "level_complete": "Level complete!",
    "game_over": "GAME OVER",
    "out_of_ammo": "Out of ammo! Run!",
    "reward": "Reward: +{:,}",
    "score": "Score: {:,}",
    "high_score": "High Score: {:,}",
    "ammo": "Ammo: {}",
    "level": "Level: {}/{}",
    "kills": "Kills: {}/{}",          # level 3
}

# ----------------------------------------------------------------------
# Background
# ----------------------------------------------------------------------
BACKGROUND_IMAGE = resource("images", "backgrounds", "space.jpg")
BACKGROUND_SPEED = 5            # scrolling speed (pixels per frame)
BACKGROUND_COLOR = (22, 20, 25)

# ----------------------------------------------------------------------
# Hero pictures
# ----------------------------------------------------------------------
HERO_HEIGHT = 90                # height of the hero on the screen (pixels)
HERO_FALLBACK_COLOR = (80, 180, 90)   # shown only if the stop picture is missing

HERO_IMAGES = {
    "stop":  resource("images", "hero", "stop.png"),    # nothing is pressed
    "fire":  resource("images", "hero", "fire.png"),    # fire key (space)
    "left":  resource("images", "hero", "left.png"),    # left arrow
    "right": resource("images", "hero", "right.png"),   # right arrow
    "up":    resource("images", "hero", "up.png"),      # up arrow
}

HEART_HEIGHT = 30               # the lives shown at the top left

# ----------------------------------------------------------------------
# Monsters: one look per level (same order as levels.py)
# ----------------------------------------------------------------------
MONSTER_LOOKS = [
    {"image": resource("images", "monsters", "pikachu.png"), "scale": 1.0},
    {"image": resource("images", "monsters", "monster_lev2.png"), "scale": 0.25},
]

# ----------------------------------------------------------------------
# LEVEL 3: the flying monsters
# ----------------------------------------------------------------------
FLYING_ENEMY = {
    "image": resource("images", "monsters", "monster3.png"),
    "height": 80,               # their height on the screen (pixels)
}

# ----------------------------------------------------------------------
# Bullets
# ----------------------------------------------------------------------
BULLET_SIZE = (23, 23)
BULLET_COLOR = (255, 220, 60)
# Put a picture here to replace the yellow ball, for example:
# resource("images", "bullets", "bullet.png")
BULLET_IMAGE = None

# The monster's fireball (level 2): outer and inner colors.
FIREBALL_OUTER_COLOR = (255, 120, 20)
FIREBALL_INNER_COLOR = (255, 230, 90)

# ----------------------------------------------------------------------
# Sounds
# ----------------------------------------------------------------------
SHOOT_SOUND = resource("sounds", "shoot.mp3")

# ----------------------------------------------------------------------
# Colors
# ----------------------------------------------------------------------
TEXT_COLOR = (30, 130, 230)
RED = (230, 40, 40)
GREEN = (60, 220, 90)
YELLOW = (255, 220, 60)
WHITE = (255, 255, 255)

# ----------------------------------------------------------------------
# Fonts (size only: the default pygame font is used)
# ----------------------------------------------------------------------
FONT_SMALL = 40                 # score, ammo, level
FONT_BIG = 80                   # big messages
FONT_BUTTON = 48

# ----------------------------------------------------------------------
# Play button
# ----------------------------------------------------------------------
BUTTON_SIZE = (240, 65)
BUTTON_COLOR = (170, 70, 110)
BUTTON_TEXT_COLOR = (255, 255, 255)

# ----------------------------------------------------------------------
# Monster health bar
# ----------------------------------------------------------------------
MONSTER_BAR_WIDTH = 200
HEALTH_BAR_BACK_COLOR = (40, 40, 40)
HEALTH_BAR_BORDER_COLOR = (15, 15, 15)
HEALTH_BAR_FULL_COLOR = (60, 220, 90)    # green: full health
HEALTH_BAR_LOW_COLOR = (230, 40, 40)     # red: almost no health