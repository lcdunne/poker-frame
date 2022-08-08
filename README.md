# poker-frame

First attempt at a poker hand simulator. Currently capable of creating a hand and ranking it from among the available 5-card hands in Texas hold 'em Poker.

## Examples

```python
>>> from card import *

>>> deck = Deck()

>>> hand = Hand(deck.take(5))

>>> print(hand)
Hand: ROYAL_FLUSH (As,Ks,Qs,Js,Ts)
```

To shuffle the deck before drawing a hand:

```python
>>> deck.shuffle()

>>> hand = Hand(deck.take(5))

>>> print(hand)
Hand: PAIR (Ac,9s,6c,2s,Ah)
```

We can also create specific hands from a list of hand labels like `['As', 'Ks', 'Qs', 'Js', 'Ts']`, and different hands can be directly compared based on their strength:

```python
>>> deck = Deck()

>>> hand_1 = Hand(names=['Js', 'Ts', '9s', '8s', '7s'])

>>> hand_2 = Hand(names=['9h', '9d', '9s', '9c', '2h'])

>>> print(hand_1)
Hand: STRAIGHT_FLUSH (Js,Ts,9s,8s,7s)

>>> print(hand_2)
Hand: FOUR_OF_A_KIND (9h,9d,9s,9c,2h)

>>> hand_1 > hand_2
```

## A Simulation

The idea was to take the known probabilities for each made hand ([see here](https://en.wikipedia.org/wiki/Texas_hold_%27em)), simulate a large number of 5-card hand deals, and see the resulting distribution of hand strengths to compare with those that would be expected.

The simulation ran 10m hands and appeared to match the expected probabilities of each hand:
<img src="https://github.com/lcdunne/pokerpy/raw/main/2022-08-01T1544_simulation-results.png" alt="" width="620">

Simulation results table:

| Hand                                                | Probability | Observed | Expected |
| --------------------------------------------------- | ----------- | -------- | -------- |
| Royal flush                                         | 1.54E-06    | 30       | 15.4     |
| Straight flush (excluding royal flush)              | 1.39E-05    | 136      | 139      |
| Four of a kind                                      | 0.00024     | 2373     | 2401     |
| Full house                                          | 0.001441    | 14415    | 14410    |
| Flush (excluding royal flush and straight flush)    | 0.001965    | 19656    | 19650    |
| Straight (excluding royal flush and straight flush) | 0.003925    | 39504    | 39250    |
| Three of a kind                                     | 0.021128    | 210887   | 211280   |
| Two pair                                            | 0.047539    | 475259   | 475390   |
| One pair                                            | 0.422569    | 4224349  | 4225690  |
| No pair / High card                                 | 0.501177    | 5013391  | 5011770  |

## TODO:

- Create main unittests
- Break up into modules
- Major improvements:
  - Extract all hand evaluation methods and create new HandEvaluator class (?) to handle this (or just a module of functions)
  - Make sure HIGH_CARD is not considered a made hand
  - 

## DOING:

- Write tests
- Decide between `.label` or `.name` for refs like `'Ts', 'Jh', 'Qc', ...`. The problem with name is that it interfered with enums.

## DONE:

- Clearing up