import pygame

from constants import *

class Controller:
    """ Class for controlling a player. """

    def __init__(self):
        self.direction = UP

    def update(self, events):
        pass

    def get_move(self):
        raise NotImplementedError("Cannot call get_move on superclass")


class KeyboardController(Controller):
    """ Class for controlling a player using keyboard inputs. """

    def __init__(self):
        super().__init__()
        self.scheme = {UP: pygame.K_UP,
                       LEFT: pygame.K_LEFT,
                       RIGHT: pygame.K_RIGHT,
                       DOWN: pygame.K_DOWN}
        self.last_pressed = None

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.scheme.values():
                    self.last_pressed = event.key

    def get_move(self):
        for direction in self.scheme:
            if self.scheme[direction] == self.last_pressed:

                # Don't turn in a direction exactly opposite current movement
                if sorted((self.direction, direction)) not in (sorted((LEFT, RIGHT)), sorted((UP, DOWN))):
                    self.direction = direction
                    self.last_pressed = None

        return self.direction


class WASDController(KeyboardController):
    def __init__(self):
        super().__init__()
        self.scheme = {UP: pygame.K_w,
                       LEFT: pygame.K_a,
                       RIGHT: pygame.K_d,
                       DOWN: pygame.K_s}


def node_number_to_board_offset(n):
    """ Given a node innovation number, calculates the offset from the player of the corresponding node. """
    n = n - NUM_OUTPUT_NODES
    x_offset = n % BOARD_WIDTH
    y_offset = (n//BOARD_WIDTH) % BOARD_HEIGHT
    return x_offset, y_offset


class AgentController(Controller):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.direction = None

    def node_number_to_board_position(self, n):
        """ Returns the position on the game board corresponding to the node number, offset by the
            position of the player corresponding to the current agent (whew!)
        """
        relevant_player = [player for player in self.agent.game.players if player.controller.agent is self.agent][0]
        origin = relevant_player.x, relevant_player.y
        x_offset, y_offset = node_number_to_board_offset(n)
        x = (origin[0] + x_offset) % BOARD_WIDTH
        y = (origin[1] + y_offset) % BOARD_HEIGHT
        return x, y

    def get_move(self):
        """ Evaluates the confidence for all output nodes in network, then proceeds in the
            direction of highest confidence.
        """
        if self.agent.game is None:
            raise ValueError("The agent's Game attribute has not been set. Cannot get move.")

        # Clear stored values of agent nodes
        self.agent.clear_all_nodes()

        # Update the set of input nodes to represent the board state
        for node in self.agent.input_nodes:
            pos = self.node_number_to_board_position(node.number)
            node.val = TILE_TYPE_TO_WEIGHT[str(self.agent.game.board[pos[0]][pos[1]][0])]

        # Check highest output value and move in that direction
        max_value = None
        max_value_node = None
        for node in self.agent.output_nodes:
            val = node.value()
            # Nodes with higher innovation number are prioritized in case of ties
            if max_value is None or val > max_value or (val == max_value and node.number > max_value_node.number):
                max_value_node = node
                max_value = val

        # Return direction corresponding to node number for highest value. Cannot turn 180 degrees.
        new_direction = INNOVATION_TO_DIRECTION[max_value_node.number]
        if new_direction == OPPOSITE_DIRECTIONS[self.direction]:
            new_direction = self.direction
        self.direction = new_direction
        return self.direction