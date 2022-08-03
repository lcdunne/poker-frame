from collections import Counter
from card import Card
from enums import Rank, Suit, HandStrength

# These might be nice as staticmethods for the Hand class
# Might require passing in a hand object instead of x because x is different for different funcs.
# Can then go hand.rankhist or hand.rankings or hand.suithist as needed.


class Hand:
    """
    TODO: *
        - After ranking, hand needs to be represented:
            1. in its natural order (e.g. Js 9s 8s Ts Qs)
            2. in according to its category (e.g. Qs Js Ts 9s 8s)
            - We have a .contains and a .has method. We could have a .where method with a lambda to get this.:
                where( lambda x: x.suit == 'SPADES' ) (all spades)
                where( lambda x: x.rank == 10 ) (all 10s)
                ...
        - After ranking, hand needs to be represented as e.g. Twos full of Nines
        - The cards cannot repeat! Qs and Qs cannot appear... Makes me think of a set instead of list
    """
    def __init__(self, labels: list=None, cards=None, ):
        if labels is not None:
            cards = [Card(label) for label in labels]
        elif all([labels is None, cards is None]):
            raise ValueError("Expected either `label`, or both of `rank` and `suit`.")
        self.cards = cards
        self._current_index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index >= len(self.cards):
            self._current_index = 0
            raise StopIteration
        
        self._current_index += 1
        return self.cards[self._current_index-1]
    
    def __getitem__(self, i):
        return self.cards[i]
    
    def __repr__(self):
        return f"<Hand({self.labels})"
    
    @property
    def labels(self):
        """Labels for each card in the hand.

        Returns
        -------
        list
            Labels for each card in the hand, e.g. `['Qs', 'Qd', '9d', '9h', '9c']`.

        """
        return [c.label for c in self]
    
    @property
    def ranks(self):
        """Ranks for each card in the hand.

        Returns
        -------
        list
            Integer rankings for each card contained in the hand. Ranks 
            correspond to the integer values of the `enums.Rank` enum. The 
            values are sorted in descending order.

        """
        return sorted( [c.rank for c in self], reverse=True )
    
    @property
    def suits(self):
        """Suits for each card in the hand.

        Returns
        -------
        list
            Suits for each card contained in the hand, corresponding to the 
            names of the `enums.Suit` enum (e.g. 'SPADES').

        """
        return [c.suit for c in self.cards]
    
    @property
    def rankhist(self):
        """Rank histogram for each card's ranking in the hand.
        
        Given the hand `Hand(['Qs', 'Qd', '9d', '9h', '9c'])`, its rank 
        histogram will be `{9: 3, 12: 2}`.

        Returns
        -------
        dict
            Ranks and their corresponding counts, sorted in descending order. 
            The keys correspond to the card ranks themselves, while the values 
            are the corresponding counts.

        """
        return dict(Counter( self.ranks ).most_common())
    
    @property
    def suithist(self):
        """Suit histogram for each card's suit in the hand
        
        Given the hand `Hand(['Qs', 'Qd', '9d', '9h', '9c'])`, its suit 
        histogram will be `{'DIAMONDS': 2, 'SPADES': 1, 'HEARTS': 1, 'CLUBS': 1}`.

        Returns
        -------
        dict
            Suits and their corresponding counts. The keys correspond to the 
            suit names, while the values are the corresponding counts.

        """
        return dict(Counter( self.suits ).most_common())
    
    def has(self, label):
        """Check if the hand contains a card.

        Parameters
        ----------
        label : str
            The label of the target card.

        Returns
        -------
        bool
            True if the hand contains the card denoted by the given label.

        """
        return label in self.labels
    
    def is_pair(self):
        return len(self.rankhist) == 4

    def is_pair(x):
        """x: `Hand.rankhist`."""
        return len(x) == 4

    def is_twopair(x):
        """x: `Hand.rankhist.values()`."""
        return x == [2, 2, 1]

    def is_three_of_a_kind(x):
        """x: `Hand.rankhist.values()`."""
        return x == [3, 1, 1]

    def is_straight(x):
        """x: Sorted (desc) `Hand.rankings`."""
        is_wheel = x == [14, 5, 4, 3, 2]
        not_wheel = (len(x) == 5) and (x == list(range(max(x), min(x)-1, -1)))
        return is_wheel or not_wheel

    def is_flush(x):
        """x: `Hand.suithist`."""
        return len(x) == 1

    def is_fullhouse(x):
        """x: `list(Hand.rankhist.values())`"""
        return x == [3, 2]

    def is_four_of_a_kind(x):
        """x: `list(Hand.rankhist.values())`"""
        return x == [4, 1]

    def is_straightflush(rankhist, suithist):
        return self.is_straight(rankhist) and self.is_flush(suithist)



class HandSpace:
    pass

h = Hand(['Qs', 'Qd', '9h','9d', '9c'])