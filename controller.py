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


class AgentController(Controller):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    def get_move(self):
        """ Evaluates the confidence for all output nodes in network, then proceeds in the
            direction of highest confidence.
        """
        max_value = None
        max_value_node = None
        for node in self.agent.output_nodes:
            val = node.value()
            # Nodes with higher innovation number are prioritized in case of ties
            if max_value is None or val > max_value or (val == max_value and node.number > max_value_node.number):
                max_value_node = node
                max_value = val

        # Return direction corresponding to node number for highest value
        return INNOVATION_TO_DIRECTION[max_value_node.number]