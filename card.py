import random
from collections import Counter
from itertools import combinations
from enum import Enum, IntEnum
from dataclasses import dataclass, field


class ExtendedEnum(Enum):
    @classmethod
    def items(cls):
        return list(map(lambda c: c.name, cls))
    
    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))

class Suit(ExtendedEnum):
    CLUBS = 'c'
    DIAMONDS = 'd'
    HEARTS = 'h'
    SPADES = 's'

class Rank(IntEnum, ExtendedEnum):
    # Access with Rank.TWO.name, Rank.TWO.value
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

class HandStrengths(IntEnum, ExtendedEnum):
    # Ended up being used like a dictionary with many hoops just to get keys & values...
    # Probably get rid and replace with a dict.
    # Could also use IntEnum........................
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


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
        self._current_index = 0
        if self.form == 'kuhn':
            # Filter out all those not specified according to Kuhn poker
            # Possibly not relevant for Deck class?
            self.cards = self._kuhnify()

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index >= len(self.cards):
            self._current_index = 0
            raise StopIteration

        # card = self.cards[self._current_index]
        self._current_index += 1
        # return card
        return self.cards[self._current_index-1]
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, obj):
        return self.cards[obj]
    
    def __repr__(self):
        return f"Deck(form={self.form})"

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
    
    def pop(self, index=-1):
        return self.cards.pop(index)
    
    def search(self, lambda_=None):
        return list(filter(lambda_, self.cards))
    
    def has(self, name):
        return len(self.search(lambda x: x.name == name)) > 0
    
    def index(self, value):
        # Given a value, returns the index. E.g., deck.index('As') -> 
        for i, card in enumerate(self.cards):
            if card.name == value:
                return i
    
    def take(self, n=None, names=None, lambda_=None):
        # n: select 
        
        if names is not None:
            if isinstance(names, str):
                names = [names]
            lambda_ = lambda x: x.name in names
        
        if lambda_ is not None:
            taken = []
            for card in self.search(lambda_):
                taken.append(self.pop(self.index(card.name)))

            return taken
        
        if n is None:
            raise ValueError("Must specify either n or lambda_")
        
        return [self.cards.pop() for _ in range(n)]

class HoleCards:
    def __init__(self, deck):
        pass

class CommunityCards:
    def __init__(self, deck):
        pass

def card_from_name(name: str):
    # Construct a card from a name like 'Ts', 5d', Ah', ...
    # Needs major improvements, should be able to construct a card like this anyway
    rank, suit = name
    return Card(rank=Rank[RankName(rank).name].value, suit=Suit(suit).name)

class Hand:
    def __init__(self, cards=None, names: list=None):
        if not any([cards, names]):
            raise ValueError("Need either `cards` or `names` but got None for both")
        
        if cards is None:
            cards = [card_from_name(name) for name in names]
        
        self.cards = cards
        self.types = {k: [] for k in HandStrengths.items()}
        self._current_index = 0
        self._rank_funcs = {
            HandStrengths.ROYAL_FLUSH.name: self.is_royalflush,
            HandStrengths.STRAIGHT_FLUSH.name: self.is_straightflush,
            HandStrengths.FOUR_OF_A_KIND.name: self.is_fourofakind,
            HandStrengths.FULL_HOUSE.name: self.is_fullhouse,
            HandStrengths.FLUSH.name: self.is_flush,
            HandStrengths.STRAIGHT.name: self.is_straight,
            HandStrengths.THREE_OF_A_KIND.name: self.is_threeofakind,
            HandStrengths.TWO_PAIR.name: self.is_twopair,
            HandStrengths.PAIR.name: self.is_pair,
        }
        self.classify_hand()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index >= len(self.cards):
            self._current_index = 0
            raise StopIteration

        card = self.cards[self._current_index]
        self._current_index += 1
        return card
    
    def __repr__(self):
        return f"<Hand(names={self.names})"
    
    def __str__(self):
        return f"Hand: {self.strength} ({','.join([h.name for h in self.cards])})"
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, obj):
        return self.cards[obj]
    
    # Comparisons
    def __eq__(self, other):
        if self._strength.value == other._strength.value:
            # Check if strength
            if self.is_suited_or_sequential(self):
                # Since they have the same value, must both be suited/seq.
                # Compare highest rankings
                return max(self.rankings) == max(other.rankings)
            else:
                # Must both be high, pair, 2-pair, trips, boat, or quads.
                # Sort histogram by max count and return the key (e.g. {10:3, 4:2} -> 10)
                return next(iter(self.rankhist)) == next(iter(other.rankhist))
        else:
            return False
    
    def __ne__(self, other):
        if self._strength.value == other._strength.value:
            if self.is_suited_or_sequential(self):
                return max(self.rankings) != max(other.rankings)
            else:
                return next(iter(self.rankhist)) != next(iter(other.rankhist))
        else:
            return True
    
    def __lt__(self, other):
        if self._strength.value == other._strength.value:
            if self.is_suited_or_sequential(self):
                return max(self.rankings) < max(other.rankings)
            else:
                return next(iter(self.rankhist)) < next(iter(other.rankhist))
        else:
            return self._strength.value < other._strength.value
    
    def __le__(self, other):
        if self._strength.value == other._strength.value:
            if self.is_suited_or_sequential(self):
                return max(self.rankings) <= max(other.rankings)
            else:
                return next(iter(self.rankhist)) <= next(iter(other.rankhist))
        else:
            return self._strength.value <= other._strength.value
    
    def __gt__(self, other):
        if self._strength.value == other._strength.value:
            if self.is_suited_or_sequential(self):
                return max(self.rankings) > max(other.rankings)
            else:
                return next(iter(self.rankhist)) > next(iter(other.rankhist))
        else:
            return self._strength.value > other._strength.value
    
    def __ge__(self, other):
        if self._strength.value == other._strength.value:
            if self.is_suited_or_sequential(self):
                return max(self.rankings) >= max(other.rankings)
            else:
                return next(iter(self.rankhist)) >= next(iter(other.rankhist))
        else:
            return self._strength.value >= other._strength.value
    
    @property
    def names(self):
        return [h.name for h in self.cards]
    
    @property
    def rankings(self):
        return [c.rank for c in self.cards]

    @property
    def suits(self):
        return [c.suit for c in self.cards]
    
    @property
    def rankhist(self):
        return dict(Counter(self.rankings).most_common())
    
    @property
    def suithist(self):
        return dict(Counter(self.suits).most_common())
    
    @property
    def strength(self):
        return self._strength.name
    
    def classify_hand(self):
        for handstrength, fun in self._rank_funcs.items():
            
            if fun():
                self._strength = HandStrengths[handstrength]
                return
        # If it got to here without returning, handstrength is HIGH_CARD
        self._strength = HandStrengths.HIGH_CARD
    
    @staticmethod
    def is_suited_or_sequential(hand):
        # Convenience function to check if the hand is either straight- or flush-like
        return hand._strength in [
            HandStrengths.FLUSH,
            HandStrengths.STRAIGHT,
            HandStrengths.STRAIGHT_FLUSH,
        ]
    
    def contains(self, holecards) -> int:
        return len([c for c in holecards if c in self])
    
    def has(self, name):
        return card_from_name(name) in self

    # Hand Strengh Categorisation. Each one has a different check
    # Alternative idea is to have these all as separate lambdas to loop through
    def is_royalflush(self):
        # Technically indistinct from straight flush but whatever.
        return self.is_straightflush() and max(self).rank == 14

    def is_straightflush(self):
        return self.is_straight() and self.is_flush()

    def is_fourofakind(self):
        return list(self.rankhist.values()) == [4, 1]

    def is_fullhouse(self):
        return list(self.rankhist.values()) == [3, 2]

    def is_flush(self):
        return len(self.suithist) == 1

    def is_straight(self):
        if self.rankings == [14,5,4,3,2]:
            return True
        else:
            return max(self.rankings) - min(self.rankings) == 4

    def is_threeofakind(self):
        return list(self.rankhist.values()) == [3, 1, 1]
    
    def is_twopair(self):
        return list(self.rankhist.values()) == [2, 2, 1]
    
    def is_pair(self):
        return len(self.rankhist) == 4
    
    def add_handtype(self, handstrength):
        # Use in each evaluation check
        self.types[handstrength.name].append(self.cards)

class HandSpace:
    # Handspace is the entire set of community cards plus holecards (max 7 in NLHE)
    def __init__(self, holecards: list, community_cards: list):
        self.holecards = holecards
        self.community_cards = community_cards
        self.space = sorted(self.holecards + self.community_cards, reverse=True) # SORTED HERE
        self.types = {k: [] for k in HandStrengths.items()}
        self._made_hands = {k: [] for k in HandStrengths.values()}
        self._find_best_hand()
    
    @property
    def best_hand(self):
        return self._best_hand
    
    @property
    def made_hands(self):
        return self._made_hands

    def getcombos(self, k=None):
        # Gets all combinations in hand space
        if k is None:
            k = 5 if len(self.space) > 5 else len(self.space)
        
        n = len(self.holecards) + len(self.community_cards)
        if k > n:
            raise ValueError(f"Tried to get {k} combinations from a space of {n}")
        return list(combinations(self.space, k))

    def _find_all_hands(self):
        # From the entire hand space, finds all available made hands
        for i, hand_combination in enumerate( self.getcombos() ):
            hand = Hand(hand_combination)
            self._made_hands[hand._strength.value].append( hand )
        self._made_hands = {k: v for k, v in self._made_hands.items() if v}
    
    def _find_best_hand(self):
        # From the entire set of available made hands, gets 
        self._find_all_hands()
        self._best_hand = max(self.made_hands[max(self.made_hands)])
        return self._best_hand


if __name__ == '__main__':
    deck = Deck()
    random.seed(24) # for repeatability
    deck.shuffle()
    holecards = deck.take(2)
    community_cards = deck.take(5)

    # holecards = deck.take(names=['9s', 'Jh'])
    # community_cards = deck.take(names=['Jd', '9h', '9c', '2s', '2d'])
    
    
    hs = HandSpace(holecards, community_cards)
    print(f"Best hand (out of {len(hs.space)} made hands): {hs.best_hand} (using {hs.best_hand.contains(holecards)} holecard(s))")


