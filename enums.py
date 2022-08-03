from enum import Enum
from itertools import product

def get_ranks_and_suits():
    # Returns list of [(2, 'CLUBS'), ... , (14, 'SPADES')]
    return product(Rank.values(), Suit.items())

def get_all_handlabels():
    # Returns list of ['2c', ... , 'As']
    return [Rank(c[0]).label+Suit[c[1]].value for c in get_ranks_and_suits()]

class _ExtendedEnum(Enum):
    @classmethod
    def items(cls):
        return [e.name for e in cls]
    
    @classmethod
    def values(cls):
        return [e.value for e in cls]

class RankName(_ExtendedEnum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN ='7'
    EIGHT = '8'
    NINE = '9'
    TEN = 'T'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

class Rank(_ExtendedEnum):
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
    
    @classmethod
    def get(cls, label):
        # Go from a RankName to a Rank
        # For example, Rank.get('T') -> 10 ... Rank.get('K') -> 13
        return Rank[RankName(label.upper()).name]
    
    @property
    def label(self):
        # For example, Rank.ACE.label -> 'A'
        return RankName[self.name].value

class Suit(_ExtendedEnum):
    CLUBS = 'c'
    DIAMONDS = 'd'
    HEARTS = 'h'
    SPADES = 's'