from typing import List


class GameField:

    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2

    def __init__(self, board: List[List[int]] = None):
        self.board = board if board else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
