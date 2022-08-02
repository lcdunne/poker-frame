from enum import Enum

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
        # For example, Rank.get('T') -> 10 ... Rank.get('K') -> 13
        return Rank[RankName(label).name]
    
    @property
    def label(self):
        # For example, Rank.ACE.label -> 'A'
        return RankName[self.name].value

class Suit(Enum):
    CLUBS = 'c'
    DIAMONDS = 'd'
    HEARTS = 'h'
    SPADES = 's'

class Card:
    def __init__(self, label: str = None, rank: Rank = None, suit: Suit = None):
        # Passing in label means that arguments for rank and suit will be ignored.
        # e.g.: Card('Jd', rank=4, suit='CLUBS') -> Card('Jd')
        if label is not None:
            # Label takes precedence e.g. Card('Td')
            self._rank, self._suit = self.parse_label(label)
            self._label = label.capitalize() # By this point label will be valid if parse_label worked
        elif all([rank, suit]):
            # Construct the label from rank and suit directly
            self._label = Rank(rank).label + Suit[suit.upper()].value
            self._rank, self._suit = self.parse_label(self.label)
        else:
            raise ValueError("Expected either `label`, or both of `rank` and `suit`.")

    @classmethod
    def parse_label(cls, label):
        # Parses a label into a valid hand rank and suit
        # Get the rank & suit from the label
        return Rank.get(label[0].upper()).value, Suit(label[1].lower()).name
    
    def __repr__(self):
        return f"<Card('{self.label}')>"
    
    def __str__(self):
        return f"{Rank(self.rank).name.capitalize()} of {self.suit.capitalize()}"
    
    def __lt__(self, other):
        if isinstance(other, Card):
            return self.rank < other.rank
        return self.rank < other
    
    def __le__(self, other):
        if isinstance(other, Card):
            self.rank <= other.rank
        return self.rank <= other
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank
        return self.rank == other
    
    def __ge__(self, other):
        if isinstance(other, Card):
            return self.rank >= other.rank
        return self.rank >= other
    
    def __gt__(self, other):
        if isinstance(other, Card):
            return self.rank > other.rank
        return self.rank > other
    
    @property
    def rank(self):
        return self._rank
    
    @property
    def suit(self):
        return self._suit
    
    @property
    def label(self):
        return self._label

td = Card('td')
qh = Card(rank=12, suit=Suit.HEARTS.name)
ad = Card('Ad')

ad > qh > td > 9
