# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
OPPOSITE_DIRECTIONS = {UP: DOWN,
                       DOWN: UP,
                       LEFT: RIGHT,
                       RIGHT:LEFT,
                       None: None}
NUM_OUTPUT_NODES = len(DIRECTIONS)

EMPTY_TILE = "."
TAIL_TILE = "+"
PLAYER_TILE = "O"
TILE_TYPE_TO_WEIGHT = {EMPTY_TILE: 0,
                       TAIL_TILE: 1,
                       PLAYER_TILE: 1}

UP_INNOVATION = 0
DOWN_INNOVATION = 1
LEFT_INNOVATION = 2
RIGHT_INNOVATION = 3
INNOVATION_TO_DIRECTION = {UP_INNOVATION: UP,
                           DOWN_INNOVATION: DOWN,
                           LEFT_INNOVATION: LEFT,
                           RIGHT_INNOVATION: RIGHT}

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TILE_SIZE = 16

BOARD_WIDTH = 22
BOARD_HEIGHT = 22
BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT
SPAWN_LOCATIONS = ((BOARD_WIDTH//4, BOARD_HEIGHT//4),
                   (BOARD_WIDTH//4, 3*BOARD_HEIGHT//4),
                   (3*BOARD_WIDTH//4, 3*BOARD_HEIGHT//4),
                   (3*BOARD_WIDTH//4, BOARD_HEIGHT//4))

WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
GREEN = (90, 180, 105)
DARK_GREEN = (40, 100, 45)
COLOR_LOOKUP = {EMPTY_TILE: DARK_GRAY,
                PLAYER_TILE: GREEN,
                TAIL_TILE: DARK_GREEN}

# Population constants
POPULATION_SIZE = 200
POPULATION_KEEP = 0.2

# NEAT constants
INTERSPECIES_MATING_PROB = 0.001
OFFSPRING_MUTATION_FRACTION = 0.25
INHERIT_DISABLED_PROB = 0.75
NEW_EDGE_MUTATION_PROB = 0.5  # This proportion of mutations are new edges; the rest are new nodes

EDGE_MUTATION_PROB = 0.2  # Each edge has this chance of mutating each time step
EDGE_MUTATION_STD_DEV = 1.5
EDGE_PERTURBATION_PROB = 0.95
EDGE_RESET_STD_DEV = 2.5

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
