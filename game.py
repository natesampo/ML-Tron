import pygame
import random
import time
import sys

import controller
import display
import player

from constants import *

board_dims = BOARD_SIZE
player_count = 1

class Game(object):
	def __init__(self):
		pygame.init()
		self.display = display.WindowDisplay(self)
		self.board = [[EMPTY_TILE for i in range(board_dims[1]-2)] for j in range(board_dims[0]-2)]
		self.board.insert(0, [TAIL_TILE for i in range(board_dims[0]-2)])
		self.board.append([TAIL_TILE for i in range(board_dims[0]-2)])
		for row in self.board:
			row.insert(0, TAIL_TILE)
			row.append(TAIL_TILE)

		self.players = []
		for i in range(player_count):
			self.players.append(player.Player(round(board_dims[0]/2), round(board_dims[1]/2), self))

		self.main()

	def main(self):
		while self.players:
			events = pygame.event.get()
			self.check_close(events)

			for i in range(len(self.players)-1, -1, -1):
				player = self.players[i]
				player.update(events)
				self.board[player.x][player.y] = TAIL_TILE
				move = player.move()
				if self.board[player.x][player.y] == EMPTY_TILE:
					self.board[player.x][player.y] = PLAYER_TILE
				else:
					player.die()
					del self.players[i]
			self.display.update()
			time.sleep(0.25)

	def check_close(self, events):
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


if __name__=="__main__":
	Game()