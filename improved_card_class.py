# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 18:54:17 2022

@author: L
"""

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

class Card:
    def __init__(self, label=None, rank: int=None, suit=None):
        # If rank & suit are provided they must be enums
        if label is not None:
            self._label = label
            # ensure correct label here (check all enum values)
            self._rank = Rank[RankName(self._label[0]).name]
            self._suit = Suit(self._label[1])
        else:
            # Ensure both rank & suit are given
            if not all([rank, suit]):
                raise ValueError("If label is not provided, both rank and suit must be provided (received None for both).")
            self._rank = Rank(rank)
            self._suit = Suit[suit]
            self._label = RankName[self._rank.name].value + self._suit.value
    
    def __repr__(self):
        return f"<Card('{self.label}')>"
    
    def __str__(self):
        return f"{self.rank.name.capitalize()} of {self.suit.name.capitalize()}"
    
    def __lt__(self, other):
        return self.rank < other.rank
    
    def __le__(self, other):
        return self.rank <= other.rank
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __ge__(self, other):
        return self.rank >= other.rank
    
    def __gt__(self, other):
        return self.rank > other.rank
    
    @property
    def rank(self):
        return self._rank
    
    @property
    def suit(self):
        return self._suit
    
    @property
    def label(self):
        return self._label
    