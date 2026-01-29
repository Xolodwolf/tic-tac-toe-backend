from dataclasses import dataclass


@dataclass
class MakeMoveRequestDto:
    row: int
    col: int
