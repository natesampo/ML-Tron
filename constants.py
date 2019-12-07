# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

EMPTY_TILE = "."
TAIL_TILE = "+"
PLAYER_TILE = "O"

UP_INNOVATION = 0
DOWN_INNOVATION = 1
LEFT_INNOVATION = 2
RIGHT_INNOVATION = 3
INNOVATION_TO_DIRECTION = {UP: UP_INNOVATION,
                           DOWN: DOWN_INNOVATION,
                           LEFT: LEFT_INNOVATION,
                           RIGHT: RIGHT_INNOVATION}

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

# Population constants
POPULATION_SIZE = 10

# NEAT constants
INTERSPECIES_MATING_PROB = 0.001
OFFSPRING_MUTATION_FRACTION = 0.25
INHERIT_DISABLED_PROB = 0.75
NEW_EDGE_MUTATION_PROB = 0.5  # This proportion of mutations are new edges; the rest are new nodes

GENOME_WEIGHT_CHANGE_PROB = 0.8
RANDOM_WEIGHT_PROB = 0.1

EXCESS_DIFFERENCE_COEFF = 1
DISJOINT_DIFFERENCE_COEFF = 1
WEIGHT_DIFFERENCE_COEFF = 0.1
SPECIES_THRESHOLD = 3

STAGNANT_TURNS = 15
MIN_NETWORKS_FOR_CHAMPION = 5

GAUSSIAN_DISTRIBUTION = 0.2
NORMAL_DISTRIBUTION = 2

# Scoring constants
WIN_SCORE = 100
SURVIVAL_SCORE = 1
