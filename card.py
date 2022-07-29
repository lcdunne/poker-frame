from enum import Enum, auto
from dataclasses import dataclass, field
import random

class ExtendedEnum(Enum):
    @classmethod
    def items(cls):
        return list(map(lambda c: c.name, cls))
    
    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))

class Suit(ExtendedEnum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()

class Rank(ExtendedEnum):
    # This is used because Card class is not really user-facing
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

class RankName(ExtendedEnum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = 'T'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

@dataclass(order=True)
class Card:
    rank: int = field(compare=True)
    suit: str = field(compare=False)
    name: str = field(compare=False, init=False)
    
    def __post_init__(self):
        if self.rank not in Rank.values():
            raise ValueError("Rank must be from range 2 - 14 (inclusive).")
        if self.suit not in Suit.items():
            raise ValueError("Suit must be from Suits (see Suits enum).")
        self._make_cardname()

    def __str__(self):
        return self.name
    
    def _make_cardname(self):
        rankname = RankName.__getattr__(Rank(self.rank).name).value 
        self.name = rankname + self.suit[0].lower()

class Deck:
    def __init__(self, form: str ='standard'):
        # form can be 'standard' or 'kuhn'. If kuhn, only K, Q, and J are used.
        self.form = form
        self._construct_deck() # Creates Deck.cards (to work with) and Deck._cards (for reference)
        if self.form == 'kuhn':
            # Filter out all those not specified according to Kuhn poker
            # Possibly not relevant for Deck class?
            self.cards = self._kuhnify()
    
    def _construct_deck(self):
        self.cards = []
        for suit in Suit.items():
            for rank in Rank.values():
                self.cards.append(Card(rank, suit))
        self._cards = tuple(self.cards)

    def _kuhnify(self, rankrange=None, suit=None):
        if rankrange is None:
            rankrange = range(11, 14)
        if suit is None:
            suit = Suit(3).name
        lambda_ = lambda x: (x.rank in rankrange) and (x.suit == suit)
        return list(filter(lambda_, self.cards))
    
    def fan(self, n=5):
        for card in self.cards[:n]:
            print(card)
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def pop(self):
        return self.cards.pop()

if __name__ == '__main__':        
    deck = Deck()                
    deck.fan()
    
    c1 = Card(2, 'CLUBS')
    c2 = Card(10, 'SPADES')
    print(c1 < c2)