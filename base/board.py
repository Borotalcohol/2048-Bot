import copy
import random
import globals
import numpy as np

class Board:
    # Initializes the board
    def __init__(self):
        self.board = None
        self.score = 0
        self.reset()

    # Resets to the initial state, only two random tiles
    def reset(self):
        self.board = [[0] * 4 for i in range(4)]

        self.add_tile()
        self.add_tile()

    # Adds the tile if one is given, generate a random one otherwise
    def add_tile(self, position = None, value = 0):
        empty_cells = [(row, col) for row in range(4) for col in range(4) if self.board[row][col] == 0]

        if position is not None and value > 0:
            self.board[position[0]][position[1]] = value
            return

        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4

    # Moves the tiles in the given direction,
    # If apply_change is True, the board edit is applied to the board state and a new random tile is generated,
    # Otherwise a board with the applied move is returned without updating the board state and without generating
    # a new random tile
    def move(self, direction, apply_change=True):
        new_board = self._slide(self.board, direction)
        new_board = self._merge(new_board, direction)
        new_board = self._slide(new_board, direction)

        if not apply_change: return new_board

        if new_board != self.board:
            self.board = new_board
            self.add_tile()

    # Checks whether the current board status is a game over.
    # Simulates a move in every direction, if all the resulting
    # boards are equal to the original one, it's game over.
    def is_game_over(self):
        game_over = True

        for dir in range(4):
            moved_board = self.move(globals.DIRECTIONS_MAP[dir], apply_change=False)
            if moved_board != self.board: return False
        
        return game_over

    # Renders the board state in the Pygame window
    def render(self, pygame, screen):
        TILE_SIZE = 110
        X_OFFSET = 35
        Y_OFFSET = globals.HEIGHT - 5 - globals.SQUARE_SIZE

        pygame.draw.rect(screen, pygame.Color(globals.MAIN_SQUARE_COLOR), pygame.Rect(20, globals.HEIGHT-20-globals.SQUARE_SIZE, globals.SQUARE_SIZE, globals.SQUARE_SIZE))

        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                if tile != 0:
                    pygame.draw.rect(screen, pygame.Color(globals.TILE_COLORS[tile]), pygame.Rect(35 + j * 110, globals.HEIGHT - 5 - globals.SQUARE_SIZE + i * 110, 100, 100))

                    # Calculate font size based on the number of digits
                    font_size = 75 - 10 * (len(str(tile)) - 1)
                    font = pygame.font.Font(None, font_size)
                    text = font.render(str(tile), True, pygame.Color(globals.DARK_TEXT_COLOR if tile < 8 else globals.LIGHT_TEXT_COLOR))

                    # Calculate text_x and text_y based on tile value
                    text_x = X_OFFSET + j * TILE_SIZE + (TILE_SIZE - text.get_width()) / 2
                    text_y = Y_OFFSET + i * TILE_SIZE + (TILE_SIZE - text.get_height()) / 2

                    screen.blit(text, (text_x, text_y))
                else:
                    pygame.draw.rect(screen, pygame.Color(globals.EMPTY_SQUARE_COLOR), pygame.Rect(35 + j * 110, globals.HEIGHT - 5 - globals.SQUARE_SIZE + i * 110, 100, 100))

    # Slides the board in the given direction without adding the tiles
    def _slide(self, board, direction):
        new_board = np.array(copy.deepcopy(board))

        def slide_line(line):
            non_zero_tiles = [tile for tile in line if tile != 0]
            new_line = non_zero_tiles + [0] * (4 - len(non_zero_tiles) if direction in ["up", "left"] else 0)
            new_line = [0] * (4 - len(new_line) if direction in ["down", "right"] else 0) + new_line
            return new_line

        if direction in ["up", "down"]:
            cols = [[new_board[i][j] for i in range(4)] for j in range(4)]
            new_cols = [slide_line(col) for col in cols]
            new_board = [[new_cols[i][j] for i in range(4)] for j in range(4)]
        elif direction in ["left", "right"]:
            new_board = [slide_line(row) for row in new_board]

        return new_board
    
    # Add adjacent tiles with equal values in the given direction
    def _merge(self, board, direction):
        new_board = np.array(copy.deepcopy(board))

        def merge_line(line):
            skip_next = False
            merged_line = [0] * 4

            if direction in ["down", "right"]:
                line = line[::-1]

            for i in range(3):
                if skip_next:
                    skip_next = False
                    continue

                if line[i] == line[i+1]:
                    merged_line[i] = line[i] * 2
                    skip_next = True
                else:
                    merged_line[i] = line[i]

            # Handle the last element
            if not skip_next:
                merged_line[3] = line[3]

            return merged_line if direction in ["up", "left"] else merged_line[::-1]

        if direction in ["up", "down"]:
            cols = [[new_board[i][j] for i in range(4)] for j in range(4)]
            new_cols = [merge_line(col) for col in cols]
            new_board = [[new_cols[i][j] for i in range(4)] for j in range(4)]
        elif direction in ["left", "right"]:
            new_board = [merge_line(row) for row in new_board]

        return new_board