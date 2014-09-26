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
    normal_move = 1
    jack = 10
    queen_of_spades = 11


class CrazyEight:

    '''
    CrazyEight Class - CS156 Assignment #2

    Contains two public methods.  They are move and move_perfect_knowledge.
    '''

    def move(self, partial_state):
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

        # Check if my current move is blocked.  If so, return immediately.
        (move_type, next_move) = check_for_blocked_turn(history)
        if(move_type != MoveType.normal_move):
            return next_move

        #  Determine available cards in deck and other player's hand.

    def move_perfect_knowledge(self, state):
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

        # Check if my current move is blocked.  If so, return immediately.
        (move_type, next_move) = check_for_blocked_turn(history)
        if(move_type != MoveType.normal_move):
            return next_move


def determine_card_rank(card_number):
    '''
    Function to extract the rank (i.e. Ace, 2, King, etc.) of a specified card.

    :param int card_number: ID number for a specific card.

    :returns: Card's rank.  0 is Ace; 2-10's rank is their face value minus 1.
                            Example: 10 is Jack. 11 is Queen. 12 is King.
    '''
    return card_number % 13  # Thirteen since 13 ranks per suit.


def determine_card_suit(card_number):
    '''
    Function to extract the suit of a specified card.

    :param int card_number: ID number for a specific card.

    :returns: Card's suit.  0 is spade; 1 is heart; 2 is diamond; 3 is clubs.
    '''
    return card_number // 4


def check_for_blocked_turn(history):
    '''
    This function checks if a move by the current player is blocked due to
    a move made by the other player.

    :param tuple history:
    :returns: Tuple in the form of (MoveType, NextMove (if applicable)).
            A NextMove is itself a tuple in the form:
            (player_num, face_up_card, suit, number_of_cards)
    '''
    # On the first move, regardless of face card, always a normal move.
    if(len(history) == 1):
        return (MoveType.normal_move, (-1, -1, -1, -1))

    #  Get the last move.
    last_move = history[len(history) - 1]

    #  Parse the last move.
    last_player = last_move[0]  # The player who played last.
    last_discard = last_move[1]  # Face up card.
    last_suit = last_move[2]
    numb_picked_up_cards = last_move[3]  # Numb of cards picked up in last turn

    # If on the last move someone drew, then this turn is always a normal move.
    if(numb_picked_up_cards > 0):
        return (MoveType.normal_move, (-1, -1, -1, -1))

    # Check if the last move was queen of spades.
    if(last_player != 0 and last_discard == MoveType.queen_of_spades):
        # On a queen of spades, must draw five cards.
        return (MoveType.queen_of_spades, (0, last_discard, last_suit, 5))

    # Check if the last move was a jack
    if(last_player != 0 and
       determine_card_rank(last_discard) == MoveType.jack):
        return (MoveType.jack, (0, last_discard, last_suit, 1))


def parse_played_history(history):
    '''
    :param tuple history: List of tuples in the format:
                 (player_num, face_up_card, suit, number_of_cards)

    :returns: Tuple in the form (number_cards_player0, number_cards_player1,
                                 list_of_discarded_cards)
    '''

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
