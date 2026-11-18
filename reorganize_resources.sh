#!/bin/bash
# Run ONCE from the project folder (where main.py is):  bash reorganize_resources.sh
# It moves your pictures and sounds into independent folders and gives them
# the names used in theme.py. Files that do not exist are skipped.

set -u
mkdir -p resources/images/hero resources/images/monsters \
         resources/images/bullets resources/images/backgrounds resources/sounds

move() {    # move SOURCE DESTINATION
    if [ -f "$1" ]; then
        mv -n "$1" "$2" && echo "moved: $1 -> $2"
    else
        echo "skipped (not found): $1"
    fi
}

# Hero
move images/Gerero/gereroStop.png resources/images/hero/stop.png
move images/Gerero/Gerero.png     resources/images/hero/fire.png
move images/Gerero/left1.png      resources/images/hero/left.png
move images/Gerero/right.png      resources/images/hero/right.png
move images/Gerero/up.png         resources/images/hero/up.png

# Monsters
move images/pikachu.png           resources/images/monsters/pikachu.png
move images/monster_lev2.png      resources/images/monsters/monster_lev2.png

# Background
move 417403_980.jpg               resources/images/backgrounds/space.jpg

# Sounds
move music/Crash_Metal_Sweetener_Distant.mp3 resources/sounds/shoot.mp3