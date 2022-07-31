import random
from math import comb
from collections import Counter
from itertools import combinations
from enum import Enum, auto, IntEnum
from dataclasses import dataclass, field



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

HAND_STRENGTHS = {
    'HIGH_CARD': 0,
    'PAIR': 1,
    'TWO_PAIR': 2,
    'THREE_OF_A_KIND': 3,
    'STRAIGHT': 4,
    'FLUSH': 5,
    'FULL_HOUSE': 6,
    'FOUR_OF_A_KIND': 7,
    'STRAIGHT_FLUSH': 8,
    'ROYAL_FLUSH': 9
}

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


# These all return True if the hand category is denoted by the key
# Should take a hand.rankings (for the numerical) and hand.suits for the flushes
histmatch = {
    'PAIR': lambda x: len(x)==4,
    'TWO_PAIR': lambda x: sorted(x.values) == [1,2,2],
    'THREE_OF_A_KIND': lambda x: sorted(x.values) == [1,1,3],
    'STRAIGHT': lambda x: max(x.values) - min(x.values) in [4, 12],
    'FULL_HOUSE': lambda x: sorted(x.values) == [2,2],
    'FOUR_OF_A_KIND': lambda x: sorted(x.values) == [1,4],
}


class HoleCards:
    def __init__(self, deck):
        pass

class CommunityCards:
    def __init__(self, deck):
        pass

class Hand:
    def __init__(self, cards):
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
    
    def __str__(self):
        return f"Hand: {self.strength} ({','.join([h.name for h in self.cards])})"
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, obj):
        return self.cards[obj]
    
    def __eq__(self, other):
        return self._strength.value == other._strength.value
    
    def __ne__(self, other):
        return self._strength.value != other._strength.value
    
    def __lt__(self, other):
        return self._strength.value < other._strength.value
    
    def __le__(self, other):
        return self._strength.value <= other._strength.value
    
    def __gt__(self, other):
        return self._strength.value > other._strength.value
    
    def __ge__(self, other):
        return self._strength.value > other._strength.value
    

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
        
    
    # def rank_all_hands(self):
    #     # Rank all han
    #     # self.temp = []
    #     # TODO: Could sort the hands on initialisation, or could sort only when testing.
    #     # Probably best to sort on the handspace init because then we only do it once.
    #     for handstrength, fun in self._rank_funcs.items():
    #         hit = fun()
    #         if hit:
    #             print(handstrength, Hand(self.cards))
    #             break
    #     #         self.temp.append(self.cards)
    #     #         self.types[handstrength].append(self.cards)
    #     #         break
    #     # if not hit:
    #     #     # Must be a highcard.
    #     #     self.add_handtype(HandStrengths.HIGH_CARD)
    
    # def classify_hand(self):
    #     for handstrength, fun in self._rank_funcs.items():
    #         if fun():
    #             return self, handstrength
    #     # If it got to here without returning, handstrength is HIGH_CARD
    #     return self, HandStrengths.HIGH_CARD.name
    
    def classify_hand(self):
        for handstrength, fun in self._rank_funcs.items():
            if fun():
                self._strength = HandStrengths[handstrength]
                return
        # If it got to here without returning, handstrength is HIGH_CARD
        self._strength = HandStrengths.HIGH_CARD.name


    # Hand Strengh Categorisation. Each one has a different check
    def is_royalflush(self):
        # Technically indistinct from straight flush but whatever.
        return self.is_straightflush() and max(self) == 14

    def is_straightflush(self):
        return self.is_straight() and self.is_flush()

    def is_fourofakind(self):
        return list(self.rankhist.values()) == [4, 1]

    def is_fullhouse(self):
        return list(self.rankhist.values()) == [3, 2]

    def is_flush(self):
        return len(self.suithist) == 1

    def is_straight(self):
        # return max(self.rankings) - min(self.rankings) in [4, 12] # If other checks pass first
        _rankings = sorted([1 if i==14 else i for i in self.rankings])
        return _rankings == list(range(min(_rankings), max(_rankings)+1))


    def is_threeofakind(self):
        return list(self.rankhist.values()) == [3, 1, 1]
    
    def is_twopair(self):
        # This one is tricky. Need the HIGHER pair of the two...
        # Could potentially have __gt__ & __lt__ funcs for this.....
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
        self.madehands = {k: [] for k in HandStrengths.items()}

    def getcombos(self, k=None):
        # Gets all combinations in hand space
        if k is None:
            k = 5 if len(self.space) > 5 else len(self.space)
        
        n = len(self.holecards) + len(self.community_cards)
        if k > n:
            raise ValueError(f"Tried to get {k} combinations from a space of {n}")
        return list(combinations(self.space, k))
    
    def findbesthand(self):
        # Loop over 7C5=21 combinations of 5-card hands
        best_hands = []
        for i, combo in enumerate(self.getcombos()):
            # print(i, Hand(combo))
            hand = Hand(combo)

            # print(f"iteration {i}: {hand} {'-'*70} #")
            # Rank all available made hands in this 5-card hand
            # After this, hand.types must have at least high card in it.
            # Test with.. if not hand.types: raise ValueError or something
            hand.rank_all_hands() # now see hand.types
            
            # print(hand.types)
            # for k, v in hand.types.items():
            #     if v:
            #         print("Adding ", k)
            #         self.types[k].append(v)
            # print()
            
            '''Problem:
                We want to pick from the top because this will naturally be the best hand.
                It therefore makes sense to descend through hand.types and stop when found.
                However, HIGH_CARD types are more likely, and these are from the bottom.
                This means we will most frequently be going close to the bottom (lots of search).
            Solution:
                Might be better to create a new dict 
            '''
            
            # Loop over all handstrengths in desc order.
            # If a hand is found, extract all combinations (may be > 1) and end
            for handstrength in sorted(HandStrengths, reverse=True):
                if hand.types.get(handstrength.name):
                    print(f"Found {handstrength.name}\t{hand}")
                    best_hands.append(hand.cards)
                    break
            # print(handstrength, [Hand(h) for h in best_hands])
        # Fails with handspace of [9,9,9,A,A,K,K]
        return best_hands





if __name__ == '__main__':
    deck = Deck()
    # random.seed(24) # for repeatability
    
    # TODO: distinguish [AAA22 from 222AA]

    hole = deck.take(names=['9s', 'Jh'])
    community = deck.take(names=['Jd', '9h', '9c', '2s', '2d'])
    hs = HandSpace(hole, community) # No sort
    # best = hs.findbesthand()
    # best_hand = Hand(max(best))
    # print(best_hand)
    # # results = []
    
    # Given a handspace...
    # Loop through all combinations in the handspace
    # Terminate on the best hand
    # Append it to the dict of available made hands
    MADEHANDS = {k: [] for k in HandStrengths.items()}
    for i, combo in enumerate(hs.getcombos()):
        hand = Hand(combo) # no sorted
        print(f"{'-'*70} #\niteration {i}")
        print(hand)
        # hand.rank_all_hands()
        # _, strength = hand.classify_hand()
        # print(strength)
        # MADEHANDS[strength].append(hand)
        
        
        
        # print()
        # if strength == 'STRAIGHT':
        #     break
        # if hand[0].rank < max(hand).rank:
        #     break
    
        