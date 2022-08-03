from enums import Rank, Suit

class Card:
    """A playing card.
    
    Members of the `Card` class can be compared (based on their rank only).
    
    Notes
    ----
    Either a single card label, or both rank and suit, must be provided for 
    construction.
    
    If label is provided and any of rank or suit are also provided, then label 
    will take precedence: Calling `Card('2s', rank=10, suit='DIAMONDS')` will 
    create the two of spades, not the ten of diamonds.
    
    Comparisons are made based on the integer ranking because this is important 
    for poker. This has the drawback that searching a deck (see `Deck._search`, 
    for example) cannot be carried out with the `in` membership operator 
    because there will be mutliple matches. This might be slower, but rank 
    comparisons are more of a requirement than dealing of specific cards (for 
    now).

    Parameters
    ----------
    label : str, optional
        A label, like `As`, or `2c` from which to create the card. The default 
        is None.
    rank : int, optional
        An integer value denoting the rank of the playing card from which to 
        create the card. This value must correspond to one of the rank values 
        defined  in `enums.Rank`, i.e. in the range (2, 14) inclusive. If 
        `rank` is used, `suit` must also be passed in. The default is None.
    suit : str, optional
        A string denoting the suit of the playing card from which to create the 
        card. This value must correspond to one of the suit values defined in 
        `enums.Suit`, i.e. one of `'SPADES'`, `'CLUBS'`, `'DIAMONDS'`, 
        `'HEARTS'`. If `suit` is used, `rank` must also be passed in. The 
        default is None.

    Raises
    ------
    ValueError
        If if label is None and only one or none of `rank` and `suit` are 
        passed.

    """
    def __init__(self, label: str = None, rank: int = None, suit: str = None):
        if label is not None:
            self._rank, self._suit = self.parse_label(label)
            # By this point label will be valid if parse_label worked
            self._label = label.capitalize()
        elif all([rank, suit]):
            self._label = Rank(rank).label + Suit[suit.upper()].value
            self._rank, self._suit = self.parse_label(self.label)
        else:
            raise ValueError("Expected either `label`, or both of `rank` and `suit`.")

    @classmethod
    def parse_label(cls, label):
        """Parse a label into a formally defined rank and suit.

        Parameters
        ----------
        label : str
            A card label, like 'As', to be parsed into a rank and suit.

        Returns
        -------
        int
            A rank value as defined in `enums.Rank.
        str
            A suit value as defined in `enums.Suit`.

        """
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
        """int: The integer rank, from `enums.Rank`, for this card."""
        return self._rank
    
    @property
    def suit(self):
        """str: The suit, from `enums.Suit`, for this card."""
        return self._suit
    
    @property
    def label(self):
        """str: The label abbreviation for this card."""
        return self._label

if __name__ == '__main__':
    td = Card('td')
    qh = Card(rank=12, suit=Suit.HEARTS.name)
    ad = Card('Ad')
    
    assert ad > qh > td > 9
