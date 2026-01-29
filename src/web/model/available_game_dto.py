from dataclasses import dataclass
from typing import Optional


@dataclass
class AvailableGameDto:
    game_id: str
    player1_id: str
    game_type: str
    player2_id: Optional[str] = None
