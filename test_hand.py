import unittest
from enums import HandStrength, get_ranks_and_suits, get_all_handlabels
from hand import Hand


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
        
        
    
    def tearDown(self):
        pass
    
    def test_made_hands(self):
        for strength, hand in self.example_hands.items():
            self.assertEqual(strength, hand.strength)
    
    def test_non_made_hands(self):
        for hand in self.example_nonhands:
            self.assertEqual(hand.strength, HandStrength.HIGH_CARD.name)
    
    def test_correct_ordering(self):
        for strength, hand in self.example_hands.items():
            self.assertEqual([c.rank for c in hand], self.orderings[strength])
        
    
if __name__ == '__main__':
    unittest.main()