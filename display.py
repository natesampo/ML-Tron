import time

import pygame

from constants import *

class Display:

    def __init__(self, game):
        """ Takes in game object on initialization. """
        self.game = game
        self.last_update_time = time.time()

    def time_step(self):
        # Calculate time step since last update
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now
        return dt

    def update(self):
        # Default display object does nothing on update
        pass


class PrintDisplay(Display):
    def update(self):
        for i in range(len(self.game.board[0])):
            for j in range(len(self.game.board)):
                print(str(self.game.board[j][i]), end=' ')
            print()
        print()

class WindowDisplay(Display):
    def __init__(self, game):
        super().__init__(game)
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

    def update(self):
        dt = self.time_step()

        origin_x = WINDOW_WIDTH//2 - (TILE_SIZE * BOARD_WIDTH)//2
        origin_y = WINDOW_HEIGHT//2 - (TILE_SIZE * BOARD_WIDTH)//2

        x, y = origin_x, origin_y
        for column in self.game.board:
            y = origin_y
            for item in column:
                color = COLOR_LOOKUP.get(str(item), WHITE)
                rect = (x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                y += TILE_SIZE
            x += TILE_SIZE

        pygame.display.flip()
