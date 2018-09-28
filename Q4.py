from tools import Series, Clock
import poker as pkr

game = pkr.Game()  # creates a game with a board and a 52 card deck (but no player)
# adding two players
game.add_player()
game.add_player()
player_1 = game.players[0]
player_2 = game.players[1]

Clock.elapsed()
# Monte Carlo
results = []
n_stories = 100000
for i in range(n_stories):
    game.reset(shuffle_deck=True)
    game.deal_card_to_player(player_1, "9s")  # always dealing the same cards to player 1.
    game.deal_card_to_player(player_1, "8s")

    game.deal_card_to_player(player_2)  # player 2 receives cards at random.
    game.deal_card_to_player(player_2)

    game.deal_flop()
    game.deal_turn()
    game.deal_river()

    # print(game)  # <- uncomment these two lines if you want a visualization of what is happening during the simulation
    # print()

    winning_players = game.get_winning_players()
    assert winning_players  # asserts that the list is not empty

    if len(winning_players) == 2:  # <- this is a tie
        results.append(0)
    elif winning_players[0] is player_1:  # <- this is a win
        results.append(1)
    else:  # <- this is a lose
        results.append(2)

# processing the results
win_series = Series([res == 1 for res in results])
lose_series = Series([res == 2 for res in results])
tie_series = Series([res == 0 for res in results])
series_dic = {"Win": win_series, "Lose": lose_series, "Tie": tie_series}
Clock.elapsed()

# displaying the results
for name, series in series_dic.items():
    print(name)
    print(series)
    print()
