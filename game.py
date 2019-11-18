import pygame
import random
import time
import sys

import controller

from constants import *

board_dims = (20, 20)
player_count = 1

class Game(object):
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((100, 100))
		self.board = [[EMPTY_TILE for i in range(board_dims[1]-2)] for j in range(board_dims[0]-2)]
		self.board.insert(0, [TAIL_TILE for i in range(board_dims[0]-2)])
		self.board.append([TAIL_TILE for i in range(board_dims[0]-2)])
		for row in self.board:
			row.insert(0, TAIL_TILE)
			row.append(TAIL_TILE)

		self.players = []
		for i in range(player_count):
			self.players.append(Player(round(board_dims[0]/2), round(board_dims[1]/2), self))

		self.main()


	def main(self):
		while self.players:
			events = pygame.event.get()
			self.check_close(events)

			for i in range(len(self.board[0])):
				for j in range(len(self.board)):
					print(self.board[j][i], end=' ')
				print()
			print()
			for i in range(len(self.players)-1, -1, -1):
				player = self.players[i]
				self.board[player.x][player.y] = TAIL_TILE
				move = player.move()
				if (self.board[player.x][player.y] == EMPTY_TILE):
					self.board[player.x][player.y] = PLAYER_TILE
				else:
					player.die()
					del self.players[i]
			time.sleep(0.25)

	def check_close(self, events):
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

class Player(object):
	def __init__(self, x, y, game):
		self.x = x
		self.y = y
		self.game = game
		self.game.board[x][y] = PLAYER_TILE
		self.controller = controller.KeyboardController()

	def move(self):
		my_move = self.controller.get_move()
		self.x += my_move[0]
		self.y += my_move[1]
		return my_move

	def die(self):
		print('Ouch')


Game()