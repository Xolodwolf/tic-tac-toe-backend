from uuid import UUID
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
from .game_field import GameField
from .game_state import GameState
from .game_type import GameType
from .player_symbol import PlayerSymbol


@dataclass
class CurrentGame:
    game_id: UUID
    game_field: GameField
    game_type: GameType
    game_state: GameState
    player1_id: UUID
    player2_id: Optional[UUID]
    player1_symbol: PlayerSymbol
    player2_symbol: PlayerSymbol
    current_player_id: Optional[UUID]
    winner_id: Optional[UUID] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_player_turn(self, player_id: UUID) -> bool:
        return (
            self.game_state == GameState.PLAYER_TURN
            and self.current_player_id == player_id
        )

    def is_game_over(self) -> bool:
        return self.game_state in [GameState.DRAW, GameState.PLAYER_WON]

    def get_opponent_id(self, player_id: UUID) -> Optional[UUID]:
        if player_id == self.player1_id:
            return self.player2_id
        elif player_id == self.player2_id:
            return self.player1_id
        return None

    def get_player_symbol(self, player_id: UUID) -> Optional[PlayerSymbol]:
        if player_id == self.player1_id:
            return self.player1_symbol
        elif player_id == self.player2_id:
            return self.player2_symbol
        return None
