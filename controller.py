import pygame

from constants import *

class Controller:
    """ Class for controlling a player. """

    def __init__(self):
        self.direction = UP

    def update(self, events):
        pass

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
        self.last_pressed = None

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.scheme.values():
                    self.last_pressed = event.key

    def get_move(self):
        for direction in self.scheme:
            if self.scheme[direction] == self.last_pressed:
                self.direction = direction
                self.last_pressed = None
        return self.direction

class WASDController(KeyboardController):
    def __init__(self):
        super().__init__()
        self.scheme = {UP: pygame.K_w,
                       LEFT: pygame.K_a,
                       RIGHT: pygame.K_d,
                       DOWN: pygame.K_s}