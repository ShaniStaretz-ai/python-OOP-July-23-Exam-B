from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps
from random import shuffle as py_shuffle


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
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

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
        return f"'{self.get_display_name()}'"

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


class DeckCheatingError(Exception):
    """Raised when a card appears more than once in the deck"""
    pass


class IDeck(ABC):
    @property
    @abstractmethod
    def cards(self): pass

    @abstractmethod
    def shuffle(self): pass

    @abstractmethod
    def draw(self): pass

    @abstractmethod
    def add_card(self, card): pass


# ========== Decorator ==========
def fair_deck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cards=args[0]
        new_card=args[1]
        if isinstance(cards, Deck):
           if new_card in cards:
                    raise DeckCheatingError(f"Duplicate card found: {new_card}")
        result = func(*args, **kwargs)
        return result

    return wrapper


class Deck(IDeck):
    def __init__(self, shuffle=True):
        self._cards = [Card(suit, rank) for suit in CardSuit for rank in CardRank]
        if shuffle:
            self.shuffle()

    @property
    def cards(self):
        return list(self._cards)

    @fair_deck
    def add_card(self, _card):
        # if card in self._cards:
        #     raise DeckCheatingError("Card already exists in the deck!")
        self._cards.append(_card)

    def draw(self):
        """ if cards exist, get and remove the card in the index 0"""
        return self._cards.pop(0) if self._cards else None

    def shuffle(self):
        py_shuffle(self._cards)

    def __len__(self):
        return len(self._cards)

    def __str__(self):
        return ', '.join(str(card) for card in self._cards)

    def __repr__(self):
        return f"Deck({self._cards})"

    def __getitem__(self, index):
        """ get the card in given index """
        return self._cards[index]

    def __max__(self):
        return max(self._cards)

    def __min__(self):
        return min(self._cards)


# ========== Utility Functions ==========
def max_card(*cards):
    return max(cards)


def cards_stats(*cards, **kwargs):
    results = {}
    if 'max' in kwargs:
        count = kwargs['max']
        results['max'] = sorted(cards, reverse=True)[:count]
    if 'min' in kwargs:
        count = kwargs['min']
        results['min'] = sorted(cards)[:count]
    if 'len' in kwargs:
        results['len'] = len(cards)
    return results


if __name__ == '__main__':
    print("Basic Card actions:")
    print("Creating 3 cards example...")
    card1 = Card(CardSuit.SPADES, CardRank.ACE)
    card11 = Card(CardSuit.SPADES, CardRank.ACE)
    card2 = Card(CardSuit.HEARTS, CardRank.ACE)
    print(f"card1:{card1.get_display_name()}")
    print(f" card2:{card2.get_display_name()}")
    print(f"card11:{card11.get_display_name()}")
    print(f"card1 < card2?{card1 < card2}")  # 14-spades(4)<14-heart(1)=False
    print(f"card1 > card2?{card1 > card2}")
    print(f"card1 == card11?{card1 == card11}")

    print("Creating a new deck...")
    deck = Deck()
    print(f"Deck has {len(deck)} cards.")

    print("Drawing 3 cards to separate desk:")
    drawn = [deck.draw() for _ in range(3)]
    for card_d in drawn:
        print(card_d)
    print(f"After draw, Deck has {len(deck)} cards.")
    print("Adding a card back to the deck...")
    deck.add_card(drawn[0])
    print(f"After add card, Deck has {len(deck)} cards.")
    print("Accessing cards directly by index:")
    for i in range(5):
        print(f"Card at index {i}: {deck[i]}")

    print("running statistic global cards functions:")
    print("\nUsing max_card:")
    print("Max:", max_card(*drawn))

    print("\nUsing cards_stats:")
    print(cards_stats(*deck.cards, max=2, min=1, len=1))

    # print("\nTesting fair_deck decorator:")


    # @fair_deck
    # def create_fair_deck():
    #     return Deck()


    # fair_deck_instance = create_fair_deck()
    # print("Deck created successfully.")
