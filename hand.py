from enums import Rank, Suit, HandStrength

# These might be nice as staticmethods for the Hand class
# Might require passing in a hand object instead of x because x is different for different funcs.
# Can then go hand.rankhist or hand.rankings or hand.suithist as needed.
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
    return is_straight(rankhist) and is_flush(suithist)


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
        - After tanking, hand needs to be represented as e.g. Twos full of Nines
    """
    pass


class HandSpace:
    pass

