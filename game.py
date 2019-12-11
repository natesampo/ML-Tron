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
    player_count = 0
    simulate = False
    vis_mode = False
    last_active_player = None
    auto_player = False
    display = None

    def __init__(self):
        pygame.init()
        if Game.display is None:
            Game.display = display.WindowDisplay(self)
        else:
            Game.display.reset(self)

        self.generate_board()
        self.players = []
        self.bot_list = []

    def add_players(self, human_player=False, bot_list=[]):
        """ Adds a human player if specified, than any number of players controlled by agents.
            args: any number of agent models for controllers.
        """
        spawn_locations = list(SPAWN_LOCATIONS)[::-1]
        if RANDOMIZE_SPAWN_LOCATION:
            random.shuffle(spawn_locations)
        if human_player:
            x, y = spawn_locations.pop()
            self.add_player(x, y)
        else:
            for agent in bot_list:
                x, y = spawn_locations.pop()
                self.add_agent_player(x, y, agent)
                agent.game = self
        if Game.auto_player:
            x, y = spawn_locations.pop()
            self.add_player(x, y)

    def generate_board(self):
        """ Generates an array of EMPTY tiles of size BOARD_SIZE with walls along the outside
            and assigns it to self.board.
        """

        self.board = [[(EMPTY_TILE, 0) for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]

        # Add tail tiles around the edges
        for x, column in enumerate(self.board):
            for y, _ in enumerate(column):
                if x == 0 or y == 0 or x == BOARD_WIDTH - 1 or y == BOARD_HEIGHT - 1:
                    self.board[x][y] = (TAIL_TILE, 0)

    def add_player(self, x, y):
        """ Adds a new player at position x, y """
        self.players.append(player.Player(x, y, self, id=len(self.players) + 1))
        self.player_count += 1

    def add_agent_player(self, x, y, agent):
        """ Adds a new player, controlled by a NEAT agent, at position x, y """
        new_player = player.Player(x, y, self, id=len(self.players) + 1)
        new_player.controller = controller.AgentController(agent)
        self.bot_list.append(new_player)
        self.players.append(new_player)
        self.player_count += 1

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
                elif event.key == pygame.K_3:
                    Game.auto_player = not Game.auto_player

    def main(self):
        """ Runs the main loop. """
        start = time.time()
        cps = 12  # Cycles per second to run simulation. Set to None for no limit.
        cycle = 0

        while len(self.players) > 1:

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
        return [((not bot.has_been_hit) * WIN_SCORE + cycle * SURVIVAL_SCORE) for bot in self.bot_list]


if __name__=="__main__":
    a = Game()
    a.add_players(human_player=True)
    print(a.main())