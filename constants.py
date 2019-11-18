# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

EMPTY_TILE = "."
TAIL_TILE = "+"
PLAYER_TILE = "O"

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TILE_SIZE = 16

BOARD_WIDTH = 20
BOARD_HEIGHT = 20
BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT

WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
GREEN = (90, 180, 105)
DARK_GREEN = (40, 100, 45)
COLOR_LOOKUP = {EMPTY_TILE: DARK_GRAY,
                PLAYER_TILE: GREEN,
                TAIL_TILE: DARK_GREEN}