from collections import Counter
from card import Card
from enums import HandStrength

class Hand:
    """A poker hand.
    
    Notes
    ----
    Hands are compared first according to `enums.Handstrength` rankings, but 
    if they are the same ranking, then additional checks are made to determine 
    which hand if any is stronger than the other within the same rank.

    Parameters
    ----------
    labels : list, optional
        A list of card string labels, like `As`, or `2c`, from which to create 
        the hand. The default is None.
    cards : list, optional
        A list of `Card` instances if these have already been created. The 
        default is None.

    Raises
    ------
    ValueError
        If the the labels are non-unique.
        If both label and cards are None.
        If number of labels is less than 1 or greater than 5.

    """
    def __init__(self, labels: list=None, cards: Card=None):
        if labels is not None:
            if len(set(labels)) != len(labels):
                _found_error = [f"{c} (x{n})" for c, n in Counter(labels).most_common() if n > 1]
                raise ValueError(f"Labels must be unique, but got: {_found_error}")
            elif (len(labels) < 1) or (len(labels) > 5):
                raise ValueError("A hand must be nonzero and can only be made from a maximum of 5 cards.")
                
            cards = [Card(label) for label in labels]

        elif (labels is None) and (cards is None):
            raise ValueError("Expected either `label`, or both of `rank` and `suit`.")

        self.cards = cards
        self._strength = None
        self._draws = None
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
        self._draw_funcs = {
            
        }
        
        self.classify_hand()
        self.sort_by_strength()
        _, self._kicker_cards = self._kickersplit()
    
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
        return f"<Hand({self.labels})>"
    
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
    
    @property
    def draws(self):
        return self._draws
    
    @property
    def components(self):
        return [self.get_by_rank(k) for k in self.rankhist]
    
    @property
    def kicker(self):
        return self._kicker_cards
    
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
    
    def _kickersplit(self):
        mains = [comp for comp in self.components if len(comp)>1]
        kicks = [comp.pop() for comp in self.components if len(comp)==1]

        if (len(kicks) == len(self)) or (1 not in self.rankhist.values()):
            return None, None

        return mains, kicks
    
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

# example hands
sf = Hand(['Jh', '9h', 'Qh', '8h', 'Th'])
quads = Hand(['Qc','6d', '6c',  '6h', '6s'])
fh = Hand(['2h', '9s', '2c', '2d', '9h'])
flush = Hand(['6d', '3d', 'Ad', 'Jd', '9d'])
straight = Hand(['7d', '9d', '5h', '8d', '6c'])
trips = Hand(['Qc', '6d', 'Ah', '6h', '6s'])
tp1 = Hand(['2d', '6s', '9c', '9h', '2h'])
tp2 = Hand(['4s', '8c', '4h', '8d', 'Kh'])
trips1 = Hand( ['7c', '7d', '7h', 'Kc', 'Ts'] )
pair = Hand(['3h', '3c', '6s', 'Td', 'Jh'])
hc = Hand(['3h', '2c', '6s', 'Td', 'Jh'])

# Draws
from itertools import combinations

oesd_fd = Hand(['Js', 'Ts', 'Qh',])
full_straightwidth = []
for card in oesd_fd:
    straightwidth = range(
        card.rank-4 if card.rank-4 >= 2 else 2,
        card.rank+4 if card.rank+4 <= 14 else 14+1
    )
    # print(card, list(straightwidth))
    full_straightwidth.extend(list(straightwidth))
# print(set(full_straightwidth))

# Looping through, we could create rankhists and suithists for each iteration and see
possibles = list(combinations(full_straightwidth, 5-len(oesd_fd)))
# But to do that we need to convert the ranking functions to staticmethods that receive arguments
# Then we can pass in a hypothetical rankhist or an actual rankhist, etc.
for p in possibles:
    if any([p_i for p_i in p if p_i in oesd_fd.ranks]):
        continue
    # print(list(p), oesd_fd.ranks)
    
    # Now loop over all ps, get every combination of p_i and suit to create labels
    # Then stick those together with the current drawing hand's labels.
    # Then check if it's a straight. if it is, then put it into the draws.