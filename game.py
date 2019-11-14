import pygame
import random

import controller

from constants import *

board_dims = (20, 20)
player_count = 1

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
			pygame.event.pump()

			for i in range(len(self.board[0])):
				for j in range(len(self.board)):
					print(self.board[j][i], end=' ')
				print()
			for i in range(len(self.players)-1, -1, -1):
				player = self.players[i]
				self.board[player.x][player.y] = 1
				move = player.move()
				#print(move)
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
		self.controller = controller.KeyboardController()

	def move(self):
		my_move = self.controller.get_move()
		self.x += my_move[0]
		self.y += my_move[1]
		return my_move

	def die(self):
		print('Ouch')


Game()