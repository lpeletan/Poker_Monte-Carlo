from tools import Series, Clock
import poker as pkr

game = pkr.Game()
n_players = 2
for i in range(n_players):
    game.add_player()
player_1 = game.players[0]

deck = pkr.Deck.standard_52_card_deck(False)
couples_to_test = [(deck["As"], deck["Ad"]),
                   (deck["Ks"], deck["Kd"]),
                   (deck["Qs"], deck["Qd"]),
                   (deck["Js"], deck["Jd"]),
                   (deck["Ts"], deck["Td"]),
                   (deck["9s"], deck["9d"]),
                   (deck["8s"], deck["8d"]),
                   (deck["7s"], deck["7d"]),
                   (deck["6s"], deck["6d"]),
                   (deck["As"], deck["Jd"]),
                   (deck["As"], deck["Js"]),
                   (deck["As"], deck["Ks"]),
                   (deck["As"], deck["Td"]),
                   (deck["Qs"], deck["Kd"]),
                   (deck["As"], deck["Kd"]),
                   (deck["As"], deck["Ts"]),
                   (deck["As"], deck["7s"]),
                   (deck["As"], deck["8s"]),
                   (deck["As"], deck["Qs"]),
                   (deck["Ks"], deck["Js"]),
                   (deck["As"], deck["Qd"]),
                   (deck["As"], deck["9s"]),
                   (deck["As"], deck["5d"]),
                   (deck["Js"], deck["Qs"]),
                   ]

hand_values = {}
n_stories = 1600*100
count = 0
for c1, c2 in couples_to_test:
    earnings = []
    for i in range(n_stories):
        game.reset()
        game.deal_card_to_player(player_1, str(c1))
        game.deal_card_to_player(player_1, str(c2))

        for player in game.players[1:]:
            game.deal_card_to_player(player)
            game.deal_card_to_player(player)

        game.deal_flop()
        game.deal_turn()
        game.deal_river()

        winning_players = game.get_winning_players()

        earning = n_players / len(winning_players) * (player_1 in winning_players) - 1
        earnings.append(earning)

    earnings_series = Series(earnings)
    if c1.value >= c2.value:
        hand_description = c1.short_rank + c2.short_rank
    else:
        hand_description = c2.short_rank + c1.short_rank
    if c1.short_rank != c2.short_rank:
        hand_description += "o" if c1.suit != c2.suit else "s"
    hand_values[hand_description] = {"mean": earnings_series.mean, "std": earnings_series.standard_deviation,
                                     "I": earnings_series.confidence_range}
    Clock.elapsed()
    count += 1
    print("{}/{}".format(count, len(couples_to_test)))

assert len(hand_values) == len(couples_to_test)
hands_ranking = [(key, value["mean"], value["I"]) for key, value in hand_values.items()]
hands_ranking.sort(key=lambda x: x[1], reverse=True)
for hand in hands_ranking:
    print(hand)
