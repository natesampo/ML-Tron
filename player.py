import controller
from constants import *

class Player(object):
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.game.board[x][y] = PLAYER_TILE
        self.controller = controller.KeyboardController()

    def update(self, events):
        self.controller.update(events)

    def move(self):
        my_move = self.controller.get_move()
        self.x += my_move[0]
        self.y += my_move[1]
        return my_move

    def die(self):
        print('Ouch')