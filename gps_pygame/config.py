"""Configurations file with all constant values.
"""

# Display
SCREEN_WIDTH = 1330
SCREEN_HEIGHT = 800
FPS = 30

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (240, 20, 20)

# Map
BOARDER_X = 0.015
BOARDER_Y = 0.006
MAP_ZOOM = 15

# Polygon
POLYGON_COLOR = BLACK
X_POS, Y_POS = 190, 205
ROTATION = [150, 210, -30, -60, 0, 60, 30]
RELATIVE = [80, 80, 80, 120, 160, 120, 80]
SCALING = [x / 2 for x in RELATIVE]

# Movement
AXELERATION = 0.1
GLIDING = 0.01
MAX_VEL = 2.0  # Ca. 216 km/h (=2.0 * 30 [FPS] * 3.6)
TURNING = 3

# Moving dot
DOT_COLOR = RED
DOT_SIZE = 5
DOT_FILLED = 0

# Text
TEXT_COLOR = BLACK
VEL_X, VEL_Y = 20, 20
N_X, N_Y = 170, 70
S_X, S_Y = 175, 285
E_X, E_Y = 280, 180
W_X, W_Y = 60, 180
TEXT_SIZE = 50

# Earth mean radius
R_E = 6371e3
