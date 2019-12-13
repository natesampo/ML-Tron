import controller
from constants import *

class Player(object):
    def __init__(self, x, y, game, id=0):
        self.x = x
        self.y = y
        self.game = game
        self.game.board[x][y] = (self, id)
        self.controller = controller.KeyboardController()
        self.has_been_hit = False
        self.id = id
        self.age = 0

    def __str__(self):
        return PLAYER_TILE

    def update(self, events):
        if self.has_been_hit:
            self.die()
        else:
            self.controller.update(events)

    def move(self):
        """ Moves in a direction determined by the controller. Then, if the new location is occupied, dies. """
        dead_players = set()

        self.game.board[self.x][self.y] = (TAIL_TILE, self.id)

        dead_players = set()

        my_move = self.controller.get_move()
        self.x += my_move[0]
        self.y += my_move[1]

        # Move to new tile if not empty
        collision_tile = self.game.board[self.x][self.y]
        if str(collision_tile[0]) is EMPTY_TILE:
            self.game.board[self.x][self.y] = (self, self.id)
        elif str(collision_tile[0]) is PLAYER_TILE:
            dead_players.add(self)
            dead_players.add(collision_tile[0])
        else:
            dead_players.add(self)

        self.age += 1
        return dead_players

        return dead_players

    def die(self):
        # self.game.board[self.x][self.y] = (TAIL_TILE, self.id)
        self.game.players.remove(self)
