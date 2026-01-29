from typing import List
from domain.model.current_game import CurrentGame
from web.model.game_info_dto import GameInfoDto
from web.model.available_game_dto import AvailableGameDto
from web.model.game_history_dto import GameHistoryDto


class GameDtoMapper:
    @staticmethod
    def to_game_info_dto(game: CurrentGame) -> GameInfoDto:
        return GameInfoDto(
            game_id=str(game.game_id),
            board=game.game_field.board,
            game_type=game.game_type.value,
            game_state=game.game_state.value,
            player1_id=str(game.player1_id),
            player2_id=str(game.player2_id) if game.player2_id else None,
            player1_symbol=game.player1_symbol.value,
            player2_symbol=game.player2_symbol.value,
            current_player_id=(
                str(game.current_player_id) if game.current_player_id else None
            ),
            winner_id=str(game.winner_id) if game.winner_id else None,
        )

    @staticmethod
    def to_available_game_dto(game: CurrentGame) -> AvailableGameDto:
        return AvailableGameDto(
            game_id=str(game.game_id),
            player1_id=str(game.player1_id),
            player2_id=str(game.player2_id) if game.player2_id else None,
            game_type=game.game_type.value,
        )

    @staticmethod
    def to_available_games_list(games: List[CurrentGame]) -> List[dict]:
        return [
            {
                "game_id": str(game.game_id),
                "player1_id": str(game.player1_id),
                "player2_id": str(game.player2_id) if game.player2_id else None,
                "game_type": game.game_type.value,
            }
            for game in games
        ]

    @staticmethod
    def to_game_history_dto(game: CurrentGame) -> GameHistoryDto:
        return GameHistoryDto(
            game_id=str(game.game_id),
            board=game.game_field.board,
            game_type=game.game_type.value,
            game_state=game.game_state.value,
            player1_id=str(game.player1_id),
            player2_id=str(game.player2_id) if game.player2_id else None,
            player1_symbol=game.player1_symbol.value,
            player2_symbol=game.player2_symbol.value,
            current_player_id=(
                str(game.current_player_id) if game.current_player_id else None
            ),
            winner_id=str(game.winner_id) if game.winner_id else None,
            created_at=game.created_at.isoformat(),
        )

    @staticmethod
    def to_game_history_list(games: List[CurrentGame]) -> List[dict]:
        return [
            {
                "game_id": str(game.game_id),
                "board": game.game_field.board,
                "game_type": game.game_type.value,
                "game_state": game.game_state.value,
                "player1_id": str(game.player1_id),
                "player2_id": str(game.player2_id) if game.player2_id else None,
                "player1_symbol": game.player1_symbol.value,
                "player2_symbol": game.player2_symbol.value,
                "current_player_id": (
                    str(game.current_player_id) if game.current_player_id else None
                ),
                "winner_id": str(game.winner_id) if game.winner_id else None,
                "created_at": game.created_at.isoformat(),
            }
            for game in games
        ]
