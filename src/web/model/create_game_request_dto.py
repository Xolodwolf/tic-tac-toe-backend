from dataclasses import dataclass


@dataclass
class CreateGameRequestDto:
    game_type: str
