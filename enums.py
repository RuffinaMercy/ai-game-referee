from enum import Enum


class ValidationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"


class RoundWinner(str, Enum):
    USER = "user"
    BOT = "bot"
    DRAW = "draw"
