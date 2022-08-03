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
            if len(set(labels)) != len(labels):
                _found_error = [f"{c} (x{n})" for c, n in Counter(labels).most_common() if n > 1]
                raise ValueError(f"Labels must be unique, but got: {_found_error}")
            cards = [Card(label) for label in labels]

        elif all([labels is None, cards is None]):
            raise ValueError("Expected either `label`, or both of `rank` and `suit`.")

        self.cards = cards
        self._current_index = 0
        self._rank_funcs = {
            # HandStrength.ROYAL_FLUSH.name: self.is_royalflush,
            HandStrength.STRAIGHT_FLUSH.name: self.is_straightflush,
            HandStrength.FOUR_OF_A_KIND.name: self.is_four_of_a_kind,
            HandStrength.FULL_HOUSE.name: self.is_full_house,
            HandStrength.FLUSH.name: self.is_flush,
            HandStrength.STRAIGHT.name: self.is_straight,
            HandStrength.THREE_OF_A_KIND.name: self.is_three_of_a_kind,
            HandStrength.TWO_PAIR.name: self.is_twopair,
            HandStrength.PAIR.name: self.is_pair,
        }
        # self.classify_hand()
    
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
        """Check if a 5-card hand is a pair.
        
        A hand like `Hand(['Ks', 'Kc', 'Ts', '8d', '2d'])` has a rank histogram 
        of `{13: 2, 10: 1, 8: 1, 2: 1}`, which has 4 elements, and this will be 
        the case for all hands that contain a pair.

        Returns
        -------
        bool
            Whether or not the hand's rank histogram has four elements.

        """
        return len(self.rankhist) == 4


    def is_twopair(self):
        """Check if a 5-card hand is two pair.
        
        A hand like `Hand(['Ks', 'Kc', 'Ts', 'Td', '2d'])` has a rank histogram 
        of `{13: 2, 10: 2, 2: 1}`, with `.values()` equal to `[2, 2, 1]`.

        Returns
        -------
        bool
            Whether or not the hand's rank histogram counts match for two pair

        """
        return list(self.rankhist.values()) == [2, 2, 1]

    def is_three_of_a_kind(x):
        """Check if a 5-card hand is three of a kind.
        
        A hand like `Hand(['Ks', 'Kc', 'Kd', 'Td', '2d'])` has a rank histogram 
        of `{13: 3, 10: 1, 2: 1}`, with `.values()` equal to `[3, 1, 1]`.

        Returns
        -------
        bool
            Whether or not the hand's rank histogram counts match for three of 
            a kind.

        """
        return x == [3, 1, 1]

    def is_straight(self):
        """Check if a 5-card hand is a straight.
        
        A hand like `Hand(['4c', '3d', '5s', 'Ah', '2c'])` has a ranks list of 
        `[14, 5, 4, 3, 2]`, and will return `True` because it is a wheel straight.
        
        A hand like `Hand(['Tc', '9d', '8s', '7h', '6c'])` has a ranks list of 
        `[10, 9, 8, 7, 6]`, and will return `True` because it is a straight. In 
        this case, the "straight pattern" is a `list` representation of 
        `range(maxrank, minrank-1, -1)`.

        Returns
        -------
        bool
            Whether or not the hand's rank list matches the expected pattern 
            for a straight.

        """
        return self.ranks in [[14, 5, 4, 3, 2], list(range(max(self.ranks), min(self.ranks)-1, -1))]

    def is_flush(self):
        """Check if a 5-card hand is a flush.
        
        A hand like `Hand(['Td', '3d', '8d', '7d', '6d'])` has a suits 
        histogram of `{'DIAMONDS': 5}`, which is a single element long and is 
        therefore a flush.

        Returns
        -------
        bool
            Whether or not the hand is comprised of a single suit.

        """
        
        return len(self.suithist) == 1

    def is_full_house(self):
        """Check if a 5-card hand is a full house.
        
        A hand like `Hand(['Ks', 'Kc', 'Ts', 'Td', 'Th'])` has a rank histogram 
        of `{13: 2, 10: 2, 2: 1}`, with values `[3, 2]`.

        Returns
        -------
        bool
            Whether or not the hand is a full house.
        
        """
        return list(self.rankhist.values()) == [3, 2]

    def is_four_of_a_kind(self):
        """Check if a 5-card hand is a full house.
        
        A hand like `Hand(['Ks', 'Tc', 'Ts', 'Td', 'Th'])` has a rank histogram 
        of `{10: 4, 13: 1}`, with values `[4, 1]`.

        Returns
        -------
        bool
            Whether or not the hand is a full house.
        
        """
        return list(self.rankhist.values()) == [4, 1]

    def is_straightflush(self):
        """Check if a 5-card hand is a straight flush.
        
        See `Hand.is_flush` and `Hand.is_straight` for details.

        Returns
        -------
        bool
            Whether or not the hand is simultaneously a flush and a straight.

        """
        return self.is_straight() and self.is_flush()



class HandSpace:
    pass

h = Hand(['Ks', 'Tc', 'Ts', 'Td', 'Th'])