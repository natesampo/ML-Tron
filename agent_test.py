import pickle
import sys

import pygame

from game import Game
from nn_tools import Agent, Population, Node, Edge

if __name__=="__main__":
    g = Game()
    filename = "agent_1576178550.8279371.pk1"

    # try:
    with open(filename, 'rb') as file:
        agent = pickle.load(file)

    Game.simulate = True
    while True:
        g = Game()
        g.players = []
        g.add_players(True, [agent])
        g.main()