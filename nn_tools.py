import math


class Node:

    def __init__(self, innovation, bias, edges_in=[], edges_out=[], activation_func=None):
        self.val = None
        self.number = innovation
        self.bias = bias
        self.edges_in = edges_in
        self.edges_out = edges_out
        self.activation_func = self.sigmoid if not activation_func else activation_func

    def get_input_sum(self):
        """ Returns a weighted sum of all incoming edges. """
        _sum = self.bias
        for edge in self.edges_in:
            _sum += edge.get_output_value()

        return _sum

    def value(self):
        """ Returns the current value, if it is defined. Otherwise,
            calls the get_value function.
        """
        if self.val is None:
            self.val = self.activation_func(self.get_input_sum())
        return self.val

    def clear(self):
        """ Resets the stored value. """
        self.val = None

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))


class Edge:

    def __init__(self, in_node, out_node, weight, enabled, innovation):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation

    def get_output_value(self):
        """ Returns the output value based on weight, input node,
            and enabled bit.
        """
        if self.enabled:
            return self.in_node.value() * self.weight
        else:
            return 0


class Agent:

    def __init__(self, population):
        self.pop = population
        self.nodes = set()
        self.input_nodes = set()
        self.edges = set()

    # TODO write methods for adding nodes and edges
    # TODO make reasonable way to initialize and give input states
    # TODO add mutation
    # TODO add reproduction


class Population:

    def __init__(self):
        self.innovation_count = 0
        self.node_count = 0

    def new_innovation_number(self):
        """ Increments the innovation counter, then returns the previous value.

            This should be called every time a gene is created and assigned an innovation number
            to avoid collisions.
        """
        result = self.innovation_count
        self.innovation_count += 1
        return result

    def new_node_number(self):
        """ Increments the node counter, then returns the previous value.

            This should be called every time a node is created and assigned an innovation number
            to avoid collisions.
        """
        result = self.node_count
        self.node_count += 1
        return result

    # TODO add population simulation
    # TODO program ability to add nodes






