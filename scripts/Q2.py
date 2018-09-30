import math
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

Clock.elapsed()
n_tries = 100
n_success = 0
n_stories = 40000
for k in range(n_tries):
    # Monte Carlo
    best_hands = []
    for i in range(n_stories):
        deck.shuffle()
        best_hand = pkr.Hand.best_from_cards(deck[:n_drawn_cards])
        best_hands.append(best_hand)
    Clock.elapsed()

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
    n_success += 1 if 0.52893 < combination_ratios["Pair"] < 0.53893 else 0

# printing the number of times that the estimated probability of a pair was in the interval [0.52893, 0.53893]
print("n_tries =", n_tries)
print("n_success =", n_success)
print('success ratio = {:%}'.format(n_success/n_tries))  # <- expected to be in the range [0.91, 0.99]
