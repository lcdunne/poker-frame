from collections import Counter
from card import Card
from enums import HandStrength

# These might be nice as staticmethods for the Hand class
# Might require passing in a hand object instead of x because x is different for different funcs.
# Can then go hand.rankhist or hand.rankings or hand.suithist as needed.


class Hand:
    """
    TODO: *
        - After ranking, hand needs to be represented:
            1. in its natural order (e.g. Js 9s 8s Ts Qs)
            2. in according to its category (e.g. Qs Js Ts 9s 8s). Perhaps `[*Counter(hself.rankhist).elements()]`
                Ordering could also happen via indexes:
                    [x for _, x in sorted(zip(Counter(h.rankhist).elements(), h.cards))]
            - We have a .contains and a .has method. We could have a .where method with a lambda to get this.:
                where( lambda x: x.suit == 'SPADES' ) (all spades)
                where( lambda x: x.rank == 10 ) (all 10s)
                ...
            
            - Seems like the obvious way to do this is to have masks for each hand type:
                [2, 2, 1, 1, 0] for 2pair, for example.
            - Or we could pop the end off:
                
                >>> hand = Hand(['4s', '5c', '4h', 'Ad', 'Th'])
                >>> mask = [1,1,0,0,0]
                >>> a = [card for i, card in enumerate(hand) if mask[i]==1]
                >>> z = [card for i, card in enumerate(hand) if mask[i]==0]
                >>> sorted(a, reverse=True) + sorted(z, reverse=True)
                [<Card('4s')>, <Card('4h')>, <Card('Ad')>, <Card('Th')>, <Card('5c')>]
                
        - After ranking, hand needs to be represented as e.g. Twos full of Nines
        - The cards cannot repeat! Qs and Qs cannot appear... Makes me think of a set instead of list
    """
    def __init__(self, labels: list=None, cards=None, ):
        if labels is not None:
            if len(set(labels)) != len(labels):
                _found_error = [f"{c} (x{n})" for c, n in Counter(labels).most_common() if n > 1]
                raise ValueError(f"Labels must be unique, but got: {_found_error}")
            elif (len(labels) < 1) or (len(labels) > 5):
                raise ValueError("A hand must be nonzero and can only be made from a maximum of 5 cards.")
                
            cards = [Card(label) for label in labels]

        elif all([labels is None, cards is None]):
            raise ValueError("Expected either `label`, or both of `rank` and `suit`.")

        self.cards = cards
        self._strength = None
        self._current_index = 0
        self._rank_funcs = {
            # HandStrength.ROYAL_FLUSH.name: self.is_royalflush, # not important
            HandStrength.STRAIGHT_FLUSH.name: self.is_straightflush,
            HandStrength.FOUR_OF_A_KIND.name: self.is_four_of_a_kind,
            HandStrength.FULL_HOUSE.name: self.is_full_house,
            HandStrength.FLUSH.name: self.is_flush,
            HandStrength.STRAIGHT.name: self.is_straight,
            HandStrength.THREE_OF_A_KIND.name: self.is_three_of_a_kind,
            HandStrength.TWO_PAIR.name: self.is_twopair,
            HandStrength.PAIR.name: self.is_pair,
        }
        self.classify_hand()
        self.sort_by_strength()
    
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
    
    def __len__(self):
        return len(self.cards)
    
    def __repr__(self):
        return f"<Hand({self.labels})"
    
    # Comparisons ----------- #
    # Note on comparisons...
    # Absolute rank is the first comparison to make.
    # But if they are both equal, need a way to distinguish the best from hand.
    # Given that they are sorted by this point, it should just be a case of comparing the first card.
    # We could make a handmask attribute..
    # We could compare rankhist
    def __lt__(self, other):
        if self._strength.value == other._strength.value:
            for l1, l2 in zip(self.components, other.components):
                if l1[0] > l2[0]:
                    return False
                elif l1[0] == l2[0]:
                    continue
                else:
                    return True
            return False
        else:
            return self._strength.value < other._strength.value
    
    def __le__(self, other):
        if self._strength.value == other._strength.value:
            for l1, l2 in zip(self.components, other.components):
                if l1[0] > l2[0]:
                    return False
                elif l1[0] == l2[0]:
                    continue
                else:
                    return True
            return True
        else:
            return self._strength.value <= other._strength.value

    def __eq__(self, other):
        if self._strength.value == other._strength.value:
            for l1, l2 in zip(self.components, other.components):
                if l1[0] > l2[0]:
                    return False
                elif l1[0] == l2[0]:
                    continue
                else:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        if self._strength.value == other._strength.value:
            for l1, l2 in zip(self.components, other.components):
                if l1[0] > l2[0]:
                    return True
                elif l1[0] == l2[0]:
                    continue
                else:
                    return True
            return False
        else:
            return True
    
    def __ge__(self, other):
        if self._strength.value == other._strength.value:
            for l1, l2 in zip(self.components, other.components):
                if l1[0] > l2[0]:
                    return True
                elif l1[0] == l2[0]:
                    continue
                else:
                    return False
            return True
        else:
            return self._strength.value >= other._strength.value
    
    def __gt__(self, other):
        if self._strength.value == other._strength.value:
            # We need to split the hand into its components to identify which is greater.
            for l1, l2 in zip(self.components, other.components):
                if l1[0] > l2[0]:
                    return True
                elif l1[0] == l2[0]:
                    continue
                else:
                    return False
            return False
        else:
            return self._strength.value > other._strength.value
    
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
    
    @property
    def strength(self):
        """The strength category name of the hand (see `enums.Handstrength`)

        Returns
        -------
        str
            Hand strength name.

        """
        return self._strength.name
    
    def get_by_rank(self, rank):
        """Get a card by its rank.

        Parameters
        ----------
        rank : int
            The integer ranking for the target return card.

        Returns
        -------
        list
            A list of cards with rank equal to `rank`. Returns empty list if 
            there were no matches.

        """
        return [c for c in self if c.rank == rank]
    
    def get_by_count(self, count):
        """Get a card by its count in the hand histogram.
        
        For example, if the hand is three of a kind, then getting all cards 
        with a count of 1 will give the kicker.

        Parameters
        ----------
        count : int
            The integer count for the target return card.

        Returns
        -------
        list
            A list of cards with rank equal to `rank`. Returns empty list if 
            there were no matches.

        """
        result = []
        for rank in [k for k, v in self.rankhist.items() if v == count]:
            result.extend( self.get_by_rank(rank) )
        return result
    
    def _is_suited_or_sequential(self):
        # Convenience function to check if the hand is either straight- or flush-like
        return self._strength in [
            HandStrength.FLUSH,
            HandStrength.STRAIGHT,
            HandStrength.STRAIGHT_FLUSH,
        ]
    
    def kickersplit(self):
        self.kicker = self.get_by_count(1)
        if self._is_suited_or_sequential():
            # No kicker. Maybe return (self.cards, [])
            return
        mains = [c for c in self.cards if self.rankhist[c.rank] > 1]
        kicks = [c for c in self.cards if self.rankhist[c.rank] == 1]
        return mains, kicks
    
    @property
    def components(self):
        # Split the hand into component parts based on its ranking histogram.
        # Hand(['9c', '9h', '2d', '2h', '6s'] becomes [[<('9c')>, <('9h')>], [<('2d')>, <('2h')>], [<('6s')>]]
        # result = []
        # for k in self.rankhist:
        #     result.append( self.get_by_rank(k) )
        # return result
        return [self.get_by_rank(k) for k in self.rankhist]
        
        
    
    
    def mask(self):
        pass
    
    def sort_by_strength(self):
        """Sort the hand based on its strength and according to the histogram.
        
        Notes
        -----
        A hand like `Hand(['Ks', 'Tc', 'Ts', 'Td', 'Th'])` becomes 
        `Hand(['Tc', 'Ts', 'Td', 'Th', 'Ks'])`
        
        A a hand like `Hand(['4s', '5c', '4h', '5d', 'Kh'])` becomes 
        `Hand(['5c', '5d', '4s', '4h', 'Kh'])`.

        Returns
        -------
        None.

        """
        x = []
        for rank in self.rankhist:
            x.extend(self.get_by_rank(rank))
        self.cards = x
    
    def classify_hand(self):
        """Classify strength of hand.

        Returns
        -------
        None.

        """
        # if len(self) == 5: classify_madehand() else classify_draw()
        if len(self) == 5:
            for handstrength, fun in self._rank_funcs.items():
                if fun():
                    self._strength = HandStrength[handstrength]
                    return

        self._strength = HandStrength.HIGH_CARD
    
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

    def is_three_of_a_kind(self):
        """Check if a 5-card hand is three of a kind.
        
        A hand like `Hand(['Ks', 'Kc', 'Kd', 'Td', '2d'])` has a rank histogram 
        of `{13: 3, 10: 1, 2: 1}`, with `.values()` equal to `[3, 1, 1]`.

        Returns
        -------
        bool
            Whether or not the hand's rank histogram counts match for three of 
            a kind.

        """
        return list(self.rankhist.values()) == [3, 1, 1]

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
    '''
    A hand space is an abstract representation of all possible holdings given a 
    set of cards in the range [2, 7]. A handspace from just two cards reflects 
    having been dealt two holecards but no flop. A handspace from five cards 
    reflects having been dealt two holecards and the flop, and will necessarily 
    contain just one combination for the five-card hand. Handspaces of 6 and 7 
    cards increase the number of combinations and reflect having seen the turn 
    and river, respectively.
    '''
    pass

sf = Hand(['Jh', '9h', 'Qh', '8h', 'Th'])
quads = Hand(['Qc','6d', '6c',  '6h', '6s'])
fh = Hand(['2h', '9s', '2c', '2d', '9h']) # doesn't work for full house
flush = Hand(['6d', '3d', 'Ad', 'Jd', '9d'])
straight = Hand(['7d', '9d', '5h', '8d', '6c'])
trips = Hand(['Qc', '6d', 'Ah', '6h', '6s'])
tp1 = Hand(['2d', '6s', '9c', '9h', '2h'])
tp2 = Hand(['4s', '8c', '4h', '8d', 'Kh'])
trips1 = Hand( ['7c', '7d', '7h', 'Kc', 'Ts'] )
pair = Hand(['3h', '3c', '6s', 'Td', 'Jh'])
hc = Hand(['3h', '2c', '6s', 'Td', 'Jh'])

# # if it isn't straight or flush, then its components are:
# #  each unique count > 1 and 
# for A, B in zip(tp1.rankhist, tp2.rankhist):
#     # zip self.rankhist, other.rankhist
#     print(A, B)

hand = tp1
other = tp2

A = list(Counter(hand.rankhist).elements())
B = list(Counter(other.rankhist).elements())

# for i, j in zip(A, B):
#     if i > j:
#         return True
#     else:
#         return False

# Because the hands by this point are arranged semantically, then we can simply compare the first element:
# [c1 > c2 for c1, c2 in zip(hand, other)][0].. or just hand[0] > other[0]...


# for h1c, h2c in zip(hand.components, other.components):
#     print(h1c, h2c)
#     if h1c[0] > h2c[0]:
#         print("\tH1 > H2")
#     elif h1c[0] == h2c[0]:
#         print("The same")

L1 = [ [7, 7], [5, 6], [4] ]
L2 = [ [7, 7], [5, 5], [4] ]

def complist(L1, L2):
    # Is L1 equal to L2?
    for l1, l2 in zip(L1, L2):
        if l1[0] > l2[0]:
            return False
        elif l1[0] == l2[0]:
            continue
        else:
            return False
    return True

print(complist(L1, L2))