from dataclasses import dataclass
from enum import Enum


class Winner(Enum):
    PLAYER1 = 1
    PLAYER2 = 2
    TIE = 0
    BYE_OR_DQ = -1


@dataclass
class Match:
    player1: str
    player2: str
    round: int
    winner: Winner
