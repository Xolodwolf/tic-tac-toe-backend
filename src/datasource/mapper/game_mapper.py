from uuid import UUID
from domain.model.game_field import GameField
from domain.model.current_game import CurrentGame
from domain.model.game_state import GameState
from domain.model.game_type import GameType
from domain.model.player_symbol import PlayerSymbol
from datasource.model.game_field_entity import GameFieldEntity
from datasource.model.current_game_entity import CurrentGameEntity


class GameMapper:
    @staticmethod
    def to_domain(entity: CurrentGameEntity) -> CurrentGame:
        game_field = GameField(board=entity.game_field.board)
        game_id = (
            UUID(entity.game_id) if isinstance(entity.game_id, str) else entity.game_id
        )

        return CurrentGame(
            game_id=game_id,
            game_field=game_field,
            game_type=GameType(entity.game_type),
            game_state=GameState(entity.game_state),
            player1_id=entity.player1_id,
            player2_id=entity.player2_id,
            player1_symbol=PlayerSymbol.from_value(entity.player1_symbol),
            player2_symbol=PlayerSymbol.from_value(entity.player2_symbol),
            current_player_id=entity.current_player_id,
            winner_id=entity.winner_id,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_entity(domain: CurrentGame) -> CurrentGameEntity:
        game_field_entity = GameFieldEntity(board=domain.game_field.board)

        entity = CurrentGameEntity()
        entity.game_id = str(domain.game_id)
        entity.game_field = game_field_entity
        entity.game_type = domain.game_type.value
        entity.game_state = domain.game_state.value
        entity.player1_id = domain.player1_id
        entity.player2_id = domain.player2_id
        entity.player1_symbol = domain.player1_symbol.value
        entity.player2_symbol = domain.player2_symbol.value
        entity.current_player_id = domain.current_player_id
        entity.winner_id = domain.winner_id
        entity.created_at = domain.created_at

        return entity
