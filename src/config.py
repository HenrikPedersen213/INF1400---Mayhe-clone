"""
Configuration constants for the Mayhem Clone game.

All global settings are defined here. Adjust these to tune gameplay.
"""

# Screen
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60
TITLE = "Mayhem Clone"

# Physics
GRAVITY = 0.02          # pixels/frame^2 downward acceleration
THRUST_POWER = 0.12     # acceleration added when thrusting
ROTATION_SPEED = 3.0    # degrees per frame
MAX_SPEED = 8.0         # maximum velocity magnitude

# Bullet
BULLET_SPEED = 10.0
BULLET_LIFETIME = 90    # frames before bullet disappears
MAX_BULLETS = 5         # max bullets per player on screen at once

# Fuel
STARTING_FUEL = 1000
FUEL_BURN_RATE = 1      # fuel units per frame of thrust
REFUEL_RATE = 5         # fuel units per frame when landed

# Scoring
SCORE_KILL = 3
SCORE_CRASH_PENALTY = 1

# Colours (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 60, 60)
BLUE = (60, 120, 220)
GREEN = (60, 200, 100)
YELLOW = (240, 200, 40)
GREY = (100, 100, 110)
DARK_GREY = (30, 30, 35)

# Player 1 controls  (arrow keys)
P1_LEFT  = "left"
P1_RIGHT = "right"
P1_THRUST = "up"
P1_FIRE  = "rctrl"   # right ctrl — change to taste

# Player 2 controls  (WASD + space)
P2_LEFT  = "a"
P2_RIGHT = "d"
P2_THRUST = "w"
P2_FIRE  = "space"