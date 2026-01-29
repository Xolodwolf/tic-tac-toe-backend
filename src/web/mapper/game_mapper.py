from domain.model.game_field import GameField
from domain.model.current_game import CurrentGame
from web.model.game_field_dto import GameFieldDTO
from web.model.current_game_dto import CurrentGameDTO


class WebGameMapper:
    @staticmethod
    def to_domain(dto: CurrentGameDTO) -> CurrentGame:
        game_field = GameField(board=dto.game_field.board)
        return CurrentGame(game_id=dto.game_id, game_field=game_field)

    @staticmethod
    def to_dto(domain: CurrentGame) -> CurrentGameDTO:
        game_field_dto = GameFieldDTO(board=domain.game_field.board)
        return CurrentGameDTO(game_id=domain.game_id, game_field=game_field_dto)
