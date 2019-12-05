from constants import *
import math
import random


class Node:

    def __init__(self, innovation, bias=None, edges_in=None, edges_out=None, activation_func=None):
        self.val = None
        self.number = innovation
        self.bias = bias if bias else self.random_bias()
        self.edges_in = edges_in if edges_in else []
        self.edges_out = edges_out if edges_out else []
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

    def __repr__(self):
        return f"\nNode (I={self.number}, " \
               f"in={sorted([item.in_node.number for item in self.edges_in])}, " \
               f"out={sorted([item.out_node.number for item in self.edges_out])}"

    def check_valid_edge(self, destination_node):
        """ Checks to see if new edge is legal """
        if destination_node == self:
            return False

        for edge in edges_out:
            if not edge.out_node.check_valid_edge(destination_node):
                return False

        return True

    @staticmethod
    def random_bias():
        """ Returns a random value for a bias term. """
        return random.gauss(0, 1)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))


class Edge:

    def __init__(self, innovation, in_node, out_node, weight=None, enabled=True):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight if weight else self.random_weight()
        self.enabled = enabled
        self.innovation = innovation

        in_node.edges_out.append(self)
        out_node.edges_in.append(self)

    def get_output_value(self):
        """ Returns the output value based on weight, input node,
            and enabled bit.
        """
        if self.enabled:
            return self.in_node.value() * self.weight
        else:
            return 0

    def disable(self):
        """ Disables the edge. """
        self.enabled = False

    @staticmethod
    def random_weight():
        """ Returns a random weight. """
        return random.gauss(0, 1)


class Agent:

    def __init__(self, population):
        self.pop = population
        self.nodes = set()
        self.input_nodes = set()
        self.output_nodes = set()
        self.edges = set()

    def create_fully_connected(self, *args):
        """ Creates a fully connected neural network, with the input values being the number of nodes in each layer.

            For instance, create_fully_connected(3, 4, 10) creates a model with three input nodes, four intermediary
            nodes, and ten output nodes.
        """
        self.nodes = set()
        self.edges = set()
        self.input_nodes = set()

        previous_layer = None
        for layer in args:
            new_nodes = set(Node(innovation=self.pop.new_node_number()) for _ in range(layer))

            # Connect edges from previous layer to new layer
            if previous_layer is not None:
                for node_1 in previous_layer:
                    for node_2 in new_nodes:
                        self.edges.add(Edge(self.pop.new_innovation_number(), node_1, node_2))

            # The first layer is the input nodes
            else:
                self.input_nodes = new_nodes

            previous_layer = new_nodes
            self.nodes |= new_nodes

        # The last layer is output nodes
        self.output_nodes = previous_layer

    def create_empty(self, input_size, output_size):
        """ Creates an unconnected, two-layer graph with the correct number of input and output nodes. """
        self.nodes = set()
        self.edges = set()
        self.input_nodes = set()

        for _ in range(input_size):
            self.input_nodes.add(Node(innovation=self.pop.new_node_number()))

        for _ in range(output_size):
            self.output_nodes.add(Node(innovation=self.pop.new_node_number()))

        self.nodes |= self.input_nodes
        self.nodes |= self.output_nodes

    def break_edge(self, edge):
        """ Creates a new node where an edge used to be, with two new edges connecting it to the previous edge's
            endpoints. Disables the previous edge.
        """

        in_node = edge.in_node
        out_node = edge.out_node
        new_node = Node(innovation=self.pop.new_node_number())
        self.edges.add(Edge(self.pop.new_innovation_number(), in_node, new_node))
        self.edges.add(Edge(self.pop.new_innovation_number(), new_node, out_node))
        self.nodes.add(new_node)
        edge.disable()

    def add_random_edge(self, max_iterations=10):
        """ Adds an edge between two random unconnected nodes, and returns True on success.
            If this fails to create a valid edge max_iterations consecutive times, it fails and returns False.
        """

        iterations = 0
        in_node = random.choice(self.nodes - self.output_nodes)
        already_connected = {edge.out_node for edge in in_node.edges_out}
        out_node = random.choice(self.nodes - self.input_nodes - already_connected - {in_node})
        while not in_node.check_valid_edge(out_node):
            out_node = random.choice(self.nodes - self.input_nodes - {in_node})
            iterations += 1
            if iterations >= max_iterations:
                return False

        self.edges.add(Edge(innovation=self.pop.new_innovation_number(),
                            in_node=in_node,
                            out_node=out_node))
        return True

    def mutate(self):
        """ Applies a random mutation to the active agent, based on values in constants.py """
        if random.random() < NEW_EDGE_MUTATION_PROB:
            self.add_random_edge()
        else:
            edge_to_break = random.choice(self.edges)
            self.break_edge(edge_to_break)
        # TODO add ability to mutate weights of edges

    # TODO make reasonable way to initialize and give input states
    # TODO add reproduction


class Population:

    def __init__(self):
        self.agents = []
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

    def instantiate_population(self):
        """ Create initial population and populate with empty agents """
        while len(self.agents) < POPULATION_SIZE:
            self.agents.append(Agent(self))

    # TODO add population simulation
    # TODO program ability to add nodes
