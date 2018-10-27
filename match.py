from dataclasses import dataclass
from enum import Enum

from player import Player


class Winner(Enum):
    PLAYER1 = 1
    PLAYER2 = 2
    TIE = 0
    BYE_OR_DQ = -1


@dataclass
class Match:
    player1: Player
    player2: Player
    round: int
    winner: Winner

    def serialize(self):
        return {
            'player1': self.player1.name,
            'deck1': self.player1.deck,
            'player2': self.player2.name,
            'deck2': self.player2.deck,
            'winner': self.winner.value
        }