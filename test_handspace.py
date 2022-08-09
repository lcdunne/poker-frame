import unittest
import random
from enums import HandStrength
from hand import Card, Hand, HandSpace

random.seed(21)

class TestHandSpace(unittest.TestCase):
    def setUp(self):
        self.example_spaces = [
            {
                'holecards': ['Kh', 'Ah'],
                'community_cards': ['Jh', '9h', 'Qh', '8h', 'Th'],
                'target': Hand(['Ah', 'Kh', 'Qh', 'Jh', 'Th']),
                'using': 2,
            }, # But a  K-9 straight flush is possible
            {
                'holecards': ['7h', '5h'],
                'community_cards': ['6h', '9h', '2h', '8h', '4h'],
                'target': Hand(['9h', '8h', '7h', '6h', '5h']),
                'using': 2,
            }, # But a  8-4 straight flush is possible
            {
                'holecards': ['7h', '7c'],
                'community_cards': ['7d', '7s', '2h', '2d', '2c'],
                'target': Hand(['7h', '7c', '7d', '7s', '2h']),
                'using': 2,
            }, # But a full house is possible
            {
                'holecards': ['7h', '5h'],
                'community_cards': ['7d', '7c', '5s', '2h', '2c', '2s'],
                'target': Hand(['7h', '7d', '7c', '5h', '5s']),
                'using': 2,
            }, # 7s full of 5s, but 2s full of 7s/2s full of 5s is also possible.
            {
                'holecards': ['7h', '8h'],
                'community_cards': ['Jh', '5c', '6s', '2h', '4h', '2s'],
                'target': Hand(['Jh', '8h', '7h', '4h', '2h']),
                'using': 2,
            }, # J-high flush but a 8-4 straight is possible.
            {
                'holecards': ['7h', '8h'],
                'community_cards': ['Kd', '7d', 'Jd', '2d', '7c', '3d'],
                'target': Hand(['Kd', 'Jd', '7d', '3d', '2d']),
                'using': 0,
            }, # Trips but the flush is on the board
            
        ]
    
    def test_best_hand(self):
        for space in self.example_spaces:
            hs = HandSpace(
                hole_cards = [Card(lbl) for lbl in space['holecards']],
                community_cards = [Card(lbl) for lbl in space['community_cards']]
            )
            
            self.assertEqual(hs.best_hand, space['target'])

    
if __name__ == '__main__':
    unittest.main()