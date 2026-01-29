from typing import List, Dict, Any


class GameFieldDTO:
    def __init__(self, board: List[List[int]]):
        self.board = board

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GameFieldDTO":
        return GameFieldDTO(board=data["board"])

    def to_dict(self) -> Dict[str, Any]:
        return {"board": self.board}
