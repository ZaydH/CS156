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
    '''
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
        return (MoveType.normal_move, (-1, -1, -1, -1))

    #  Get the last move.
    last_move = history[len(history) - 1]

    #  Parse the last move.
    last_discard = get_discard(last_move[1])  # Face up card.
    # Numb of cards picked up in last turn
    numb_picked_up_cards = get_number_of_cards_to_draw(last_move[3])

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


def parse_played_history(history):
    '''
    :param tuple history: List of tuples in the format:
                 (player_num, face_up_card, suit, number_of_cards)

    :returns: Tuple in the form (number_cards_player0, number_cards_player1,
                                 list_of_discarded_cards)
    '''
    assert(False)

    # Each player starts with 8 cards.
    numb_cards_per_player = [8, 8]

    # Process the first move
    previous_discard = history[0][1]
    discarded_cards = [previous_discard]  # Extracts first card in the history

    # Iterate through the remaining moves
    for i in range(1, len(history)):
        # Extract the current player, current discarded card, and numb cards
        current_player = history[i][0]
        current_discard = history[i][1]
        numb_drawn_cards = history[i][3]

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


def create_move(player_numb, top_of_discard, suit, numb_drawn_cards):
    '''
    Helper function to create a move for the history list.

    :param int player_numb: 0 for Computer, 1 for Human
    :param int top_of_card: Rank/Suit number for card on top of discard pile
    :param int suit: Number of the suit
    :param int numb_draw_cards: Number of cards drawn in the turn.

    :returns: Tuple in the form:
        (player_numb, top_of_discard, suit, numb_drawn_cards)
    '''
    return (player_numb, top_of_discard, suit, numb_drawn_cards)


def get_discard(move):
    '''
    Extracts from a move the discarded card.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number for the discarded card.
    '''
    return move[1]


def get_number_of_cards_to_draw(move):
    '''
    Extracts from a move the number of cards to draw in this turn.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number of cards to draw (>=0) in the form:
        (player_numb, top_of_discard, suit, numb_drawn_cards)
    '''
    return move[3]
