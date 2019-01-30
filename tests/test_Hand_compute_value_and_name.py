import poker.poker as p

deck = p.Deck.standard_52_card_deck(False)

cards = [deck["5C"], deck["6C"], deck["7C"], deck["8C"], deck["9C"]]
hand = p.Hand(cards)
print(hand, "(should be: 5C 6C 7C 8C 9C, Straight flush, strength=80900000000)")

cards = [deck["TC"], deck["JC"], deck["AC"], deck["KC"], deck["QC"]]
hand = p.Hand(cards)
print(hand, "(should be: Royal Straight flush, strength=81400000000)")

cards = [deck["5C"], deck["2C"], deck["3C"], deck["AC"], deck["4C"]]
hand = p.Hand(cards)
print(hand, "(should be: Straight flush, strength=80500000000)")


cards = [deck["5C"], deck["5D"], deck["5H"], deck["5S"], deck["AC"]]
hand1 = p.Hand(cards)
print(hand1, "(should be: 5C 5D 5H 5S AC, Four of a kind, strength=70514000000)")


cards = [deck["TC"], deck["TD"], deck["TH"], deck["JH"], deck["JC"]]
hand2 = p.Hand(cards)
print(hand2, "(should be: TC TD TH JH JC, Full house, strength=61011000000)")

cards = [deck["TS"], deck["TC"], deck["TD"], deck["JS"], deck["JH"]]
hand3 = p.Hand(cards)
print(hand3, "(should be: TS TC TD JS JH, Full house, strength=61011000000)")

print(hand3 > hand2)
print(hand3 >= hand2)
print(hand3 < hand2)
print(hand3 <= hand2)
print(hand3 == hand2)
print(hand3 != hand2)


cards = [deck["QS"], deck["7S"], deck["4S"], deck["TS"], deck["8S"]]
hand.cards = cards
print(hand, "(should be: QS 7S 4S TS 8S, Flush, strength=51210080704)")


cards = [deck["JS"], deck["TC"], deck["7H"], deck["8H"], deck["9H"]]
hand.cards = cards
print(hand, "(should be: JS TC 7H 8H 9H, Straight, strength=41100000000)")


cards = [deck["5S"], deck["5C"], deck["5H"], deck["KH"], deck["3D"]]
hand.cards = cards
print(hand, "(should be: Three of a kind, strength=30513030000)")


cards = [deck["2S"], deck["2C"], deck["JH"], deck["JS"], deck["TD"]]
hand.cards = cards
print(hand, "(should be: Two pairs, strength=21102100000)")

cards = [deck["AS"], deck["AC"], deck["JH"], deck["9S"], deck["TD"]]
hand.cards = cards
print(hand, "(should be: Pair, strength=11411100900)")

cards = [deck["7S"], deck["AC"], deck["JH"], deck["9S"], deck["TD"]]
hand.cards = cards
print(hand, "(should be: High card, strength=1411100907)")

cards = []
hand.cards = cards
print(hand, "(should be: Nothing, strength=0)")
