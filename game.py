import pygame
import random

board_dims = (20, 20)
player_count = 1

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Game(object):
	def __init__(self):
		pygame.init()
		self.board = [[0 for i in range(board_dims[1]-2)] for j in range(board_dims[0]-2)]

		self.players = []
		for i in range(player_count):
			self.players.append(Player(round(board_dims[0]/2), round(board_dims[1]/2), self))

		self.main()


	def main(self):
		while self.players:
			for i in range(len(self.board[0])):
				for j in range(len(self.board)):
					print(self.board[j][i], end=' ')
				print()
			for i in range(len(self.players)-1, -1, -1):
				player = self.players[i]
				self.board[player.x][player.y] = 1
				print(player.move())
				if (self.board[player.x][player.y] == 0):
					self.board[player.x][player.y] = 2
				else:
					player.die()
					del self.players[i]



class Player(object):
	def __init__(self, x, y, game):
		self.x = x
		self.y = y
		self.game = game
		self.game.board[x][y] = 2

	def move(self):
		my_move = random.choice([UP, DOWN, LEFT, RIGHT])
		self.x += my_move[0]
		self.y += my_move[1]
		return my_move

	def die(self):
		print('Ouch')


Game()