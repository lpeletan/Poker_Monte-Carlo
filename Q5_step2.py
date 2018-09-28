from tools import Series, Clock
import poker as pkr

game = pkr.Game()
n_players = 8
for i in range(n_players):
    game.add_player()
player_1 = game.players[0]

deck = pkr.Deck.standard_52_card_deck(False)
# these hands are chosen from the results of Q5_step1
hands_to_test = [
                   (deck["As"], deck["Ad"]),
                   (deck["Ks"], deck["Kd"]),
                   (deck["Qs"], deck["Qd"]),
                   (deck["Js"], deck["Jd"]),
                   (deck["Ts"], deck["Td"]),
                   (deck["As"], deck["Ks"]),
                   (deck["As"], deck["Qs"]),
                   (deck["As"], deck["Js"]),
                   (deck["As"], deck["Ts"]),
                   (deck["As"], deck["Kd"]),
                   (deck["As"], deck["Qd"]),
                   (deck["As"], deck["Jd"]),
                   (deck["Ks"], deck["Qs"]),
                   (deck["Ks"], deck["Js"]),
                   (deck["Qs"], deck["Js"]),
                   (deck["Js"], deck["Ts"]),
                   ]

hands_earnings = {}
n_stories = 1600*100  # simulating 100x more stories that in step 1 (95% confidence range is 10x more accurate)
count = 0
for c1, c2 in hands_to_test:
    earnings = []
    for i in range(n_stories):
        game.reset(True)
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
    assert hand_description not in hands_earnings.keys()
    hands_earnings[hand_description] = {"mean": earnings_series.mean, "std": earnings_series.standard_deviation,
                                        "I": earnings_series.confidence_range}
    Clock.elapsed()
    count += 1
    print("{}/{}".format(count, len(hands_to_test)))

assert len(hands_earnings) == len(hands_to_test)
hands_ranking = [(key, value["mean"], value["I"]) for key, value in hands_earnings.items()]
hands_ranking.sort(key=lambda x: x[1], reverse=True)  # sorting by descending mean average earnings
for hand_stats in hands_ranking:
    print(hand_stats)
