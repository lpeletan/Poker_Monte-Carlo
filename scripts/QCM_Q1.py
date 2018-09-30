from poker.tools import Series
from poker.tools import Clock
import poker.poker as pkr

game = pkr.Game()
game.add_player()
game.add_player()
game.add_player()
player_1 = game.players[0]
player_2 = game.players[1]
player_3 = game.players[2]

Clock.elapsed()
results = []
n_stories = 100000
for i in range(n_stories):
    game.reset()
    game.deal_card_to_player(player_1, "As")
    game.deal_card_to_player(player_1, "Ks")

    game.deal_card_to_player(player_2, "9d")
    game.deal_card_to_player(player_2, "9c")

    game.deal_card_to_player(player_3)
    game.deal_card_to_player(player_3)

    game.deal_flop()
    game.deal_turn()
    game.deal_river()

    winning_players = game.get_winning_players()
    assert winning_players  # asserts that the list is not empty

    if player_1 not in winning_players:
        results.append(2)
    elif len(winning_players) >= 2:
        results.append(0)
    else:
        results.append(1)

win_series = Series([res == 1 for res in results])
lose_series = Series([res == 2 for res in results])
tie_series = Series([res == 0 for res in results])
series_dic = {"Win": win_series, "Lose": lose_series, "Tie": tie_series}
Clock.elapsed()

for name, series in series_dic.items():
    print(name)
    print(series)
    print()
