import random
from collections import Counter
from itertools import combinations
from enum import Enum, auto
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

class Rank(ExtendedEnum):
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

class HandStrengths(ExtendedEnum):
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

class HoleCards:
    def __init__(self, deck):
        pass

class CommunityCards:
    def __init__(self, deck):
        pass

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.strength = 0
        self.types = {k: [] for k in HandStrengths.items()}
        self._current_index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index >= len(self.cards):
            self._current_index = 0
            raise StopIteration

        card = self.cards[self._current_index]
        self._current_index += 1
        return card
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, obj):
        return self.cards[obj]

    def __repr__(self):
        return ','.join([h.name for h in self.cards])

    @property
    def rankings(self):
        return [c.rank for c in self.cards]

    @property
    def suits(self):
        return [c.suit for c in self.cards]

    # Hand Strengh Categorisation. Each one has a different check
    def is_royalflush(self):
        self.strength = max(900, self.strength)
        self.add_handtype(HandStrengths.ROYAL_FLUSH)
        return all([self.is_straight(), self.is_flush(), max(self).rank == 14])

    def is_straightflush(self):
        self.strength = max(8, self.strength)
        self.add_handtype(HandStrengths.STRAIGHT_FLUSH)
        return self.is_straight() and self.is_flush()

    def is_fourofakind(self):
        # Hist is 4 & 1
        self.strength = max(7, self.strength)
        self.add_handtype(HandStrengths.FOUR_OF_A_KIND)
        return 4 in Counter(self.rankings).values()

    def is_fullhouse(self):
        # Hist is 3 & 2
        self.strength = max(6, self.strength)
        self.add_handtype(HandStrengths.FULL_HOUSE)
        return (3 in Counter(self.rankings).values()) and (2 in Counter(self.rankings).values())

    def is_flush(self):
        self.strength = max(5, self.strength)
        self.add_handtype(HandStrengths.FLUSH)
        return 5 in Counter(self.suits).values()

    def is_straight(self):
        self.strength = max(4, self.strength)
        self.add_handtype(HandStrengths.STRAIGHT)
        return self.rankings == list(range(min(self.rankings), max(self.rankings)+1))

    def is_threeofakind(self):
        self.strength = max(3, self.strength)
        self.add_handtype(HandStrengths.THREE_OF_A_KIND)
        return 3 in Counter(self.rankings).values()
    
    def is_twopair(self):
        self.strength = max(2, self.strength)
        self.add_handtype(HandStrengths.TWO_PAIR)
        return 2 in Counter(Counter(self.rankings).values())
    
    def is_pair(self):
        self.strength = max(1, self.strength)
        self.add_handtype(HandStrengths.PAIR)
        return 2 in Counter(self.rankings).values()
    
    def add_handtype(self, handstrength):
        # Use in each evaluation check
        self.types[handstrength.name].append(self.cards)



class HandSpace:
    # Handspace is the entire set of community cards plus holecards (max 7 in NLHE)
    def __init__(self, holecards: list, community_cards: list):
        self.holecards = holecards
        self.community_cards = community_cards
        self.space = sorted(self.holecards + self.community_cards)
    
    # def get_draws(self):
    #     pass
    
    # def get_backdoor_draws(self):
    #     pass
    
    # def get_madehands(self):
    #     pass
    
    def getcombos(self, k=None):
        # Gets all combinations in hand space
        if k is None:
            k = 5 if len(self.space) > 5 else len(self.space)
        
        n = len(self.holecards) + len(self.community_cards)
        if k > n:
            raise ValueError(f"Tried to get {k} combinations from a space of {n}")
        return list(combinations(self.space, k))


if __name__ == '__main__':
    # Seed 20, 39 contains flush on iterations 12,11
    # Seed 13 contains a straight at iteration 0
    # Seed 24 contains 3-of-a-kind
    random.seed(24) # for repeatability
    deck = Deck()
    deck.shuffle()

    hole = deck.take(names=['As', 'Ks'])
    community = deck.take(names=['Qs', 'Js', 'Ts', '4c', '2d'])
    
    hs = HandSpace(hole, community)
    
    results = []
    for i, combo in enumerate(hs.getcombos()):
        hand = Hand(combo)
        print(f"Iteration {i}\t{hand}\tStarting strength: {hand.strength}")
        cnt = Counter(hand.rankings)
        
        if hand.is_royalflush():
            print(f"Found royal flush on iteration {i}: ", hand, hand.strength)
            results.append((i, hand.strength))
        
        elif hand.is_straightflush():
            print(f"Found straigth flush on iteration {i}: ", hand, hand.strength)
            results.append((i, hand.strength))
        
        elif hand.is_fourofakind():
            print(f"Found quads on iteration {i}: ", hand, hand.strength)
            results.append((i, hand.strength))
        
        elif hand.is_fullhouse():
            print(f"Found full house on iteration {i}: ", hand, hand.strength)
            results.append((i, hand.strength))

        elif hand.is_flush():
            print(f"Found flush on iteration {i}: ", hand, hand.strength)
            results.append((i, hand.strength))

        elif hand.is_straight():
            print(f"Found straight on iteration {i}: ", hand, hand.strength)
            results.append((i, hand.strength))
        
        elif hand.is_threeofakind():
            print(f"Found three of a kind in iteration {i}:", hand, hand.strength)
            results.append((i, hand.strength))
        
        elif hand.is_twopair():
            print(f"Found 2-pair on iteration {i}:", hand, hand.strength)
            results.append((i, hand.strength))

        elif hand.is_pair():
            print(f"Found pair on iteration {i}:", hand, hand.strength)
            results.append((i, hand.strength))
        else:
            print(f"No made hand (high card) on iteration {i}:", hand, hand.strength)
            results.append((i, 0))
        print()
    
    
    