from typing import Optional, List, Tuple
from uuid import UUID
from collections import defaultdict
from sqlalchemy.orm import Session
from datasource.model.current_game_entity import CurrentGameEntity
from domain.model.game_state import GameState


class GameRepository:

    def __init__(self, db_session: Session):
        self._session = db_session

    def save_game(self, game: CurrentGameEntity) -> CurrentGameEntity:
        existing_game = (
            self._session.query(CurrentGameEntity)
            .filter_by(game_id=game.game_id)
            .first()
        )

        if existing_game:
            existing_game.game_field = game.game_field
            existing_game.game_type = game.game_type
            existing_game.game_state = game.game_state
            existing_game.player1_id = game.player1_id
            existing_game.player2_id = game.player2_id
            existing_game.player1_symbol = game.player1_symbol
            existing_game.player2_symbol = game.player2_symbol
            existing_game.current_player_id = game.current_player_id
            existing_game.winner_id = game.winner_id
            self._session.merge(existing_game)
            self._session.commit()
            return existing_game
        else:
            self._session.add(game)
            self._session.commit()
            self._session.refresh(game)
            return game

    def get_game(self, game_id: UUID) -> Optional[CurrentGameEntity]:
        return (
            self._session.query(CurrentGameEntity)
            .filter_by(game_id=str(game_id))
            .first()
        )

    def get_available_games(self) -> List[CurrentGameEntity]:
        return (
            self._session.query(CurrentGameEntity)
            .filter(
                CurrentGameEntity.game_state.in_(
                    [GameState.WAITING_FOR_PLAYER.value, GameState.PLAYER_TURN.value]
                )
            )
            .all()
        )

    def delete_game(self, game_id: UUID) -> bool:
        game = self.get_game(game_id)
        if game:
            self._session.delete(game)
            self._session.commit()
            return True
        return False

    def get_completed_games_by_user(self, user_id: UUID) -> List[CurrentGameEntity]:
        return (
            self._session.query(CurrentGameEntity)
            .filter(
                (CurrentGameEntity.player1_id == user_id)
                | (CurrentGameEntity.player2_id == user_id)
            )
            .filter(
                CurrentGameEntity.game_state.in_(
                    [GameState.PLAYER_WON.value, GameState.DRAW.value]
                )
            )
            .order_by(CurrentGameEntity.created_at.desc())
            .all()
        )

    def get_leaderboard(self, limit: int) -> List[Tuple[UUID, float, int, int]]:
        completed_games = (
            self._session.query(CurrentGameEntity)
            .filter(
                CurrentGameEntity.game_state.in_(
                    [GameState.PLAYER_WON.value, GameState.DRAW.value]
                )
            )
            .all()
        )

        user_stats = defaultdict(lambda: {"wins": 0, "total": 0})

        for game in completed_games:
            if game.player1_id:
                user_stats[game.player1_id]["total"] += 1
                if game.winner_id == game.player1_id:
                    user_stats[game.player1_id]["wins"] += 1

            if game.player2_id:
                user_stats[game.player2_id]["total"] += 1
                if game.winner_id == game.player2_id:
                    user_stats[game.player2_id]["wins"] += 1

        results = []
        for user_id, stats in user_stats.items():
            if stats["total"] > 0:
                win_ratio = stats["wins"] / stats["total"]
                results.append((user_id, win_ratio, stats["wins"], stats["total"]))

        results.sort(key=lambda x: (x[1], x[2]), reverse=True)

        return results[:limit]
