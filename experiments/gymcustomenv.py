import random
import pygame
import math
import numpy as np
import gymnasium as gym
from gymnasium import spaces

background_color = "#FAF8EF"
main_square_border_color = "#BBADA0"
empty_square_color = "#CDC0B4"

dark_text_color = "#776E65"
light_text_color = "#F9F6F2"

tile_colors = {
    2: "#EEE4DA",
    4: "#EDE0C8",
    8: "#F2B179",
    16: "#F59563",
    32: "#F67C5F",
    64: "#F65E3B",
    128: "#EDCF72",
    256: "#EDCC61",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",
    4096: "#3E3933",
    8192: "#3E3933",
    16384: "#3E3933",
    32768: "#3E3933",
    65536: "#3E3933"
}

HEURISTICS = [[2**16,2**15,2**14,2**13],
              [2**9, 2**10,2**11,2**12],
              [2**8, 2**7, 2**6, 2**5],
              [2,   2**2, 2**3, 2**4]]

def generate_random_tile(board):
    x = random.randint(0, 3)
    y = random.randint(0, 3)

    while board[x][y] != 0:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
    
    num = 2 if random.random() < 0.9 else 4
    board[x][y] = num

    return board

def slide(board, action):
    cols = [[board[i][j] for i in range(4)] for j in range(4)]

    new_cols = []
    new_rows = []

    new_board = []

    if action == 0:
        for col in cols:
            non_zero_tiles = [tile for tile in col if tile != 0]
            new_col = non_zero_tiles + [0] * (4 - len(non_zero_tiles))
            new_cols.append(new_col)

        new_board = [[new_cols[i][j] for i in range(4)] for j in range(4)]
    
    elif action == 1:
        for col in cols:
            non_zero_tiles = [tile for tile in col if tile != 0]
            new_col = [0] * (4 - len(non_zero_tiles)) + non_zero_tiles
            new_cols.append(new_col)

        new_board = [[new_cols[i][j] for i in range(4)] for j in range(4)]

    elif action == 2:
        for row in board:
            non_zero_tiles = [tile for tile in row if tile != 0]
            new_row = non_zero_tiles + [0] * (4 - len(non_zero_tiles))
            new_rows.append(new_row)

        new_board = new_rows

    elif action == 3:
        for row in board:
            non_zero_tiles = [tile for tile in row if tile != 0]
            new_row = [0] * (4 - len(non_zero_tiles)) + non_zero_tiles
            new_rows.append(new_row)

        new_board = new_rows
    
    return new_board

def compress(board, action):
    new_board = [[board[j][i] for i in range(4)] for j in range(4)]
    score_increment = 0

    if action == 0:
        for i in range(4):
            for j in range(3):
                if new_board[j][i] == new_board[j+1][i]:
                    new_board[j][i] *= 2
                    score_increment += new_board[j][i]
                    new_board[j+1][i] = 0

    elif action == 1:
        for i in range(4):
            for j in range(3, 0, -1):
                if new_board[j][i] == new_board[j-1][i]:
                    new_board[j][i] *= 2
                    score_increment += new_board[j][i]
                    new_board[j-1][i] = 0

    elif action == 2:
        for i in range(4):
            for j in range(3):
                if new_board[i][j] == new_board[i][j+1]:
                    new_board[i][j] *= 2
                    score_increment += new_board[i][j]
                    new_board[i][j+1] = 0

    elif action == 3:
        for i in range(4):
            for j in range(3, 0, -1):
                if new_board[i][j] == new_board[i][j-1]:
                    new_board[i][j] *= 2
                    score_increment += new_board[i][j]
                    new_board[i][j-1] = 0

    return score_increment, new_board

def move(board, action):
    new_board = [[board[j][i] for i in range(4)] for j in range(4)]

    new_board = slide(new_board, action)
    score_increment, new_board = compress(new_board, action)
    new_board = slide(new_board, action)

    if board != new_board:
        new_board = generate_random_tile(new_board)
    
    return score_increment, new_board

def draw_state(pygame, screen, state, height, square_size):
    pygame.draw.rect(screen, pygame.Color(main_square_border_color), pygame.Rect(20, height-20-square_size, square_size, square_size))

    for i, row in enumerate(state):
        for j, tile in enumerate(row):
            if tile != 0:
                pygame.draw.rect(screen, pygame.Color(tile_colors[tile]), pygame.Rect(35 + j * 110, height - 5 - square_size + i * 110, 100, 100))

                font = pygame.font.Font(None, 75)
                text = font.render(str(tile), True, pygame.Color(dark_text_color if tile < 8 else light_text_color))

                text_x = 35 + j * 110 + 35
                text_y = height - 5 - square_size + i * 110 + 30

                screen.blit(text, (text_x, text_y))
            else:
                pygame.draw.rect(screen, pygame.Color(empty_square_color), pygame.Rect(35 + j * 110, height - 5 - square_size + i * 110, 100, 100))

class Env2048(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None):
        self.score = 0
        self.window_size = 512
        self.square_size = self.window_size - 40
        self.render_mode = render_mode

        self.observation_space = spaces.Box(0, 2048, shape=(4, 4), dtype=int)
        self.action_space = spaces.Discrete(4)

        if render_mode == None: return

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()

    def reset(self):
        self.score = 0
        board = [[0] * 4 for _ in range(4)]

        board = generate_random_tile(board)
        board = generate_random_tile(board)

        self.state = board
        return self.state
    
    def step(self, action):
        score_increment, next_state = move(self.state, action)
        self.score += score_increment

        self.state = next_state
        won = any(2048 in row for row in next_state)
        lose = all(0 not in row for row in next_state)

        goodness_score = 0
        for i in range(4):
            for j in range(4):
                goodness_score += self.state[j][i] * math.log(HEURISTICS[j][i])

        reward = -100.0 if lose else goodness_score

        if won: print("Won!")

        done = won or lose

        if done:
            print("Highest tile: ", np.max(self.state))

        return next_state, reward, done, done, {"score": self.score}

    def render(self):
        if self.render_mode == None: return

        self.screen.fill(pygame.Color(background_color))
        draw_state(pygame, self.screen, self.state, self.window_size, self.square_size)
        pygame.display.update()
