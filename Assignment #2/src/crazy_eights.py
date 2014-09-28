'''
Created on September 26, 2014

@author: Zayd Hammoudeh

Team Member #1: Zayd Hammoudeh (009418877)
Team Member #2: Muffins Hammoudeh
        (No student ID - she's my cat but was here with me
        while I worked so she deserves credit).
'''

import random


class MoveType:
    '''
    '''
    normal_move = -1
    two = 1
    one_two = 2
    two_twos = 4
    three_twos = 6
    four_twos = 8
    eight = 7
    jack = 10
    queen_of_spades = 11


class PlayerType:
    human = 0
    computer = 1


class CrazyEight:

    '''
    CrazyEight Class - CS156 Assignment #2

    Contains two public methods.  They are move and move_perfect_knowledge.
    '''

    @staticmethod
    def move(partial_state):
        '''
        :param tuple partial_state: Tuple in the form:
            (face_up_card, suit, hand, history)

        :returns: A move in the form:
            (player_num, face_up_card, suit, number_of_cards)
        '''
        # Extract the input parameters from the tuple.
        face_up_card = partial_state[0]
        suit = partial_state[1]
        hand = partial_state[2]
        history = partial_state[3]

        # Extract current move type.
        move_type = check_for_special_move_type(history)
        # Make forced play in case of a queen of spaces.
        if(move_type == MoveType.queen_of_spades):
            return get_special_move(MoveType.queen_of_spades,
                                    PlayerType.computer)

        #  Determine available cards in deck and other player's hand.

    @staticmethod
    def move_perfect_knowledge(state):
        '''
        :param tuple state: Tuple in the form (deck, other_hand, partial_state)
        '''
        # Extract the deck.
        deck = state[0]

        # List of cards in the other player's hand.
        other_hand = state[1]

        # Extract the partial state information from the state object.
        face_up_card = state[2][0]
        suit = state[2][1]
        hand = state[2][2]
        history = state[2][3]

        # Extract current move type.
        move_type = check_for_special_move_type(history)
        # Make forced play in case of a queen of spaces.
        if(move_type == MoveType.queen_of_spades):
            return get_special_move(MoveType.queen_of_spades,
                                    PlayerType.computer)


def get_card_rank(card_number):
    '''
    Function to extract the rank (i.e. Ace, 2, King, etc.) of a specified card.

    :param int card_number: ID number for a specific card.

    :returns: Card's rank.  0 is Ace; 2-10's rank is their face value minus 1.
                            Example: 10 is Jack. 11 is Queen. 12 is King.
    '''
    return card_number % 13  # Thirteen since 13 ranks per suit.


def get_card_suit(card_number):
    '''
    Function to extract the suit of a specified card.

    :param int card_number: ID number for a specific card.

    :returns: Card's suit.  0 is spade; 1 is heart; 2 is diamond; 3 is clubs.

    >>> get_card_suit(0)
    0
    >>> get_card_suit(51)
    3
    >>> get_card_suit(13)
    1
    >>> get_card_suit(15)
    1
    >>> get_card_suit(39)
    3
    >>> get_card_suit(-1)
    Traceback (most recent call last):
        ...
    ValueError: card_number must be between 0 and 51
    >>> get_card_suit(52)
    Traceback (most recent call last):
        ...
    ValueError: card_number must be between 0 and 51
    '''
    if(card_number < 0 or card_number > 51):
        raise ValueError("card_number must be between 0 and 51")
    return card_number // 13


def check_for_special_move_type(history):
    '''
    This function checks if a move by the current player is specially altered
    due to a move made by the other player.

    :param tuple history: History of moves to current time.

    :returns: An object of type "MoveType"
    '''
    # On the first move, regardless of face card, always a normal move.
    if(len(history) == 1):
        return MoveType.normal_move

    #  Get the last move.
    last_move = history[len(history) - 1]

    #  Parse the last move.
    last_discard = get_discard(last_move)  # Face up card.
    # Numb of cards picked up in last turn
    numb_picked_up_cards = get_number_of_cards_to_draw(last_move)

    # If on the last move someone drew, then this turn is always a normal move.
    if(numb_picked_up_cards > 0):
        return MoveType.normal_move

    # Check if the last move was queen of spades.
    if(last_discard == MoveType.queen_of_spades):
        # On a queen of spades, must draw five cards.
        return MoveType.queen_of_spades

    # Check if the last move was a jack
    if(get_card_rank(last_discard) == MoveType.jack):
        return MoveType.jack

    # Check if the last move was a two.
    if(get_card_rank(last_discard) == MoveType.two):
        numb_history_elements = len(history)
        twos_count = 1

        # Iterate checking twos court
        while(twos_count < 4
              and get_card_rank(last_discard) == MoveType.two
              and numb_history_elements >= twos_count + 2):

            # Get previous discard count.
            last_discard = get_discard(history[len(history) - twos_count - 1])
            if(get_card_rank(last_discard) == MoveType.two):
                # Increment the number of twos
                twos_count += 1

                if(numb_history_elements == 1 + twos_count):
                    return MoveType.two_twos

        # Return the number of twos played in a row,
        if(twos_count == 1):
            return MoveType.one_two
        if(twos_count == 2):
            return MoveType.two_twos
        elif(twos_count == 3):
            return MoveType.three_twos
        else:
            return MoveType.four_twos

    # Under all other circumstances, the next move is normal.
    return MoveType.normal_move


def get_special_move(move_type, player_type):
    '''
    For specified special moves, this function returns the associated
    special move object.

    :param MoveType move_type: Type of move made.
    :param PlayerType player_type: Current player either human or computer.

    :returns: Move object in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)
    '''
    #  Check for special move for queen of spades
    if(move_type == MoveType.queen_of_spades):
        return create_move(player_type, 0, 0, 5)

    #  Check for special move for multiple twos
    if(move_type == MoveType.one_two or move_type == MoveType.two_twos
       or move_type == MoveType.three_twos or move_type == MoveType.four_twos):
        return create_move(player_type, 0, 0, move_type)


def parse_move_string(move_type, input_move, player,
                      hand, face_up_card, face_up_suit):
    '''
    This function parses a specified string and if it is a valid
    move it, returns that string.  Otherwise, it returns None.

    :param MoveType move_type: Type of move made.
    :param str input_move: String specified as an input move
    :param PlayerType player: Current player either human (0) or computer (1)
    :param int hand: List of cards in the player's hand.
    :param int face_up_card: 0 to 51 for current face up card.
    :param int face_up_suit: 0 to 3 value of the suit.

    :returns: Move object in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)
        or None if the move is invalid.

    >>> parse_move_string(MoveType.normal_move, "" , 1 , [3,4], 6, 1)

    >>> parse_move_string(MoveType.normal_move, "(" , 1 , [3,4], 6, 1)

    >>> parse_move_string(MoveType.normal_move, "()" , 1 , [3,4], 6, 1)

    >>> parse_move_string(MoveType.normal_move, "(1, 3, 0, dsd)", 1, [3], 6, 1)

    >>> parse_move_string(MoveType.normal_move, "(1, 3, 0, 0)", 1, [3,4], 6, 0)
    (1, 3, 0, 0)
    >>> parse_move_string(MoveType.queen_of_spades,"(1, 0, 0, 5)",1,[3,4],6,0)
    (1, 0, 0, 5)
    '''

    if(len(input_move) < 2):
        return None

    # Check for preceding parenthesis
    if(input_move[0] != "("):
        return None
    # Remove initial parenthesis
    else:
        input_move = input_move[1:]

    # Check if last character is a parenthesis
    move_len = len(input_move)
    if(input_move[move_len - 1] != ")"):
        return None
    # Remove the trailing parenthesis
    else:
        input_move = input_move[:move_len - 1]

    # Extract the move parameters
    string_move_parameters = input_move.split(", ")
    if(len(string_move_parameters) != 4):
        return None

    # Convert the string parameters to integers.
    move_param = []  # Create the integer move parameters array
    for param in string_move_parameters:
        try:
            int_param = int(param)
        except:
            # Value is not an integer so return None
            return None
        # If a valid integer, then append it.
        move_param.append(int_param)

    # Build the tuple.
    move = (move_param[0], move_param[1], move_param[2], move_param[3])

    # If the move is valid return it otherwise return None.
    if(check_if_move_valid(move_type, move, player, hand,
                           face_up_card, face_up_suit)):
        return move
    else:
        return None


def check_if_move_valid(move_type, move, player,
                        hand, face_up_card, face_up_suit):
    '''
    This function parses a specified string and if it is a valid
    move it, returns that string.  Otherwise, it returns None.

    :param MoveType move_type: Type of move made.
    :param str input_move: String specified as an input move
    :param PlayerType player: Current player either human (0) or computer (1)
    :param int hand: List of cards in the player's hand.
    :param int face_up_card: 0 to 51 for current face up card.
    :param int face_up_suit: 0 to 3 value of the suit.

    :returns: True for a valid move and False otherwise.

    >>> check_if_move_valid(MoveType.normal_move, (0, 0, 0, 0), -1, [], -1,-1)
    Traceback (most recent call last):
        ...
    ValueError: player must be either 0 or 1
    >>> check_if_move_valid(MoveType.normal_move, (0, 0, 0, 0), 0, [], -1,-1)
    Traceback (most recent call last):
        ...
    ValueError: The player's hand must have at least one card.
    >>> check_if_move_valid(MoveType.normal_move, (0, 0, 0, 0), 0, [0], -1,-1)
    Traceback (most recent call last):
        ...
    ValueError: face_up_card must be between 0 and 51
    >>> check_if_move_valid(MoveType.normal_move, (0, 0, 0, 0), 0, [0], 0,-1)
    Traceback (most recent call last):
        ...
    ValueError: face_up_suit must be between 0 and 3
    >>> check_if_move_valid(MoveType.normal_move,(1,40,0,0),1,[20,50,40],39,3)
    True
    >>> check_if_move_valid(MoveType.normal_move,(1,40,0,1),1,[20,50,40],39,3)
    False
    >>> check_if_move_valid(MoveType.normal_move,(1,0,1,1),1,[20,50,40],39,3)
    False
    >>> check_if_move_valid(MoveType.normal_move, (0, 0, 0, 0), 0, [1], 2,0)
    False
    >>> check_if_move_valid(MoveType.normal_move, (1, 0, 0, 0), 1, [0],2,0)
    True
    >>> check_if_move_valid(MoveType.normal_move, (0, 0, 0, 0), 0, [0],2,0)
    True
    >>> check_if_move_valid(MoveType.normal_move, (1, 0, 0, 1), 0, [0], 2,0)
    False
    >>> check_if_move_valid(MoveType.one_two, (1, 0, 0, 1), 1, [0], 2,0)
    False
    >>> check_if_move_valid(MoveType.one_two, (1, 0, 0, 2), 1, [0], 2,0)
    True
    >>> check_if_move_valid(MoveType.one_two, (1, 1, 0, 0), 1, [3,1], 2,0)
    True
    >>> check_if_move_valid(MoveType.one_two, (1, 3, 0, 0), 1, [3,1], 2,0)
    False
    >>> check_if_move_valid(MoveType.queen_of_spades, (1, 0, 0, 5),1,[1], 2,0)
    True
    >>> check_if_move_valid(MoveType.queen_of_spades, (1, 0, 0, 4),1,[1], 2,0)
    False
    >>> check_if_move_valid(MoveType.queen_of_spades, (1, 1, 0, 0),1,[1], 2,0)
    False
    >>> check_if_move_valid(MoveType.normal_move, (1, 7, 1, 0),1,[7,20], 2,0)
    True
    >>> check_if_move_valid(MoveType.normal_move, (1, 20, 0, 0),1,[20,7], 2,0)
    True
    '''

    # Check for valid input conditions.
    if(player != 0 and player != 1):
        raise ValueError("player must be either 0 or 1")
    if(len(hand) == 0):
        raise ValueError("The player's hand must have at least one card.")
    if(face_up_card < 0 or face_up_card > 51):
        raise ValueError("face_up_card must be between 0 and 51")
    if(face_up_suit < 0 or face_up_suit > 3):
        raise ValueError("face_up_suit must be between 0 and 3")

    # Extract some information on the move. This is used below.
    discarded_card = get_discard(move)
    numb_cards_to_draw = get_number_of_cards_to_draw(move)

    #  Check if the player in the move matches the expected value.
    if(get_player(move) != player):
        return False

    # Check special moves here.
    if(move_type == MoveType.queen_of_spades):
        return move == get_special_move(MoveType.queen_of_spades, player)

    # Check the case where you need to draw cards.
    if(move_type == MoveType.one_two or move_type == MoveType.two_twos
       or move_type == MoveType.three_twos or move_type == MoveType.four_twos):
        # If the player had to draw on a two, verify the move is valid.
        if(numb_cards_to_draw > 0):
            return move == get_special_move(move_type, player)
        # Check if the move matches what was expected.
        else:
            return (get_card_rank(discarded_card) == MoveType.two
                    and get_card_suit(discarded_card) == get_suit(move))

    # Check the case where you need to draw cards.
    if(numb_cards_to_draw > 0):
        if(discarded_card == get_suit(move) == 0):
            return True
        else:
            return False

    # Check if the specified discarded card is in the player's hand.
    if(discarded_card not in hand):
        return False

    # TODO implement checking for checking of 8's
    # Handle the case of an 8 special
    if(get_card_rank(discarded_card) == MoveType.eight):
        return True

    # For a discard, check if the suit and/or face card matches
    return (get_card_rank(discarded_card) == get_card_rank(face_up_card)
            or get_card_suit(discarded_card) == face_up_suit)


def parse_played_history(history):
    '''
    :param tuple history: List of tuples in the format:
                 (player_num, face_up_card, suit, number_of_cards)

    :returns: Tuple in the form (number_cards_player0, number_cards_player1,
                                 list_of_discarded_cards)
    '''

    # TODO In history parser, handle when player is 0/1 and forced picked.

    # Each player starts with 8 cards.
    numb_cards_per_player = [8, 8]

    # Process the first move
    previous_discard = history[0][1]
    discarded_cards = [previous_discard]  # Extracts first card in the history

    # Iterate through the remaining moves
    for i in range(1, len(history)):

        # Get the last move.
        last_move = history[i]

        # Extract the current player, current discarded card, and numb cards
        current_player = history[i][0]
        current_discard = get_discard(last_move)
        numb_drawn_cards = get_number_of_cards_to_draw(last_move)

        # Check if a card was discarded in the last turn
        # If so, update the list of discard cards and
        # decrement the players card count.
        if(current_discard != previous_discard):
            discarded_cards.append(current_discard)
            numb_cards_per_player[current_player] -= 1
        else:
            numb_cards_per_player[current_player] += numb_drawn_cards

        # Return the play history.
        return (numb_cards_per_player[0], numb_cards_per_player[1],
                discarded_cards)


def shuffle_deck(valid_cards):
    '''
    This function takes a list of remaining card values.
    It then shuffles the cards and returns a list of cards.

    This shuffling is done in place.

    :param int valid_cards: List of integers of valid cards.

    :returns: List of the specified valid cards shuffled.
    '''
    numb_cards = len(valid_cards)  # Extract number of cards

    # The way the iterator works is that it selects a random
    # card and then swaps it with the card at index i.
    # The swapping is done in place.
    for i in range(numb_cards):
        rand_index = random.randint(i, numb_cards-1)
        temp = valid_cards[i]  # temporarily store the integer in i.
        #  Swap the card at the random index and the card at i.
        valid_cards[i] = valid_cards[rand_index]
        valid_cards[rand_index] = temp

    #  Return the shuffled deck.
    return valid_cards


def create_move(player, discarded_card, suit, numb_drawn_cards):
    '''
    Helper function to create a move for the history list.

    :param int player: 0 for Computer, 1 for Human
    :param int discarded_card: Rank/Suit number for card on top of discard pile
    :param int suit: Number of the suit
    :param int numb_draw_cards: Number of cards drawn in the turn.

    :returns: Tuple in the form:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    >>> create_move(2, 0, 8, -1)
    Traceback (most recent call last):
        ...
    ValueError: player must be either 0 or 1
    >>> create_move(1, 55, 8, -1)
    Traceback (most recent call last):
        ...
    ValueError: discarded_card must be between 0 and 51
    >>> create_move(1, 0, 8, -1)
    Traceback (most recent call last):
        ...
    ValueError: suit must be between 0 and 3
    >>> create_move(1, 0, 0, 7)
    Traceback (most recent call last):
        ...
    ValueError: numb_drawn cards must be either 0, 1, 2, 4, 5, or 8
    >>> create_move(1, 1, 0, 5)
    Traceback (most recent call last):
        ...
    ValueError: When discarding cards, discarded_card and suit both must be 0
    >>> create_move(1, 0, 2, 5)
    Traceback (most recent call last):
        ...
    ValueError: When discarding cards, discarded_card and suit both must be 0
    >>> create_move(1, 25, 2, 0)
    (1, 25, 2, 0)
    '''

    # Check the input parameters.
    if(player != 0 and player != 1):
        raise ValueError("player must be either 0 or 1")
    if(discarded_card < 0 or discarded_card > 51):
        raise ValueError("discarded_card must be between 0 and 51")
    if(suit < 0 or suit > 3):
        raise ValueError("suit must be between 0 and 3")
    if(numb_drawn_cards != 0 and numb_drawn_cards != 1
       and numb_drawn_cards != 2 and numb_drawn_cards != 4
       and numb_drawn_cards != 5 and numb_drawn_cards != 8):
        raise ValueError("numb_drawn cards must be either 0, 1, 2, 4, 5, or 8")
    if(numb_drawn_cards > 0 and (discarded_card != 0 or suit != 0)):
        raise ValueError("When discarding cards, discarded_card"
                         + " and suit both must be 0")

    # Return the tuple
    return (player, discarded_card, suit, numb_drawn_cards)


def get_player(move):
    '''
    Extracts from a move the player that made it.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number for the player.
    '''
    return move[0]


def get_discard(move):
    '''
    Extracts from a move the discarded card.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number for the discarded card.
    '''
    return move[1]


def get_suit(move):
    '''
    Extracts from a move the currently active suit.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number for the current suit.
    '''
    return move[2]


def get_number_of_cards_to_draw(move):
    '''
    Extracts from a move the number of cards to draw in this turn.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number of cards to draw (>=0) in the form:
        (player_numb, top_of_discard, suit, numb_drawn_cards)
    '''
    return move[3]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
