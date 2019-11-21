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

    def __init__(self):
        pygame.init()
        self.display = display.WindowDisplay(self)
        self.generate_board()

        self.players = []
        for i in range(self.player_count):
            self.add_player(round(BOARD_WIDTH/2), round(BOARD_HEIGHT/2))

        self.main()

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

    def check_close(self, events):
        """ Given a list of PyGame events, closes the program if it contains a QUIT event. """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def main(self):
        """ Runs the main loop. """
        while self.players:
            events = pygame.event.get()
            self.check_close(events)

            for player in self.players[::-1]:
                player.update(events)
                player.move()
            self.display.update()
            time.sleep(0.1)


if __name__=="__main__":
    Game()