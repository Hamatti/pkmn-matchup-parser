from dataclasses import dataclass


@dataclass
class Player:
    name: str
    deck: str = ''
    wins: int = 0
    losses: int = 0
    ties: int = 0

    def record(self):
        return f'{self.wins}-{self.losses}-{self.ties}'

    def points(self):
        return self.wins * 3 + self.ties

    def __gt__(self, other):
        return self.points() > other.points()

    def serialize(self):
        return {
            'name': self.name,
            'deck': self.deck,
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties
        }

