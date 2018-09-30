from poker.tools import Series, Clock
import poker.poker as pkr

game = pkr.Game()
n_players = 8
for i in range(n_players):
    game.add_player()
player_1 = game.players[0]

cards_to_test = pkr.Deck.standard_52_card_deck()[:26]

hands_earnings = {}
n_stories = 1600
count = 0
for c1 in cards_to_test[:13]:
    for c2 in cards_to_test:
        if c2.value < c1.value or c1 is c2:
            continue
        earnings = []
        for i in range(n_stories):
            game.reset(shuffle_deck=True)
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
        # saving everything but the n_stories values of earnings (to save memory)
        assert hand_description not in hands_earnings.keys()
        hands_earnings[hand_description] = {"mean": earnings_series.mean, "std": earnings_series.standard_deviation,
                                            "I": earnings_series.confidence_range}
        Clock.elapsed()
        count += 1
        print("{}/169".format(count))

assert len(hands_earnings) == 169
hands_ranking = [(key, value["mean"], value["I"]) for key, value in hands_earnings.items()]
hands_ranking.sort(key=lambda x: x[1], reverse=True)  # sorting by descending mean average earnings
for hand_stats in hands_ranking:
    print(hand_stats)
