import poker.poker as p

d = p.Deck.standard_52_card_deck()
print(d)
for c in d:
    print(repr(c), c)


h = p.Hand([d['2c']])

print(h._strength)
print(h.strength)

# h = p.Hand.best_from_cards(d.cards)
# print(h)
