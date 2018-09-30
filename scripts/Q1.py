import math
import itertools
import poker.poker as pkr
from poker.tools import Clock

deck = pkr.Deck.standard_32_card_deck()
# deck = pkr.Deck.standard_52_card_deck()
n_drawn_cards = 5
# n_drawn_cards = 7

n_cards = len(deck)
print("The deck has {} cards.".format(n_cards))

n_combi = int(math.factorial(n_cards) / (math.factorial(n_drawn_cards) * math.factorial(n_cards - n_drawn_cards)))
print("{} combinations of {} cards among {} cards.".format(n_combi, n_drawn_cards, n_cards))

# generating combinations
Clock.elapsed()  # prints the elapsed time as a reference
best_hands = []
# exhaustive search
for i, cards in enumerate(itertools.combinations(deck, n_drawn_cards)):  # iterates through all the combinations
    best_hand = pkr.Hand.best_from_cards(cards)
    best_hands.append(best_hand)
    if i % (n_combi//100) == 0:
        print("simulation progress: {:.1%}".format(i / n_combi))
print("{} combinations evaluated".format(len(best_hands)))
Clock.elapsed()  # prints the elapsed time since the last call to Clock.elapsed()

# counting the results
combination_count = {}
for hand in best_hands:
    name = hand.name
    combination_count[name] = combination_count.get(name, 0) + 1

# counting percentages
n_total = len(best_hands)
combination_ratios = {name: v/n_total for name, v in combination_count.items()}
sum_ratios = sum(v for v in combination_ratios.values())
assert abs(1 - sum_ratios) < 1e-6  # checking that the sum of probabilities is close to 1.

print(combination_count)
print(combination_ratios)
