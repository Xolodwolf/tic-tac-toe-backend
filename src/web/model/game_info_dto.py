from dataclasses import dataclass
from typing import Optional, List


@dataclass
class GameInfoDto:
    game_id: str
    board: List[List[int]]
    game_type: str
    game_state: str
    player1_id: str
    player2_id: Optional[str]
    player1_symbol: int
    player2_symbol: int
    current_player_id: Optional[str]
    winner_id: Optional[str]
