import pygame
import random
import time
import sys

import controller
import display
import player

from constants import *


class Game:

    board = None
    player_count = 1
    simulate = False
    vis_mode = False
    last_active_player = None

    def __init__(self):
        pygame.init()
        self.display = display.WindowDisplay(self)
        self.generate_board()

        self.players = []

    def add_players(self, human_player=False, *args):
        """ Adds a human player if specified, than any number of players controlled by agents.
            args: any number of agent models for controllers.
        """
        spawn_locations = list(SPAWN_LOCATIONS)[::-1]
        if human_player:
            x, y = spawn_locations.pop()
            self.add_player(x, y)
        else:
            for agent in args:
                x, y = spawn_locations.pop()
                self.add_agent_player(x, y, agent)
                agent.game = self

    def generate_board(self):
        """ Generates an array of EMPTY tiles of size BOARD_SIZE with walls along the outside
            and assigns it to self.board.
        """

        self.board = [[EMPTY_TILE for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]

        # Add tail tiles around the edges
        for x, column in enumerate(self.board):
            for y, _ in enumerate(column):
                if x == 0 or y == 0 or x == BOARD_WIDTH - 1 or y == BOARD_HEIGHT - 1:
                    self.board[x][y] = TAIL_TILE

    def add_player(self, x, y):
        """ Adds a new player at position x, y """
        self.players.append(player.Player(x, y, self))

    def add_agent_player(self, x, y, agent):
        """ Adds a new player, controlled by a NEAT agent, at position x, y """
        new_player = player.Player(x, y, self)
        new_player.controller = controller.AgentController(agent)
        self.players.append(new_player)

    def check_globals(self, events):
        """ Given a list of PyGame events, closes the program if it contains a QUIT event. """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Game.simulate = not Game.simulate
                elif event.key == pygame.K_2:
                    print(f"Vis mode {not Game.vis_mode}")
                    Game.vis_mode = not Game.vis_mode

    def main(self):
        """ Runs the main loop. """
        start = time.time()
        cps = 25  # Cycles per second to run simulation. Set to None for no limit.
        cycle = 0

        while self.players:

            # Check keyboard inputs and window closing
            events = pygame.event.get()
            self.check_globals(events)

            # Update players
            for player in self.players[::-1]:
                player.update(events)
                player.move()
                self.last_active_player = player
            if Game.simulate:
                self.display.update(Game.vis_mode)

            # Run at a fixed number of cycles per second
            if Game.simulate:
                while time.time() < start + 1/cps:
                    pass
                start += 1/cps
            else:
                start = time.time()

            cycle += 1
        self.display.update(Game.vis_mode)
        return cycle * SURVIVAL_SCORE


if __name__=="__main__":
    a = Game()
    a.add_players(human_player=True)
    print(a.main())