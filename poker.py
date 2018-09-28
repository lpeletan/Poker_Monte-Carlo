"""A simple Poker Texas Hold'em game simulator tool."""
import random
import itertools


class Card:
    rank_to_value = {str(i): i for i in range(2, 10 + 1)}
    rank_to_value.update({"Jack": 11, "Queen": 12, "King": 13, "Ace": 14})
    valid_ranks = list(rank_to_value.keys())  # acts as a whitelist
    valid_suits = ["Clubs", "Diamonds", "Hearts", "Spades"]  # acts as a whitelist

    def __init__(self, rank, suit):
        """
        Initializes an instance of Card. A card is defined by its rank and its suit.
        :param rank: string.
        The rank of the card (eg: "3", "Ten", "King").
        :param suit: string.
        The suit of the card (eg: "Hearts", "Diamonds").
        """
        assert rank in Card.valid_ranks  # limiting the card to the official rank whitelist
        assert suit in Card.valid_suits  # limiting the suit to the official suit whitelist
        self._rank = rank  # string. "2", "3", ..., "9", "10", "Jack", "Queen", "King", "Ace"
        self._suit = suit  # string. "Diamonds", "Hearts", "Clubs", "Spades"

    # the rank and the suit are made immutable to avoid possible inconsistency bugs when interacting with the other
    # classes
    @property
    def rank(self):
        return self._rank

    @property
    def short_rank(self):  # the short rank is one character long.
        if self._rank == "10":
            return "T"
        else:
            return self._rank[0]

    @property
    def suit(self):
        return self._suit

    @property
    def short_suit(self):  # the short suit is one character long.
        return self._suit[0].lower()

    @property
    def value(self):
        """
        Returns the value of the card. The value represents the strength of the card and is an integer.
        :return: integer.
        """
        return Card.rank_to_value[self.rank]

    def __str__(self):  # the informal representation of a card is two character long (eg. "Tc" for "Ten of Clubs")
        return self.short_rank + self.short_suit

    def __repr__(self):
        return "<Card: {} of {}>".format(self.rank, self.suit)


class Deck:
    """Represents a deck of cards. A Deck is intended to be used as a classic Python list of cards while providing
    additional features like the ability to reset the deck to its original state, easy shuffling and manipulation.
    It also provides static methods for creating standard 32 and 52 card decks.
    Example usage :
    deck = Deck.standard_52_card_deck(shuffled=True)  # creates a standard 52 card deck. The deck is initially shuffled.
    card_Ts = deck["Ts"]  # returns the ten of spades from the deck but it is not removed from the deck.
    print(repr(card_Ts))  # <- "<Card: Ten of Spades>"
    card_Qc = deck[("Queen", "Clubs")]  # alternative syntax to get a specific card.
    print(card_Qc)  # <- "Qc"
    for card in deck[:5]:  # prints the five first cards of the deck
        print(card)
    first_card = deck.extract_card()  # extracts the first card. The first card is no longer present in the deck.
    specific_card = deck.extract_card("Kd")  # extracts a specific card from the deck (no longer present in the deck)
    b = specific_card in deck
    print(b)  # <- b is False because the specific has been extracted from the deck and thus is no longer present in it.
    deck.reset(shuffle=False)  # resets the deck to its original configuration (previously extracted cards are back).
    deck.shuffle()  # shuffles the deck inplace.
    """

    def __init__(self, initial_cards=(), initial_shuffle=False):
        """
        Initializes a deck.
        :param initial_cards: iterable of cards.
        Represents the initial state of the deck. When reset, the deck returns to this initial state.
        :param initial_shuffle: boolean.
        If True, the deck is initially shuffled.
        """
        self.initial_cards = tuple(initial_cards)  # Stores the initial state of the deck. Used for reset.
        self.cards = None  # is used to store the list of the cards currently present in the deck.
        self.reset(initial_shuffle)

    def __str__(self):
        return "[" + ", ".join(str(c) for c in self.cards) + "]"

    def __repr__(self):
        return "<Deck: " + str(self) + ">"

    # The following special methods are here to make a deck usable like a Python list.
    def __len__(self):
        return self.cards.__len__()

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._get_card(item[0], item[1])
        return self.cards.__getitem__(item)

    def __setitem__(self, item):
        return self.cards.__setitem__(item)

    def __delitem__(self, item):
        return self.cards.__delitem__(item)

    def __iter__(self):
        return self.cards.__iter__()

    def __reversed__(self):
        return self.cards.__reversed__()

    def __contains__(self, item):
        return self.cards.__contains__(item)

    def reset(self, shuffle=False):
        """
        Resets the deck to its original state. An optional shuffle option is provided.
        :param shuffle: boolean.
        If True, the deck is shuffled after being reset.
        :return: None.
        """
        self.cards = list(self.initial_cards)
        if shuffle:
            self.shuffle()

    def shuffle(self):
        """Shuffles the deck inplace."""
        random.shuffle(self.cards)

    def _get_card(self, rank, suit):
        """
        Look for the first card in the deck with the provided rank and suit. Raises a LookUpError if not found.
        :param rank: string or integer.
        The rank of the card being looked for. Can also be the short rank (eg. "T"). Integers are converted to string.
        :param suit: string.
        The suit of the card being looked for. Can also be the short suit (eg. "d").
        :return: Card.
        The first card of the deck with corresponding rank and suit.
        """
        if isinstance(rank, int):
            rank = str(rank)
        for card in self.cards:
            if rank in (card.rank, card.short_rank) and suit in (card.suit, card.short_suit):
                return card
        raise LookupError("No card where rank='{}' and suit='{}'.".format(rank, suit))

    def look_at_card(self, card_description=None):
        """
        Returns the card corresponding to card_description. Raises a LookUpError if there is no card corresponding to
        card_description.
        If card_description is None then the first card of the deck is returned. Returns None if the deck is empty.
        The returned card is not removed from the deck.
        :param card_description: Iterable of at least 2 objects or None.
        Can be a string (eg. "Qd") or a tuple/list (eg. ["Queen", "Diamonds"]).
        :return: Card or None.
        """
        if card_description is None:
            return self.cards[0] if self.cards else None
        return self._get_card(*card_description[:2])

    def extract_card(self, card_description=None):
        """
        Returns the card corresponding to card_description and removes it from the deck. Raises a LookUpError if there
        is no card corresponding to card_description.
        If card_description is None then the first card of the deck is returned and removed. Returns None if the deck
        is empty.
        :param card_description: Iterable of at least 2 objects or None.
        Can be a string (eg. "Qd") or a tuple/list (eg. ["Queen", "Diamonds"]).
        :return: Card or None.
        """
        if card_description is None:
            return self.cards.pop(0) if self.cards else None
        card = self._get_card(*card_description[:2])
        self.cards.remove(card)
        return card

    @staticmethod
    def standard_32_card_deck(shuffled=False):
        """
        Returns a standard 32 card deck containing all the cards from the 7 to the Ace in all the four standard suits.
        :param shuffled: boolean.
        If True, the deck is created shuffled.
        :return: Deck.
        """
        cards = [Card(rank, suit) for suit in Card.valid_suits
                 for rank in Card.valid_ranks if rank not in (str(i) for i in range(2, 6 + 1))]
        return Deck(cards, shuffled)

    @staticmethod
    def standard_52_card_deck(shuffled=False):
        """
        Returns a standard 5 card deck containing all the cards from the 2 to the Ace in all the four standard suits.
        :param shuffled: boolean.
        If True, the deck is created shuffled.
        :return: Deck.
        """
        cards = [Card(rank, suit) for suit in Card.valid_suits for rank in Card.valid_ranks]
        return Deck(cards, shuffled)


class Hand:
    """Represents a combination of 5 (or less) cards (Pair, Straight, Full House, etc)"""
    def __init__(self, cards=()):
        assert len(cards) <= 5
        self._cards = tuple(cards)  # tuple of 5 cards or less
        self._strength = None  # integer representing the strength of the hand. The higher the stronger.
        self._name = None  # string (eg: "Two pairs", "Three of a kind", "Royal straight flush")

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, new_cards):
        if set(new_cards) != set(self._cards):
            self._strength = None
            self._name = None
        self._cards = tuple(new_cards)

    @property
    def strength(self):
        if self._strength is None:
            self.compute_strength_and_name()
        return self._strength

    @property
    def name(self):
        if self._name is None:
            self.compute_strength_and_name()
        return self._name

    def __repr__(self):
        return "{" + " ".join(str(c) for c in self._cards) + "} " + ",{}, strength={}".format(self.name, self.strength)

    def compute_strength_and_name(self):
        """Computes the strength and determines the name of the hand. This implementation asserts that the number of
        cards in the hand is five at most."""
        # This is a naive implementation designed for teaching and not for performance.
        n_cards = len(self._cards)
        assert n_cards <= 5
        only_one_suit = len(set(c.suit for c in self._cards)) == 1  # True if all the cards are of the same suit.
        card_values = [c.value for c in self._cards]
        min_of_card_values = min(card_values) if len(card_values) > 0 else 0
        normalised_values_set = set(v - min_of_card_values for v in card_values)
        if normalised_values_set == {0, 1, 2, 3, 4}:  # general case
            is_straight = 1
        elif normalised_values_set == {0, 1, 2, 3, 12}:  # case where the Ace counts as a 1: "A 2 3 4 5"
            is_straight = 2
        else:
            is_straight = 0
        value_count_dic = {c.value: card_values.count(c.value) for c in self._cards}
        values = [(count, value) for value, count in value_count_dic.items()]
        values.sort(reverse=True)  # sort by descending count then descending value
        values = [v[1] for v in values]  # extracting values

        strength_indicators = []
        self._name = "Nothing"
        # straight flush
        if n_cards == 5 and only_one_suit and is_straight:
            if is_straight == 1:  # general case
                strength_indicators = [8, min_of_card_values + 4]
            elif is_straight == 2:  # case where the Ace counts as a 1: "A 2 3 4 5"
                strength_indicators = [8, 5]
            self._name = "Royal straight flush" if min_of_card_values == 10 else "Straight flush"
        # four of a kind
        elif n_cards >= 4 and 4 in value_count_dic.values():
            strength_indicators = [7] + values
            self._name = "Four of a kind"
        # full house
        elif n_cards == 5 and 3 in value_count_dic.values() and 2 in value_count_dic.values():
            strength_indicators = [6] + values
            self._name = "Full house"
        # flush
        elif n_cards == 5 and only_one_suit:
            strength_indicators = [5] + values
            self._name = "Flush"
        # straight
        elif n_cards == 5 and is_straight:
            if is_straight == 1:  # general case
                strength_indicators = [4, min_of_card_values + 4]
            elif is_straight == 2:  # case where the Ace counts as a 1: "A 2 3 4 5"
                strength_indicators = [4, 5]
            self._name = "Straight"
        # three of a kind
        elif n_cards >= 3 and 3 in value_count_dic.values():
            strength_indicators = [3] + values
            self._name = "Three of a kind"
        # two pairs
        elif n_cards >= 4 and list(value_count_dic.values()).count(2) == 2:
            strength_indicators = [2] + values
            self._name = "Two pairs"
        # one pair
        elif n_cards >= 2 and 2 in value_count_dic.values():
            strength_indicators = [1] + values
            self._name = "Pair"
        # high card
        elif n_cards >= 1:
            strength_indicators = [0] + values
            self._name = "High card"

        assert len(strength_indicators) <= 6
        self._strength = sum(s * 100 ** (5 - i) for i, s in enumerate(strength_indicators))

    @staticmethod
    def best_from_cards(cards):
        """
        Returns the best hand of 5 cards from the cards provided. Works with any number of cards. Warning: this method
        tries every possible combination of 5 cards, thus it is very inefficient especially for large (>5) number of
        cards.
        :param cards: iterable of cards.
        :return: Hand.
        """
        current_hand = Hand()
        for cards_subset in itertools.combinations(cards, min(5, len(cards))):
            candidate_hand = Hand(cards_subset)
            if candidate_hand.strength > current_hand.strength:
                current_hand = candidate_hand
        return current_hand


class Player:
    """Represents a player. The bankroll is not modeled here. A player is thus represented only by her name and her
    private cards."""
    n_unnamed_players = 0

    def __init__(self, name=None):
        """Initializes a player. If name is not provided, a generic name will automatically be generated."""
        if name is None:
            Player.n_unnamed_players += 1
            name = "Player " + str(Player.n_unnamed_players)
        self.name = name
        self.cards = []  # private cards of the player

    def __repr__(self):
        cards_repr = "[" + " ".join(str(c) for c in self.cards) + "]"
        return "<Player: {}, {}>".format(self.name, cards_repr)

    def __str__(self):
        cards_str = "[" + " ".join(str(c) for c in self.cards) + "]"
        return "{}: {}".format(self.name, cards_str)

    def reset(self):
        self.cards = []


class Board:
    """The board contains the deck and the cards laid face up that are common to all the players."""
    def __init__(self, deck=None):
        self.cards = []  # list of cards laid face up on the board common to all the players
        if deck is None:
            deck = Deck.standard_52_card_deck()
        self.deck = deck  # instance of class Deck

    def __str__(self):
        cards_str = "[" + " ".join(str(c) for c in self.cards) + "]"
        return "Board: " + cards_str

    def reset(self, shuffle_deck=False):
        """
        Resets the board: removes all the common cards and resets the deck to its original state.
        :param shuffle_deck: boolean.
        If True, the deck is shuffled.
        :return: None.
        """
        self.cards = []
        self.deck.reset(shuffle_deck)

    def shuffle_deck(self):
        """Shuffles the deck inplace."""
        self.deck.shuffle()

    def deal_card_face_up(self, card_description=None):
        """
        Removes the card matching card_description from the deck and places it face up on the board.
        If card_description is None, the first card of the deck is chosen.
        :param card_description: iterable or None
        :return: None
        """
        self.cards.append(self.deck.extract_card(card_description))

    def burn_card(self, card_description=None):
        """Discards a card from the deck. If no card description is provided, discards the first card of the deck."""
        self.deck.extract_card(card_description)


class Game:
    """Represents a game. Can perform all the actions that the dealer can do."""
    def __init__(self, board=None, players_list=()):
        if board is None:
            board = Board()
        self.board = board
        self.players = list(players_list)

    def __str__(self):
        res = ""
        for player in self.players:
            res += str(player) + '\n'
        res += str(self.board)
        return res

    def reset(self, shuffle_deck=False):
        for player in self.players:
            player.reset()
        self.board.reset(shuffle_deck)

    def get_player_named(self, name):
        """
        Returns first player matching the name provided. Raises a NameError if no match is found.
        :param name: string.
        Name of the player.
        :return: Player.
        """
        for player in self.players:
            if player.name == name:
                return player
        raise NameError("No player named {}".format(name))

    def shuffle_deck(self):
        """Shuffles the deck."""
        self.board.shuffle_deck()

    def add_player(self, name=None):
        """
        Adds a player to the game.
        :param name: string or None.
        Name of the new player.
        If None, the new player receives a generic name.
        :return: None
        """
        self.players.append(Player(name))

    def deal_card_to_player(self, player, card_description=None):
        """
        Deals a card from the deck to the designated player.
        :param player: Player or string
        The player to deal the card to.
        If it is a string, the card is dealt to the first player having this name.
        :param card_description: iterable or None
        If not None, the player is dealt the first card of the deck matching the description.
        If None, the player is dealt the first card of the deck.
        :return: None
        """
        if isinstance(player, str):
            player = self.get_player_named(player)
        player.cards.append(self.board.deck.extract_card(card_description))

    def deal_card_to_board(self, card_description=None):
        """Deals the card matching the description face up from the deck to the board. If card_description is None then
        the first card of the deck is chosen."""
        self.board.deal_card_face_up(card_description)

    def deal_private_cards_to_players(self):
        """Deals two cards from the deck to every player."""
        for i in range(2):  # every player is dealt two cards.
            for player in self.players:
                self.deal_card_to_player(player)

    def burn_card(self, card_description=None):
        """Discards a card from the deck. If no card description is provided, discards the first card of the deck."""
        self.board.burn_card(card_description)

    def deal_flop(self):
        """Deals the first three cards of the deck face up on the board."""
        self.burn_card()  # kind of useless but this is how it's done in real life
        for i in range(3):
            self.deal_card_to_board()

    def deal_turn(self):
        """Deals a fourth card to the board. Should only called after the flop has been dealt."""
        self.burn_card()  # kind of useless but this is how it's done in real life
        self.deal_card_to_board()

    def deal_river(self):
        """Deals the river card to the board. Should only be called after the turn."""
        self.burn_card()  # kind of useless but this is how it's done in real life
        self.deal_card_to_board()

    def get_best_hand_from_player(self, player):
        """
        Returns the best hand possible from the cards of the board combined with the cards of the designated player.
        :param player: Player or string.
        Player to get the cards from.
        If string, gets the cards from the first player matching this name.
        :return: Hand.
        Best hand of the player.
        """
        if isinstance(player, str):
            player = self.get_player_named(player)
        total_cards = player.cards + self.board.cards
        return Hand.best_from_cards(total_cards)

    def players_with_hand(self):
        """Returns a dictionary where the keys are the players and the values are their corresponding best hand."""
        return {player: self.get_best_hand_from_player(player) for player in self.players}

    def get_winning_players(self):
        """Returns the list of the players who have strongest hand."""
        # In typical situations, the list will contain only one player.
        if not self.players:  # if there is no player
            return []
        hands_dic = self.players_with_hand()
        max_strength = max(hand.strength for hand in hands_dic.values())
        return [player for player, hand in hands_dic.items() if hand.strength == max_strength]
