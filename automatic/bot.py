import copy
import globals
from board import Board

HEURISTIC = [[2**16,2**15,2**14,2**13],
              [2**9, 2**10,2**11,2**12],
              [2**8, 2**7, 2**6, 2**5],
              [2,   2**2, 2**3, 2**4]]

DIRECTIONS_MAP = {
    0: "up",
    1: "down",
    2: "left",
    3: "right",
}

class Bot:
    def __init__(self):
        pass

    def get_best_action(self, board, depth, pool=None):
        best_score = float("-inf")
        best_action = None

        goodnesses = []

        for dir in range(4):
            direction = DIRECTIONS_MAP[dir]
            action_board = Board(board.move(direction, apply_change=False))
            if action_board.board == board.board: continue
            goodnesses.append(pool.apply_async(self._compute_goodness, (action_board, depth, dir)))
            #goodnesses.append(self._compute_goodness(action_board, depth, dir))
        
        goodnesses = [goodness.get() for goodness in goodnesses]

        for goodness in goodnesses:
            if goodness["score"] >= best_score:
                best_score = goodness["score"]
                best_action = goodness["action"]

        return best_action

    def _heuristics(self, board):
        score = sum(board.board[i][j] * HEURISTIC[i][j] for i in range(4) for j in range(4))
        return score

    def _compute_goodness(self, board, depth, direction=None):
        if board.is_game_over(): return {"score": float("-inf"), "action": direction}
        elif depth < 0: return {"score": self._heuristics(board), "action": direction}

        score = 0

        if depth != int(depth):
            score = float("-inf")

            for dir in range(4):
                direction = DIRECTIONS_MAP[dir]
                action_board = Board(board.move(direction, apply_change=False))
                if action_board != board:
                    goodness_score = self._compute_goodness(action_board, depth=depth-0.5, direction=direction)["score"]
                    if goodness_score > score: score = goodness_score
        
        elif depth == int(depth):
            score = 0
            indices_list = [(i, j) for i, row in enumerate(board.board) for j, tile in enumerate(row) if tile == 0]

            for r, c in indices_list:
                board2, board4 = copy.deepcopy(board), copy.deepcopy(board)
                board2.board[r][c], board4.board[r][c] = 2, 4

                score += 1.0 / len(indices_list) * 0.9 * self._compute_goodness(board2, depth=depth-0.5, direction=direction)["score"]
                score += 1.0 / len(indices_list) * 0.1 * self._compute_goodness(board4, depth=depth-0.5, direction=direction)["score"]
        
        return {"score": score, "action": direction}

