from itertools import product
import random
from enums import Rank, Suit
from card import Card

class Deck:
    """A deck of playing cards.
    
    Each element is defined by the `Card` class. The deck is an iterable. Basic 
    methods are:
        `.shuffle` - shuffle the deck.
        `.fan` - view a small selection of the deck.
        `.has` - check if the deck contains a specific card.
        `.take` - take cards from the deck.
    
    
    """
    def __init__(self):
        self.cards = [
            Card(rank=r, suit=s) for r,s in product(Rank.values(), Suit.items())
        ]
        self._current_index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index >= len(self.cards):
            self._current_index = 0
            raise StopIteration

        self._current_index += 1
        return self.cards[self._current_index-1]
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, obj):
        return self.cards[obj]
    
    # def __repr__(self):
    #     return "Deck()"
    
    def __str__(self):
        return f"{self.cards}"
    
    def _search(self, lambda_=None):
        return list(filter(lambda_, self))
    
    def shuffle(self):
        """Shuffle the deck in place.

        Returns
        -------
        None

        """
        random.shuffle(self.cards)
    
    def fan(self, n=5):
        """See the first `n` cards

        Parameters
        ----------
        n : int, optional
            The number of cards to show. The default is 5.

        Returns
        -------
        list
            A list of `n` `Card` objects.

        """
        return self[:n] if n > 0 else self[n:]
    
    def has(self, label):
        """Check to see if a card label, is contained in the deck.

        Parameters
        ----------
        label : str
            A label like `Jd`, 'As', etc.

        Returns
        -------
        bool
            Whether the card denoted by the label exists in the deck or not.

        """
        return label in [card.label for card in self]
    
    def take(self, n=None, labels=None, lambda_=None):
        """Take cards from deck.
        
        Take any number of cards by `n`, based on their `labels`, or based on a 
        lambda function. Note that this pops the cards from the deck, which 
        occurs in place - make sure to store the result.

        Parameters
        ----------
        n : int, optional
            Number of cards to take from the top of the deck. The default is 
            None.
        labels : str or list, optional
            A list of card labels, like ['Ts', 'Qc'] to take from the deck. The 
            default is None.
        lambda_ : callable, optional
            A custom lambda function for the cards in the deck. The default is 
            None.

        Raises
        ------
        ValueError
            If no arguments are given.

        Returns
        -------
        list
            Cards that were taken from the deck.

        """
        if labels is not None:
            if isinstance(labels, str):
                labels = [labels]
            lambda_ = lambda x: x.label in labels
        
        if lambda_ is not None:
            # Create a search list as a reference to extract from cards.
            searched = [i.label for i in self._search(lambda_) if i is not None]
            
            # Store cards to take
            taken = [c for c in self if c.label in searched]
            
            # Update original cards list  to reflect removal
            self.cards = [c for c in self if c.label not in searched]
            
            return taken
        
        if n is None:
            raise ValueError("Must specify either n, labels, or lambda function.")
        return [self.cards.pop() for _ in range(n)]

if __name__ == '__main__':
    deck = Deck()
    print(deck[:8])
    print(len(deck))
    all_spades = deck._search(lambda x: x.suit == 'SPADES')
    print(f"All spades (n={len(all_spades)}):", all_spades)
