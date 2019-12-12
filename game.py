import pygame
import random
import time
import sys

import controller
import display
import player

from constants import *


class Game:

    board = None
    player_count = 0
    simulate = False
    vis_mode = False
    last_active_player = None
    auto_player = False
    display = None
    render_enable = True
    pickle_best_agent = False

    def __init__(self):
        pygame.init()
        if Game.display is None:
            # Game.display = display.Display(self)
            Game.display = display.WindowDisplay(self)
        else:
            Game.display.reset(self)

        self.generate_board()
        self.players = []
        self.bot_list = []
        self.ui_font = pygame.font.SysFont("arial", 20)

    def add_players(self, human_player=False, bot_list=[]):
        """ Adds a human player if specified, than any number of players controlled by agents.
            args: any number of agent models for controllers.
        """
        spawn_locations = list(SPAWN_LOCATIONS)[::-1]
        if RANDOMIZE_SPAWN_LOCATION:
            random.shuffle(spawn_locations)
        if human_player:
            x, y = spawn_locations.pop()
            self.add_player(x, y)
        for agent in bot_list:
            x, y = spawn_locations.pop()
            self.add_agent_player(x, y, agent)
            agent.game = self
        if Game.auto_player:
            x, y = spawn_locations.pop()
            self.add_player(x, y)

    def generate_board(self):
        """ Generates an array of EMPTY tiles of size BOARD_SIZE with walls along the outside
            and assigns it to self.board.
        """

        self.board = [[(EMPTY_TILE, 0) for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]

        # Add tail tiles around the edges
        for x, column in enumerate(self.board):
            for y, _ in enumerate(column):
                if x == 0 or y == 0 or x == BOARD_WIDTH - 1 or y == BOARD_HEIGHT - 1:
                    self.board[x][y] = (TAIL_TILE, 0)

    def add_player(self, x, y):
        """ Adds a new player at position x, y """
        self.players.append(player.Player(x, y, self, id=len(self.players) + 1))
        self.player_count += 1

    def add_agent_player(self, x, y, agent):
        """ Adds a new player, controlled by a NEAT agent, at position x, y """
        new_player = player.Player(x, y, self, id=len(self.players) + 1)
        new_player.controller = controller.AgentController(agent)
        self.bot_list.append(new_player)
        self.players.append(new_player)
        self.player_count += 1

    def render_settings(self):
        colors  = [(80, 255, 110) if item else (150, 150, 150) for item in [Game.simulate,
                                                                             Game.vis_mode,
                                                                             Game.auto_player,
                                                                             Game.render_enable,
                                                                             True]]
        text = [f"1. ANIMATION {'ON' if Game.simulate else 'OFF'}",
                f"2. VIS MODE {'ON' if Game.vis_mode else 'OFF'}",
                f"3. HUMAN MODE {'ON' if Game.auto_player else 'OFF'}",
                f"4. DISPLAY {'ON' if Game.render_enable else 'OFF'}",
                f"5. SAVE AGENT POPULATION"]
        surfs = [self.ui_font.render(t, 1, colors[i]) for i, t in enumerate(text)]
        x = 10
        y = 10
        for item in surfs:
            self.display.screen.blit(item, (x, y))
            y += 20

    def check_globals(self, events):
        """ Given a list of PyGame events, closes the program if it contains a QUIT event. """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Game.simulate = not Game.simulate
                elif event.key == pygame.K_2:
                    print(f"Vis mode {not Game.vis_mode}")
                    Game.vis_mode = not Game.vis_mode
                elif event.key == pygame.K_3:
                    Game.auto_player = not Game.auto_player
                elif event.key == pygame.K_4:
                    Game.render_enable = not Game.render_enable
                    if not Game.render_enable:
                        text = self.ui_font.render("Press 4 to enable rendering", 1, (255, 255, 255))
                        self.display.screen.fill((0, 0, 0))
                        self.display.screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2,
                                                        WINDOW_HEIGHT//2 - text.get_height()//2))
                        pygame.display.flip()
                elif event.key == pygame.K_5:
                    Game.pickle_best_agent = not Game.pickle_best_agent

    def main(self):
        """ Runs the main loop. """
        start = time.time()
        cps = 8  # Cycles per second to run simulation. Set to None for no limit.
        cycle = 0

        while len(self.players) > 1:

            # Check keyboard inputs and window closing
            events = pygame.event.get()
            self.check_globals(events)

            # Update players
            for player in self.players[::-1]:
                player.update(events)
                if player in self.players:
                    player.move()
                    self.last_active_player = player
                if Game.pickle_best_agent:
                    try:
                        player.controller.agent.pop.pickle_best_agent = Game.pickle_best_agent
                    except AttributeError as a:
                        pass
            if Game.simulate and self.render_enable:
                self.display.update(Game.vis_mode)
                self.render_settings()
                pygame.display.flip()

            # Run at a fixed number of cycles per second
            if Game.simulate:
                while time.time() < start + 1/cps:
                    pass
                start += 1/cps
            else:
                start = time.time()

            cycle += 1

        if Game.render_enable:
            self.display.update(Game.vis_mode)
            self.render_settings()
            pygame.display.flip()

        if len(self.players):
            winner = self.last_active_player if self.last_active_player else self.players[0]
            winner.age += self.count_empty_tiles()//2
        return [bot.age * SURVIVAL_SCORE for bot in self.bot_list]

    def count_empty_tiles(self):
        total = 0
        for row in self.board:
            for item in row:
                if item[0] == EMPTY_TILE:
                    total += 1
        return total


if __name__=="__main__":
    a = Game()
    a.add_players(human_player=True)
    print(a.main())