from itertools import product
import random
from enums import Rank, Suit
from card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(rank=r, suit=s) for r,s in product(Rank.values(), Suit.items())]
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
        random.shuffle(self.cards)
    
    def fan(self, n=5):
        # Like pandas.dataframe.head, only for playing cards
        return self[:n]
    
    def has(self, name):
        return name in [card.label for card in self]
    
    def take(self, n=None, names=None, lambda_=None):
        """Take cards from deck.
        
        Take any number of cards by `n`, based on their `names`, or based on a 
        lambda function. Note that this pops the cards from the deck, which 
        occurs in place - make sure to store the result.

        Parameters
        ----------
        n : int, optional
            Number of cards to take from the top of the deck. The default is 
            None.
        names : str or list, optional
            A list of card names, like ['Ts', 'Qc'] to take from the deck. The 
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
        if names is not None:
            if isinstance(names, str):
                names = [names]
            lambda_ = lambda x: x.label in names
        
        if lambda_ is not None:
            # Create a search list as a reference to extract from cards.
            searched = [i.label for i in self._search(lambda_) if i is not None]
            # Store cards to take
            taken = [c for c in self if c.label in searched]
            # Update original cards list  to reflect removal
            self.cards = [c for c in self if c.label not in searched]
            return taken
        
        if n is None:
            raise ValueError("Must specify either n, names, or lambda function.")
        return [self.cards.pop() for _ in range(n)]

if __name__ == '__main__':
    deck = Deck()
    print(deck[:8])
    print(len(deck))
    all_spades = deck._search(lambda x: x.suit == 'SPADES')
    print(f"All spades (n={len(all_spades)}):", all_spades)
