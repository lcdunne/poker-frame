from enums import Rank, Suit

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
    
    # Note on comparisons ----------- #
    # Comparisons are made based on the ranking because this is important for poker.
    # This has the drawback that searching a deck cannot be carried out with 
    # the `in` operator because there will be mutliple matches.
    # This might be slower, but rank comparisons are more of a requirement than
    # dealing of specific cards (for now).
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

if __name__ == '__main__':
    td = Card('td')
    qh = Card(rank=12, suit=Suit.HEARTS.name)
    ad = Card('Ad')
    
    assert ad > qh > td > 9
