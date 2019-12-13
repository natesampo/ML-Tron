import pickle
import sys

import pygame

from constants import PLAY_WINDOW
from game import Game
from nn_tools import Agent, Population, Node, Edge

if __name__=="__main__":
    g = Game()
    filename = "population_gen0.pkl"

    # try:
    with open(filename, 'rb') as file:
        population = pickle.load(file)

    print("Sorting agents by best.")
    agents = population.agents
    for i in range(len(agents)):
        for j in range(1, 5):
            try:
                agents[i].test_fitness([agents[i], agents[(i + j) % len(agents)]])
            except:
                continue

    agents.sort(key=lambda x:x.fitness)
    best = agents[-1]

    Game.simulate = True
    while True:
        g = Game()
        g.players = []
        g.add_players(True, [best])
        g.main()