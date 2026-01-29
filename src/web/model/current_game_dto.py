from typing import Dict, Any
from uuid import UUID
from web.model.game_field_dto import GameFieldDTO


class CurrentGameDTO:
    def __init__(self, game_id: UUID, game_field: GameFieldDTO):
        self.game_id = game_id
        self.game_field = game_field

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CurrentGameDTO":
        game_id = UUID(data["game_id"])
        game_field = GameFieldDTO.from_dict(data["game_field"])
        return CurrentGameDTO(game_id=game_id, game_field=game_field)

    def to_dict(self) -> Dict[str, Any]:
        return {"game_id": str(self.game_id), "game_field": self.game_field.to_dict()}
