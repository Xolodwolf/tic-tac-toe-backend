from enum import Enum


class PlayerSymbol(Enum):
    X = 1
    O = 2

    @classmethod
    def from_value(cls, value: int):
        for symbol in cls:
            if symbol.value == value:
                return symbol
        return None

    def opposite(self):
        return PlayerSymbol.O if self == PlayerSymbol.X else PlayerSymbol.X
