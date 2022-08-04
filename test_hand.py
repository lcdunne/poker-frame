import unittest
import random
from enums import HandStrength
from hand import Hand

random.seed(21)

class TestHand(unittest.TestCase):
    
    def setUp(self):
        # All hands (values) should have strength equal to the keys
        self.example_hands = {
            HandStrength.STRAIGHT_FLUSH.name: Hand(['Jh', '9h', 'Qh', '8h', 'Th']),
            HandStrength.FOUR_OF_A_KIND.name: Hand(['Qc','6d', '6c',  '6h', '6s']),
            HandStrength.FULL_HOUSE.name: Hand(['2h', '9s', '2c', '2d', '9h']),
            HandStrength.FLUSH.name: Hand(['6d', '3d', 'Ad', 'Jd', '9d']),
            HandStrength.STRAIGHT.name: Hand(['7d', '9d', '5h', '8d', '6c']),
            HandStrength.THREE_OF_A_KIND.name: Hand(['Qc', '6d', 'Ah', '6h', '6s']),
            HandStrength.TWO_PAIR.name: Hand(['2d', 'Ks', '9c', '9h', '2h']),
            HandStrength.PAIR.name: Hand(['3h', '3c', '6s', 'Td', 'Jh']),
            HandStrength.HIGH_CARD.name: Hand(['3h', '2c', '6s', 'Td', 'Jh']),
        }
        
        # All should evaluate to HIGH_CARD
        self.example_nonhands = [Hand(labels=h.labels[:-1]) for h in self.example_hands.values()]
        
        # Manually input orderings for each hand in example_hands
        self.orderings = {
            HandStrength.STRAIGHT_FLUSH.name: [12, 11, 10, 9, 8],
            HandStrength.FOUR_OF_A_KIND.name: [6, 6, 6, 6, 12],
            HandStrength.FULL_HOUSE.name: [2, 2, 2, 9, 9],
            HandStrength.FLUSH.name: [14, 11, 9, 6, 3],
            HandStrength.STRAIGHT.name: [9, 8, 7, 6, 5],
            HandStrength.THREE_OF_A_KIND.name: [6, 6, 6, 14, 12],
            HandStrength.TWO_PAIR.name: [9, 9, 2, 2, 13],
            HandStrength.PAIR.name: [3, 3, 11, 10, 6],
            HandStrength.HIGH_CARD.name:[11, 10, 6, 3, 2],
        }
        
        # Some edge case hands that could be tricker comparisons
        self.better = [
            Hand(['2d', '6s', '9c', '9h', '2h']), # 2 pair, nines and twos with 6 kicker
            Hand(['Jh', 'Jd', 'Jc', 'Qs', '5h']), # Trip jacks with Q-5 kickers
            Hand(['Kc', 'Ks', 'Ad', '6c', '2h']), # TPTK
        ]
        
        self.worse = [
            Hand(['4s', '8c', '4h', '8d', 'Kh']), # 2 pair, eights and fours with k kicker
            Hand(['Jh', 'Jd', 'Jc', 'Qs', '4h']), # Trip jacks with Q-6 kickers
            Hand(['Kd', 'Kh', 'Qd', '6c', '2h']), # TPGK (but not good enough)
        ]
    
    def shuffle_hand_cards(self, hand):
        labels = hand.labels
        random.shuffle(labels)
        return Hand(labels)
    
    def test_made_hands(self):
        for strength, hand in self.example_hands.items():
            self.assertEqual(strength, hand.strength)
    
    def test_non_made_hands(self):
        for hand in self.example_nonhands:
            self.assertEqual(hand.strength, HandStrength.HIGH_CARD.name)
    
    def test_correct_ordering(self):
        for strength, hand in self.example_hands.items():
            self.assertEqual([c.rank for c in hand], self.orderings[strength])
    
    def test_comparisons(self):
        gt = list(self.example_hands.values())
        lt = list(self.example_hands.values())[1:]
        lt.append( Hand( ['7h', '5h', '4c', '3d', '2c'] ) )
        for g, l in zip(gt, lt):
            
            self.assertGreater(g, l)
            self.assertGreaterEqual(g, self.shuffle_hand_cards(g))
            self.assertGreaterEqual(g, self.shuffle_hand_cards(l))
            self.assertGreaterEqual(l, self.shuffle_hand_cards(l))

            self.assertLess(l, g)
            self.assertLessEqual(g, self.shuffle_hand_cards(g))
            self.assertLessEqual(l, self.shuffle_hand_cards(l))
            self.assertLessEqual(l, self.shuffle_hand_cards(g))
            
            self.assertNotEqual(l, g)
        
        for good, bad in zip(self.better, self.worse):
            self.assertGreater(good, bad)
        
    
if __name__ == '__main__':
    unittest.main()