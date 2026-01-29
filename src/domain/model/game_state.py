from enum import Enum


class GameState(Enum):
    WAITING_FOR_PLAYER = "waiting_for_player"
    PLAYER_TURN = "player_turn"
    DRAW = "draw"
    PLAYER_WON = "player_won"
