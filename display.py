import time

import pygame

from constants import *
from controller import node_number_to_board_offset

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
        self.node_label_font = pygame.font.SysFont("Arial", 30)
        self.node_surf = pygame.Surface((25, 25))
        pygame.draw.ellipse(self.node_surf, (100, 100, 100), (0, 0, 25, 25))
        self.active_node_surf = pygame.Surface((25, 25))
        pygame.draw.ellipse(self.active_node_surf, (255, 255, 255), (0, 0, 25, 25))
        self.reset(game)

    def reset(self, game):
        self.game = game
        self.node_count = 0
        self.node_innovation_to_position = {}

    def tile_to_color(self, tile):
        hues = [(1, 1, 1), (0.3, 0.6, 1), (1, 0.4, 0.3), (0.4, 0.9, 0.3), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
        vals = {PLAYER_TILE: 200,
                TAIL_TILE: 128,
                EMPTY_TILE: 40}
        hue = hues[tile[1]]
        val = vals[str(tile[0])]
        return tuple([int(h * val) for h in hue])

    def update(self, vis_mode=False):
        dt = self.time_step()

        self.screen.fill((0, 0, 0))

        origin_x = WINDOW_WIDTH//2 - (TILE_SIZE * BOARD_WIDTH)//2
        if vis_mode:
            origin_x -= WINDOW_WIDTH//4
        origin_y = WINDOW_HEIGHT//2 - (TILE_SIZE * BOARD_WIDTH)//2

        if vis_mode:
            active_player = self.game.players[0] if self.game.players else self.game.last_active_player

        x, y = origin_x, origin_y
        for i, column in enumerate(self.game.board):
            for j, item in enumerate(column):
                real_i, real_j = i, j
                if vis_mode:
                    real_i = (i - active_player.x - BOARD_WIDTH//2) % BOARD_WIDTH
                    real_j = (j - active_player.y - BOARD_HEIGHT//2) % BOARD_HEIGHT
                color = self.tile_to_color(item)
                rect = (x + real_i*TILE_SIZE, y + real_j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

        if vis_mode:
            if hasattr(active_player.controller, "agent"):
                agent = active_player.controller.agent
                self.draw_output_nodes(agent)
                self.draw_intermediary_nodes(agent)
                self.draw_edges(agent)

        pygame.display.flip()

    def draw_output_nodes(self, agent):
        best_node = max(list(agent.output_nodes), key=lambda x:x.val)
        names = ["UP", "LEFT", "RIGHT", "DOWN"]
        x = int(WINDOW_WIDTH*0.85)
        y = int(WINDOW_WIDTH*0.28)
        for name in names:
            if name == "UP":
                innovation = DIRECTION_TO_INNOVATION[UP]
            elif name == "DOWN":
                innovation = DIRECTION_TO_INNOVATION[DOWN]
            elif name == "LEFT":
                innovation = DIRECTION_TO_INNOVATION[LEFT]
            elif name == "RIGHT":
                innovation = DIRECTION_TO_INNOVATION[RIGHT]

            label = self.node_label_font.render(name, 1, (255, 255, 255))
            self.screen.blit(label, (x, y))
            self.screen.blit(self.node_surf, (x - 35, y + 5))
            if best_node.number == innovation:
                self.screen.blit(self.active_node_surf, (x - 35, y + 5))
            self.node_innovation_to_position[innovation] = (x - 35, y + 5)
            y += 35

    def draw_intermediary_nodes(self, agent):
        x = WINDOW_WIDTH//2
        y = WINDOW_HEIGHT//4
        xoff = 0
        yoff = 0
        wid = WINDOW_WIDTH//3
        for node in agent.nodes - agent.input_nodes - agent.output_nodes:
            self.screen.blit(self.node_surf, (x + xoff, y + yoff))
            self.node_innovation_to_position[node.number] = (x + xoff, y + yoff)

            yoff += 50
            if yoff > wid:
                yoff = 0
                xoff += 50

    def draw_edges(self, agent):
        for edge in agent.edges:
            pos_1 = self.innovation_to_position(edge.in_node.number)
            if pos_1[0] < WINDOW_WIDTH//2:
                highlight = pygame.Surface((TILE_SIZE, TILE_SIZE))
                highlight.fill((255, 255, 255))
                highlight.set_alpha(25)
                self.screen.blit(highlight, (pos_1[0] - TILE_SIZE//2, pos_1[1] - TILE_SIZE//2))
            pos_2 = self.innovation_to_position(edge.out_node.number)
            color = (0, 255, 0) if edge.weight > 0 else (255, 0, 0)
            if not edge.enabled:
                color = (100, 100, 100)
            width = min(int(abs(edge.weight)) + 1, 5)
            pygame.draw.line(self.screen, color, pos_1, pos_2, width)

    def innovation_to_position(self, inn):
        if inn in self.node_innovation_to_position:
            x, y = self.node_innovation_to_position[inn]
            return x + 12, y + 12
        else:
            x_pos, y_pos = node_number_to_board_offset(inn)
            x_pos = (x_pos + BOARD_WIDTH//2) % BOARD_WIDTH
            y_pos = (y_pos + BOARD_WIDTH//2) % BOARD_WIDTH
            x = x_pos * TILE_SIZE + WINDOW_WIDTH//4 - (TILE_SIZE * BOARD_WIDTH)//2
            y = y_pos * TILE_SIZE + WINDOW_HEIGHT//2 - (TILE_SIZE * BOARD_WIDTH)//2
            return x + TILE_SIZE//2, y + TILE_SIZE//2

