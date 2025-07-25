
from enum import Enum
from abc import ABC, abstractmethod
class ICard(ABC):
    @property
    @abstractmethod
    def suit(self):
        pass

    @property
    @abstractmethod
    def rank(self):
        pass

    @abstractmethod
    def get_display_name(self):
        pass

class CardSuit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4

    def __str__(self):
        return self.name.capitalize()

class CardRank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE=9
    TEN=10
    JACK=11
    QUEEN=12
    KING=13
    ACE=14


    def __str__(self):
        return self.name.capitalize()

class Card(ICard):
    def __init__(self, suit: CardSuit, rank: CardRank):
        if not isinstance(suit, CardSuit) or not isinstance(rank, CardRank):
            raise ValueError("Invalid suit or rank")
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def get_display_name(self):
        return f"{self.rank} of {self.suit}"

    def __str__(self):
        return self.get_display_name()

    def __repr__(self):
        return f"Card({self.rank.name}, {self.suit.name})"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        if self.rank.value == other.rank.value:
            return self.suit.value < other.suit.value
        return self.rank.value < other.rank.value


    def __gt__(self, other):
        return other < self

if __name__ == '__main__':
    card1 = Card(CardSuit.SPADES, CardRank.ACE)
    card11 = Card(CardSuit.SPADES, CardRank.ACE)
    card2 = Card(CardSuit.HEARTS, CardRank.ACE)
    print(card1.get_display_name())
    print(card2.get_display_name())
    print(card1<card2)#14-spades(4)<14-heart(1)=False
    print(card1 > card2)
    print(card1 == card11)