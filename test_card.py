import unittest
from enums import Rank, Suit, get_ranks_and_suits, get_all_handlabels
from card import Card

class TestCard(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    
    def test_card_labels_by_ranksuit(self):
        # Loop over all ranks and suits and test that labels are as expected.
        for rank, suit in get_ranks_and_suits():
            card = Card( rank=rank, suit=suit )
            q = Rank(rank).label + Suit[suit].value
            self.assertEqual( card.label, q )
    
    def test_card_label(self):
        # Loop over all combinations of rank and suit
        for rank, suit in get_ranks_and_suits():
            label_ = Rank(rank).label + Suit[suit].value
            for label in [
                    label_, # Normal, like Qd
                    label_[0].lower() + label_[1].upper(), # Abnormal, like qD
                    label_.upper() # Abnormal, like QD
                ]:
                
                card = Card( label )
            
                # Test that rank and suit are correctly generated from label
                self.assertEqual( card.rank, rank )
                self.assertEqual( card.suit, suit )
                
                # Test that despite weird input, the label gets set nicely
                self.assertEqual( card.label, label_ )
    
    def test_card_label_precedence(self):
        # Test that providing a card label takes precedence over rank and suit args.
        handlabels = get_all_handlabels()[::-1] # reversed for a different order.
        ranks_suits = get_ranks_and_suits()
        
        for label, ranksuit in zip(handlabels, ranks_suits):
            rank, suit = ranksuit[0], ranksuit[1]
            
            # Ignore if rank or suit matches current iteration's one
            if (Rank.get(label[0]).value == rank) or (Suit[suit].value == suit):
                continue

            card = Card( label, rank=rank, suit=suit)
            self.assertEqual(card.label, label) # label not overwritten by rank
            self.assertNotEqual(card.rank, rank) # card rank based on LABEL and not `rank`
            self.assertNotEqual(card.suit, suit) # card suit based on LABEL and not `suit`
        
    def test_inadequate_input(self):
        # Test that giving just a rank or just a suit to Card throws a ValueError
        # Just the rank
        with self.assertRaises(ValueError):
            Card(rank=Rank.TEN.value)
        # Just the suit
        with self.assertRaises(ValueError):
            Card(suit=Rank.TEN.value)
    
    def test_card_comparisons(self):
        ranks = Rank.values()[::-1]        
        for suit in Suit.items():
            for i, rank in enumerate(ranks):
                card_smaller = Card(rank=rank, suit=suit)
                self.assertEqual(card_smaller, Card(rank=rank, suit=suit))
                if i == 0:
                    continue
            
                card_bigger = Card(rank=ranks[i-1], suit=suit)
                self.assertLess(card_smaller, card_bigger)


if __name__ == '__main__':
    unittest.main()