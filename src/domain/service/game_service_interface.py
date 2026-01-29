from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from ..model.current_game import CurrentGame
from ..model.game_type import GameType
from ..model.leader_stats import LeaderStats


class GameServiceInterface(ABC):
    @abstractmethod
    def create_game(self, player_id: UUID, game_type: GameType) -> CurrentGame:
        pass

    @abstractmethod
    def join_game(self, game_id: UUID, player_id: UUID) -> CurrentGame:
        pass

    @abstractmethod
    def make_move(
        self, game_id: UUID, player_id: UUID, board: List[List[int]]
    ) -> CurrentGame:
        pass

    @abstractmethod
    def get_game(self, game_id: UUID) -> Optional[CurrentGame]:
        pass

    @abstractmethod
    def get_available_games(self) -> List[CurrentGame]:
        pass

    @abstractmethod
    def get_completed_games_by_user(self, user_id: UUID) -> List[CurrentGame]:
        pass

    @abstractmethod
    def get_leaderboard(self, limit: int) -> List[LeaderStats]:
        pass
