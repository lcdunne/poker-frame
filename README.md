# pokerpy

First attempt at a poker hand simulator. Currently capable of creating a hand and ranking it from among the available 5-card hands in Texas hold 'em Poker.

Simulation ran for 10m hands appears to match expected probabilities of each hand:
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
- Major improvements

## DOING:

- Write tests

## DONE:

- Clearing up