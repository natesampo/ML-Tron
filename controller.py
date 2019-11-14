import pygame

from constants import *

class Controller:
    """ Class for controlling a player. """

    def __init__(self):
        self.direction = UP

    def get_move(self):
        raise NotImplementedError("Cannot call get_move on superclass")


class KeyboardController(Controller):
    """ Class for controlling a player using keyboard inputs. """

    def __init__(self):
        super().__init__()
        self.scheme = {UP: pygame.K_UP,
                       LEFT: pygame.K_LEFT,
                       RIGHT: pygame.K_RIGHT,
                       DOWN: pygame.K_DOWN}

    def get_move(self):
        pressed = pygame.key.get_pressed()
        for direction in DIRECTIONS:
            if pressed[self.scheme[direction]]:
                self.direction = direction
                return direction
        return self.direction

class WASDController(KeyboardController):
    def __init__(self):
        super().__init__()
        self.scheme = {UP: pygame.K_w,
                       LEFT: pygame.K_a,
                       RIGHT: pygame.K_d,
                       DOWN: pygame.K_s}