from card import Hand, HandStrengths

# 1. Royal Flush of Parsley
rf = Hand(names=['Ac', 'Kc', 'Qc', 'Jc', 'Tc'])
# 2. Straight Flush
sf = Hand(names=['Qh', 'Jh', 'Th', '9h', '8h'])
# 3. Quads
quads = Hand(names=['Kh', 'Ks', 'Qh', 'Kd', 'Kc'])
# 4. Full house
fh = Hand(names=['Js', 'Jd', 'Jc', 'Ts', 'Th'])
# 5. Flush
flush = Hand(names=['Kh', '7h', '6h', '3h', '2h'])
# 6. Straight
st = Hand(names=['Th', '9h', '8s', '7d', '6h'])
# 7. Trips
trps = Hand(names=['8h', '8d', '8s', 'Qc', 'Ks'])
# 8. 2-Pair
tpr = Hand(names=['8h', '8d', '7s', '7c', 'Ks'])
# 9. Pair
pr = Hand(names=['Ah', 'Ad', '8s', 'Qc', 'Ks'])
# 10. High Card
hc = Hand(names=['Ah', 'Jd', '8s', 'Qc', '2s'])


hands = [rf, sf, quads, fh, flush, st, trps, tpr, pr, hc]
for hand, hstrn in zip(hands, HandStrengths.values()[::-1]):
    print(hand, hstrn)
    assert hand.strength == HandStrengths(hstrn).name, f"Got {hand.strength}, expected {HandStrengths(hstrn).name}"

# Check hand comparisons between ranks
assert rf > sf > quads > fh > flush > st > trps > tpr > pr > hc

# Check hand comparisons within ranks