import unittest
from deck import Deck
from enums import Suit, get_all_handlabels

class TestDeck(unittest.TestCase):
    
    def test_shuffle(self):
        deck = Deck()
        firstcard = deck[0]
        deck.shuffle()
        self.assertNotEqual(firstcard, deck[0])
    
    def test_has(self):
        deck = Deck()
        for label in get_all_handlabels():
            self.assertTrue( deck.has(label) )
    
    def test_take_n(self):
        deck = Deck()
        lendeck_start = len(deck) # just in case shorter decks are implemented
        
        n_to_take = 13
        
        deck.take(n_to_take)
        self.assertLess(len(deck), lendeck_start)
        self.assertEqual(len(deck), lendeck_start-n_to_take)
    
    def test_take_all_labels(self):
        deck = Deck()
        all_handlabels = get_all_handlabels()
        
        self.assertEqual(len(deck), len(all_handlabels))
        
        # Take all cards from deck
        taken = deck.take(labels=all_handlabels)
        self.assertEqual(len(deck), 0)
        self.assertEqual(len(taken), len(all_handlabels))
        self.assertTrue( all([t.label in all_handlabels for t in taken]) )
    
    def test_take_specific_labels(self):
        deck = Deck()
        handlabels = ['Ks', 'Qs', 'Js', 'Ts', '9s']
        
        # Take the labels
        taken = deck.take(labels=handlabels)
        for handlabel in handlabels:
            # Make sure they the deck no longer has them
            self.assertFalse( deck.has(handlabel) )
            # Make sure the list of taken cards does have them
            self.assertTrue( handlabel in [t.label for t in taken] )
    
    def test_take_all_by_n(self):
        deck = Deck()

        starting_length = len(deck)
        n = starting_length
        
        taken = deck.take(n)
        self.assertEqual(len(deck), starting_length-n)
        self.assertEqual(len(taken), n)
    
    def test_take_some_by_n(self):
        deck = Deck()

        starting_length = len(deck)
        n = 21
        
        taken = deck.take(n)
        self.assertEqual(len(deck), starting_length-n)
        self.assertEqual(len(taken), n)
    
    def test_take_by_lambda(self):
        
        lambdas = [
            lambda x: x.suit == Suit.SPADES.name, # all spades
            lambda x: x.rank < 8, # cards with rank below 8
            lambda x: x.rank == 14, # all aces
            lambda x: x.rank > 10, # all court cards
            lambda x: x.label in ['As', 'Ts', '4c', 'Jh'], # some random selection
            lambda x: x.label in ['i am not in the deck', 'haha', 'joker']
            
        ]
        
        for lambda_ in lambdas:
            deck = Deck()
            starting_length = len(deck)
            
            # Get the labels in a list
            labels = [card.label for card in deck._search(lambda_)]
                    
            taken = deck.take(lambda_=lambda_)
            
            self.assertEqual( len(taken), len(labels) )
            self.assertEqual( len(deck), starting_length - len(taken) )
            
            for card in taken:
                self.assertTrue( card.label in labels ) # contained in labels?
                self.assertFalse( deck.has( card.label ) ) # no longer in deck?


if __name__ == '__main__':
    unittest.main()