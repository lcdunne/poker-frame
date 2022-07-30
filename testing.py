from card import *



royal_flushes = [
    [('As', 'Ks'), ('Qs', 'Js', 'Ts')],
]

straight_flushes = [
    [('Kh', 'Qh'), ('Jh', 'Th', '9h')],
    [('Qh', 'Jh'), ('Th', '9h', '8h')],
    [('Jh', 'Th'), ('9h', '8h', '7h')],
    [('Th', '9h'), ('8h', '7h', '6h')],
    
]

for handcards in straight_flushes:
    deck = Deck()
    hole = deck.take(names=list(handcards[0]))
    community = deck.take(names=list(handcards[1]))