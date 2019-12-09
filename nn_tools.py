import math
import random
import game
import pickle
from constants import *


class Node:

    def __init__(self, innovation, edges_in=None, edges_out=None, activation_func=None):
        self.val = None
        self.number = innovation
        self.edges_in = edges_in if edges_in else []
        self.edges_out = edges_out if edges_out else []
        self.activation_func = self.sigmoid if not activation_func else activation_func

    def get_input_sum(self):
        """ Returns a weighted sum of all incoming edges. """
        _sum = 0
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

        for edge in self.edges_out:
            if not edge.out_node.check_valid_edge(destination_node):
                return False

        return True

    def copy(self):
        """ Copies the node preserving all values """
        return Node(self.number, edges_in=self.edges_in, edges_out=self.edges_out, activation_func=self.activation_func)

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

    def copy(self):
        """ Copies the edge preserving all values """
        return Edge(self.innovation, self.in_node, self.out_node, weight=self.weight, enabled=self.enabled)

    @staticmethod
    def random_weight():
        """ Returns a random weight. """
        return random.random()*NORMAL_DISTRIBUTION - NORMAL_DISTRIBUTION/2


class Agent:

    def __init__(self, population):
        self.pop = population
        self.nodes = set()
        self.input_nodes = set()
        self.output_nodes = set()
        self.edges = set()
        self.innovations = set()
        self.node_numbers = set()
        self.fitness = 0
        self.game = None  # Reference to in-progress game object for testing fitness

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

        for _ in range(output_size):
            self.output_nodes.add(Node(innovation=self.pop.new_node_number()))

        for _ in range(input_size):
            self.input_nodes.add(Node(innovation=self.pop.new_node_number()))

        self.nodes |= self.input_nodes
        self.nodes |= self.output_nodes

    def break_edge(self, edge):
        """ Creates a new node where an edge used to be, with two new edges connecting it to the previous edge's
            endpoints. Disables the previous edge.
        """

        in_node = edge.in_node
        out_node = edge.out_node
        self.node_numbers.add(self.pop.node_count)
        new_node = Node(innovation=self.pop.new_node_number())
        self.innovations.add(self.pop.innovation_count)
        self.edges.add(Edge(self.pop.new_innovation_number(), in_node, new_node))
        self.innovations.add(self.pop.innovation_count)
        self.edges.add(Edge(self.pop.new_innovation_number(), new_node, out_node))
        self.nodes.add(new_node)
        edge.disable()

    def clear_all_nodes(self):
        """ Resets the stored values of all nodes in the Agent --- must do between testing outputs. """
        for node in self.nodes:
            node.clear()

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

        self.innovations.add(self.pop.innovation_count)
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

        self.mutate_edges()

    def mutate_edges(self):
        """ Has a chance of applying a perturbation to each edge. """
        for edge in self.edges:
            if random.random() < EDGE_MUTATION_PROB:
                edge.weight += random.gauss(0, EDGE_MUTATION_STD_DEV)

    def test_fitness(self):
        """ Runs a simulation for the Agent and returns a fitness. """
        g = game.Game()
        g.add_players(False, self)
        self.fitness = g.main()
        self.game = None  # Reset this value, set in Game
        return self.fitness

    def copy(self):
        """ Copy agent preserving all values """
        new_agent = Agent(self.pop)

        new_agent.innovations = self.innovations
        new_agent.node_numbers = self.node_numbers

        for edge in self.edges:
            new_agent.edges.add(edge.copy())

        for node in self.nodes:
            new_node = node.copy()

            for edge in new_agent.edges:
                if edge.in_node == node:
                    edge.in_node = new_node

                if edge.out_node == node:
                    edge.out_node = new_node

            new_agent.nodes.add(new_node)

            if node in self.input_nodes:
                new_agent.input_nodes.add(new_node)
            if node in self.output_nodes:
                new_agent.output_nodes.add(new_node)

        return new_agent

    def get_edge_by_innov(self, innov: int) -> Edge:
        """ Return an Edge object with the given innovation number
        """
        for edge in self.edges:
            if edge.innovation == innov:
                return edge
    # TODO make reasonable way to initialize and give input states
    # TODO add reproduction


class Population:

    def __init__(self):
        self.agents = []
        self.innovation_count = 0
        self.node_count = 0
        self.generation = 0

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
        new_agent = Agent(self)
        new_agent.create_empty(10, 4)
        # TODO Copy first agent and mutate for initial population
        self.agents.append(new_agent)

    def save_population(self):
        """ Create pickle file of entire population
        """
        filename = "population_gen" + str(self.generation) + ".pkl"
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def load_population(self, generation):
        """ Loads a population from a pickled population object
        """
        filename = "population_gen" + str(generation) + ".pkl"
        with open(filename, 'rb') as file:
            loaded_pop = pickle.load(file)
            self.agents = loaded_pop.agents
            self.innovation_count = loaded_pop.innovation_count
            self.node_count = loaded_pop.node_count
            self.generation = loaded_pop.generation

    @staticmethod
    def reproduction(agent_1, agent_2):
        """ Combine agent to create a new one """
        new_agent = (agent_1.copy() if agent_1.fitness > agent_2.fitness else agent_2.copy())

        for edge in agent_2.edges:
            if not edge.innovation in new_agent.innovations:
                new_agent.edges.add(edge)

                if not edge.in_node.number in new_agent.node_numbers:
                    new_node = edge.in_node.copy()
                    for new_edge in new_node.edges_in:
                        new_edge.out_node = new_node

                    for new_edge in new_node.edges_out:
                        new_edge.in_node = new_node

                    new_agent.nodes.add(new_node)

        return new_agent

    @staticmethod
    def get_difference(agent_1: Agent, agent_2: Agent) -> int:
        """ Measures genetic distance between two agents
        """
        innov_1 = agent_1.innovations
        innov_2 = agent_2.innovations

        excess_count = innov_1 - innov_2
        disjoint_count = innov_2 - innov_1
        common = innov_1.intersection(innov_2)
        total_w_diff = 0
        for innov in common:
            e_1 = agent_1.get_edge_by_innov(innov)
            e_2 = agent_2.get_edge_by_innov(innov)
            total_w_diff += abs(e_1.weight - e_2.weight)
        ave_w_diff = total_w_diff / len(common)
        n = max(len(innov_1), len(innov_2))
        dist = WEIGHT_DIFFERENCE_COEFF * ave_w_diff + DISJOINT_DIFFERENCE_COEFF * (disjoint_count / n) \
               + EXCESS_DIFFERENCE_COEFF * (excess_count / n)
        return dist

    # TODO add population simulation
    # TODO program ability to add nodes
