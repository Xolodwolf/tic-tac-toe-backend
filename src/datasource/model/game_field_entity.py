import json
from typing import List
from sqlalchemy import Column, Integer, Text
from datasource.database import Base


class GameFieldEntity(Base):
    __tablename__ = "game_fields"

    id = Column(Integer, primary_key=True, autoincrement=True)
    board_data = Column(Text, nullable=False)

    def __init__(self, board: List[List[int]]):
        super().__init__()
        self.board = board

    @property
    def board(self) -> List[List[int]]:
        if hasattr(self, "_board"):
            return self._board
        if self.board_data:
            return json.loads(self.board_data)
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    @board.setter
    def board(self, value: List[List[int]]):
        self._board = value
        self.board_data = json.dumps(value)
