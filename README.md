# poker-frame

First attempt at a poker hand simulator. Currently capable of creating a hand and ranking it from among the available 5-card hands in Texas hold 'em Poker.

## Examples

```python
>>> from deck import Deck
>>> from hand import Hand

>>> deck = Deck()
>>> deck.fan()
[<Card('2c')>, <Card('2d')>, <Card('2h')>, <Card('2s')>, <Card('3c')>]

>>> hand = Hand(cards=deck.take(5))

>>> print(hand)
<Hand(['As', 'Ks', 'Qs', 'Js', 'Ts'])>
>>> print(hand.strength)
ROYAL_FLUSH
```

To shuffle the deck before drawing a hand:

```python
>>> deck.shuffle()

>>> hand = Hand(cards=deck.take(5))

>>> print(hand)
<Hand(['Tc', 'Td', 'Qh', '7d', '5d'])>

>>> print(hand.strength)
PAIR
```

We can also create specific hands from a list of hand labels like `['As', 'Ks', 'Qs', 'Js', 'Ts']`, and different hands can be directly compared based on their strength:

```python
>>> deck = Deck()

>>> hand_1 = Hand(['Js', 'Ts', '9s', '8s', '7s'])

>>> hand_2 = Hand(['9h', '9d', '9s', '9c', '2h'])

>>> print(hand_1, hand_1.strength)
<Hand(['Js', 'Ts', '9s', '8s', '7s'])> STRAIGHT_FLUSH

>>>print(hand_2, hand_2.strength)
<Hand(['9h', '9d', '9s', '9c', '2h'])> FOUR_OF_A_KIND)

>>> hand_1 > hand_2
True
```

## A Simulation

To test that the implementation is correct, I simulated a large number of 5-card hand deals to see the resulting distribution of hand strengths. This was then compared with those that would be expected by chance, based on their known probabilities of occurrence ([see here](https://en.wikipedia.org/wiki/Texas_hold_%27em)).

The simulation ran 10m hands and appeared to match the expected probabilities for each hand:
<img src="https://github.com/lcdunne/poker-frame/raw/main/2022-08-09T2120_simulation-results.png" alt="" width="620">

Simulation results table:

| Hand                                                | Probability | Observed | Expected |
|-----------------------------------------------------|-------------|----------|----------|
| Royal flush                                         | 1.54E-06    | 25       | 15.4     |
| Straight flush (excluding royal flush)              | 1.39E-05    | 128      | 139      |
| Four of a kind                                      | 0.0002401   | 2361     | 2401     |
| Full house                                          | 0.001441    | 14272    | 14410    |
| Flush (excluding royal flush and straight flush)    | 0.001965    | 19581    | 19650    |
| Straight (excluding royal flush and straight flush) | 0.003925    | 38988    | 39250    |
| Three of a kind                                     | 0.021128    | 211165   | 211280   |
| Two pair                                            | 0.047539    | 475173   | 475390   |
| One pair                                            | 0.422569    | 4226364  | 4225690  |
| No pair / High card                                 | 0.501177    | 5011943  | 5011770  |

## TODO:

## DOING:

## DONE: