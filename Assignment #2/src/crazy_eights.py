'''
Created on September 26, 2014

@author: Zayd Hammoudeh

Team Member #1: Zayd Hammoudeh (009418877)
Team Member #2: Muffins Hammoudeh
        (No student ID - she's my cat but was here with me
        while I worked so she deserves credit).
'''

import random


cards_per_deck = 52


class MoveType:
    '''
    Essentially an enumerated type listing special
    move indicators.
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
    '''
    Indicator of the player making a specific move.
    '''
    human = 0
    computer = 1


class CrazyEight:

    '''
    CrazyEight Class - CS156 Assignment #2

    Contains two public methods.  They are move and move_perfect_knowledge.
    '''
    _maximum_depth = 5

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
        active_suit = partial_state[1]
        computer_hand = partial_state[2]
        history = partial_state[3]

        #  Determine available cards in deck and other player's hand.
        numb_human_cards, numb_computer_cards, discarded_cards = \
            parse_play_history(history)

        # If the number of cards in the history does not match the
        # number the number cards in the computers hand raise an error'''
        if(numb_computer_cards != len(computer_hand)):
            raise ValueError("The history and the size of the computer's "
                             + "hand do not match")

        # Build a list of the available plays
        available_cards = build_available_card_list(computer_hand,
                                                    discarded_cards)

        # Iterate through n random game possible permutations
        # to select the best possible move.
        best_move = (-1, -1, -1, -1)

        # Dictionary storing moves proposed by the "perfect_knowledge" method
        # as well as the number of times it was selected.  The more times it
        # was selected, the better the solution.
        proposed_moves = {}
        for i in range(0, 100):

            # Shuffle the available deck.
            shuffled_deck = shuffle_deck(list(available_cards))
            # Separate the available cards into the human player's hand
            # and the un-played (available) card set.
            human_player_hand, shuffled_deck = draw_cards(shuffled_deck,
                                                          numb_human_cards)
            # Sort the human player hand for improved readability.
            # TODO remove human player hand sort.
            human_player_hand.sort()

            # Build the state Tuple for the computer's move.
            state = (shuffled_deck, human_player_hand, partial_state)
            temp_move = CrazyEight.move_perfect_knowledge(state)

            # On first loop, best move is the current one.
            if(i == 0):
                best_move = temp_move
                # Add first move to the dictionary
                proposed_moves[temp_move] = 1
            else:
                # If this move has not been previously proposed,
                # then add it to the dictionary
                if(temp_move not in proposed_moves):
                    proposed_moves[temp_move] = 1
                # If previously proposed, increment its proposed count
                else:
                    # Get previous proposed count
                    proposed_count = proposed_moves[temp_move]
                    proposed_moves[temp_move] = proposed_count + 1

                # Check if you need to update best move
                if(proposed_moves[temp_move] > proposed_moves[best_move]):
                    temp_move = best_move

        # TODO Remove move checker before submitting.
        # Extract previous move type.
        previous_move_type = check_for_special_move_type(history)
        # Error check that the proposed move is valid.
        if(check_if_move_valid(previous_move_type, best_move,
                               PlayerType.computer, computer_hand,
                               face_up_card, active_suit)):
            raise RuntimeError("Best move selected is invalid.")

        # Return the best move.
        return best_move

    @staticmethod
    def move_perfect_knowledge(state):
        '''
        :param tuple state: Tuple in the form (deck, other_hand, partial_state)

        :returns: Best possible move given the state and search depth.
        '''

        # Extract the partial state information from the state object.
        partial_state = state[2]
        face_up_card = partial_state[0]
        active_suit = partial_state[1]
        computer_hand = partial_state[2]
        history = partial_state[3]

        # Check if the current move is a special contigency.
        previous_move_type = check_for_special_move_type(history)

        # Generate set of possible moves.
        possible_moves = \
            CrazyEight.generate_all_moves(PlayerType.computer,
                                          computer_hand, face_up_card,
                                          active_suit)

        # TODO Remove possible moves checker.
        if(len(possible_moves) == 0):
            raise RuntimeError("Error generating moves. One move is "
                               + "always possible.")

        # If only one move is possible, just return that.
        if(len(possible_moves) == 1):
            return possible_moves[0]

    @staticmethod
    def generate_all_moves(player, previous_move_type, player_hand,
                           face_up_card, active_suit):
        '''
        Builds the set of possible ACTIONs for a given hand, face up
        card,

        :param PlayerType player: 0 for human, 1 for computer.
        :param MoveType previous_move_type: Type of previous move.
        :param int[] player_hand: Cards (ints) in the player's hand.
        :param int face_up_card: Card on top of the debug pile.
        :param int active_suit: Currently active suit.

        :returns: List of possible moves where a move is a tuple in the form:
            (player_num, face_up_card, suit, number_of_cards)

        >>> CrazyEight.generate_all_moves(1, MoveType.queen_of_spades, \
 [3, 4, 5], 3, 1)
        [(1, 0, 0, 5)]
        >>> CrazyEight.generate_all_moves(0, MoveType.queen_of_spades, \
 [3, 4, 5], 3, 1)
        [(0, 0, 0, 5)]
        >>> CrazyEight.generate_all_moves(1, MoveType.normal_move, \
 [16, 4, 5], 3, 1)
        [(1, 16, 1, 0), (1, 0, 0, 1)]
        >>> CrazyEight.generate_all_moves(0, MoveType.normal_move, \
 [16, 4, 5], 3, 1)
        [(0, 16, 1, 0), (0, 0, 0, 1)]
        >>> CrazyEight.generate_all_moves(1, MoveType.normal_move, \
 [16, 7, 20], 3, 1)
        [(1, 16, 1, 0), (1, 7, 0, 0), (1, 7, 1, 0), (1, 7, 2, 0),\
 (1, 7, 3, 0), (1, 20, 0, 0), (1, 20, 1, 0), (1, 20, 2, 0), (1, 20, 3, 0),\
 (1, 0, 0, 1)]
        >>> CrazyEight.generate_all_moves(0, MoveType.normal_move, \
 [16, 7, 20], 3, 1)
        [(0, 16, 1, 0), (0, 7, 0, 0), (0, 7, 1, 0), (0, 7, 2, 0),\
 (0, 7, 3, 0), (0, 20, 0, 0), (0, 20, 1, 0), (0, 20, 2, 0), (0, 20, 3, 0),\
 (0, 0, 0, 1)]
        >>> CrazyEight.generate_all_moves(0, MoveType.one_two, \
 [2, 13, 50], 2, 0)
        [(0, 0, 0, 2)]
        >>> CrazyEight.generate_all_moves(0, MoveType.two_twos, \
 [2, 13, 50], 2, 0)
        [(0, 0, 0, 4)]
        >>> CrazyEight.generate_all_moves(0, MoveType.three_twos, \
 [2, 13, 50], 2, 0)
        [(0, 0, 0, 6)]
        >>> CrazyEight.generate_all_moves(1, MoveType.three_twos, \
 [2, 1, 50], 2, 0)
        [(1, 0, 0, 6), (1, 1, 0, 0)]
        >>> CrazyEight.generate_all_moves(1, MoveType.three_twos, \
 [2, 14, 1, 50], 2, 0)
        [(1, 0, 0, 6), (1, 14, 1, 0), (1, 1, 0, 0)]
        >>> CrazyEight.generate_all_moves(0, MoveType.four_twos, \
 [2, 13, 50, 1, 14], 2, 0)
        [(0, 0, 0, 8)]
        '''

        # Empty set of possible moves initially.
        possible_moves = []

        # Make forced play in case of a queen of spaces.
        if(previous_move_type == MoveType.queen_of_spades):
            temp_move = get_special_move(MoveType.queen_of_spades, player)
            return[temp_move]

        # If the move is four twos, must pick up. No choice.
        if(previous_move_type == MoveType.four_twos):
            temp_move = get_special_move(MoveType.four_twos, player)
            return[temp_move]

        # Check if the previous move was a two.
        if(previous_move_type == MoveType.one_two
           or previous_move_type == MoveType.two_twos
           or previous_move_type == MoveType.three_twos):

            # Always can pick up
            possible_moves = [get_special_move(previous_move_type, player)]

            # Check if any twos in the hand.
            for card in player_hand:
                if(get_card_rank(card) == MoveType.two):
                    possible_moves += [create_move(player, card,
                                                   get_card_suit(card), 0)]

            # Return on these possible moves
            return possible_moves

        # Check playable cards. Playable moves add to the list.
        for card in player_hand:
            # Check special case of an 8.
            if(get_card_rank(card) == MoveType.eight):
                # For an eight add all possible suit choices.
                for i in range(0, 4):
                    possible_moves += [create_move(player,
                                                   card, i, 0)]
            # All other cards but 8 must match either suit or rank.
            elif(get_card_rank(card) == get_card_rank(face_up_card)
                 or get_card_suit(card) == active_suit):
                # If eligible card, add to the array.
                possible_moves += [create_move(player, card,
                                               active_suit, 0)]

        # If not a special move, then always can draw a card.
        possible_moves += [create_move(player, 0, 0, 1)]
        # Return set of possible moves.
        return possible_moves

    @staticmethod
    def heuristic_eval_function(human_hand, computer_hand):
        '''
        Function used when the cut-off test is met in the Minimax
        algorithm.

        :param int human_hand: List of integers for cards in human's hand
        :param int computer_hand: List of integers for cards in computer's hand

        :returns: 1 if computer has greater chance to win, -1 otherwise.

        >>> CrazyEight.heuristic_eval_function([3,4],[2,5])
        1
        >>> CrazyEight.heuristic_eval_function([4],[2,5])
        -1
        >>> CrazyEight.heuristic_eval_function([6,5,2],[2,5])
        1
        >>> CrazyEight.heuristic_eval_function([],[5])
        Traceback (most recent call last):
            ...
        ValueError: The human and computer hands must have at least 1 card
        >>> CrazyEight.heuristic_eval_function([5],[])
        Traceback (most recent call last):
            ...
        ValueError: The human and computer hands must have at least 1 card
        '''

        if(len(human_hand) == 0 or len(computer_hand) == 0):
            raise ValueError("The human and computer hands must have "
                             + "at least 1 card")

        #  Determine a predicted score for each of the players
        for i in range(0, 2):
            # First time through the loop, look at human hand
            if(i == PlayerType.human):
                current_hand = human_hand
            # Second time through the loop, look at the computer hand
            else:
                current_hand = computer_hand

            # Start by looking at size of one's hand.
            current_score = len(current_hand)

            # Correct for good quality cards
            for card in current_hand:
                # In case of two, could hurt opponent so subtract 1
                if(card == MoveType.two):
                    current_score -= 1
                # Queen can hurt the opponent so subtract 3.5
                elif(card == MoveType.queen_of_spades):
                    current_score -= 3.5
                # Eights are valuable so subtract 0.5
                elif(card == MoveType.eight):
                    current_score -= 0.5
                # Jacks can hurt opponent so subtract 0.5
                elif(card == MoveType.jack):
                    current_score -= 0.5

            # Store the score
            if(i == PlayerType.human):
                human_score = current_score
            else:
                computer_score = current_score

        # If computer has a lower score, return 1 since
        # We predict he has a better chance to win.
        if(computer_score < human_score):
            return 1
        # If computer has a lower score, return -1 since
        # we predict he has a better chance to lose.
        elif(human_score < computer_score):
            return -1
        # If both have the same score, look at their mins
        else:
            if(min(human_hand) > min(computer_hand)):
                return 1
            else:
                return -1


def at_game_end(game_deck, human_player_hand, computer_player_hand):
    '''
    Checks to see if the game has been completed.

    :param int game_deck: List of cards remaining in the game deck.
    :param int human_player_hand: List of cards in the human's hand.
    :param int computer_player_hand: List of cards in the computer's hand.

    >>> at_game_end([],[6,8],[5])
    True
    >>> at_game_end([945],[6,8],[5])
    False
    >>> at_game_end([945],[],[5])
    True
    >>> at_game_end([945],[5],[])
    True
    >>> at_game_end([945],[],[])
    True
    >>> at_game_end([],[],[])
    True
    '''
    return (len(game_deck) == 0 or len(human_player_hand) == 0
            or len(computer_player_hand) == 0)


def determine_winner(human_hand, computer_hand):
    '''
    At the end of a game, it terms the winning player.

    :param int[] human_hand: Cards in the human player's hand.
    :param int[] computer_hand: Cards in the computer player's hand.

    :returns: PlayerType.human if the human won. Otherwise PlayerType.Computer

    >>> determine_winner([], [])
    Traceback (most recent call last):
        ...
    ValueError: Both human and computer hands cannot be empty.
    >>> determine_winner([], [5, 8, 9])
    0
    >>> determine_winner([], [5])
    0
    >>> determine_winner([5, 8, 9], [])
    1
    >>> determine_winner([5, 50, 4], [2])
    1
    >>> determine_winner([2, 800], [5, 50, 4])
    0
    '''

    if(len(human_hand) == len(computer_hand) == 0):
        raise ValueError("Both human and computer hands cannot be empty.")

    # Case #1: Human has less cards so s/he wins.
    if(len(human_hand) < len(computer_hand)):
        return PlayerType.human

    # Case #2: Computer has less cards so it wins.
    elif(len(human_hand) > len(computer_hand)):
        return PlayerType.computer

    # Case #3: Computer and player have same number of cards so
    # the person with the lowest value card in their hand wins.
    else:
        # If the minimum card is in the computer's hand, it won.
        # Otherwise the human player one.
        if(min(computer_hand) < min(human_hand)):
            return PlayerType.computer
        else:
            print PlayerType.human


def check_and_print_victory_conditions(human_hand, computer_hand):
    '''
    At the end of a game, this function checks to see which player one.
    After checking who won, it prints a message to the console.

    :params None.

    :returns: None.

    Only side effect is printing a message to the screen.

    >>> check_and_print_victory_conditions([], [5, 8, 9])
    You won.  However, you still are awful.
    >>> check_and_print_victory_conditions([], [5])
    You won.  However, you still are awful.
    >>> check_and_print_victory_conditions([5, 8, 9], [])
    The computer won. You are a huge loser.
    >>> check_and_print_victory_conditions([5, 50, 4], [2])
    The computer won. You are a huge loser.
    >>> check_and_print_victory_conditions([2, 800], [5, 50, 4])
    You won.  However, you still are awful.
    '''

    if(determine_winner(human_hand, computer_hand) == PlayerType.human):
        print "You won.  However, you still are awful."
    else:
        print "The computer won. You are a huge loser."


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


def get_special_move(previous_move_type, player_type):
    '''
    For specified special moves, this function returns the associated
    special move object.

    :param MoveType previous_move_type: Type of previous move made.
    :param PlayerType player_type: Current player either human or computer.

    :returns: Move object in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)
    '''
    #  Check for special move for queen of spades
    if(previous_move_type == MoveType.queen_of_spades):
        return create_move(player_type, 0, 0, 5)

    #  Check for special move for multiple twos
    if(previous_move_type == MoveType.one_two
       or previous_move_type == MoveType.two_twos
       or previous_move_type == MoveType.three_twos
       or previous_move_type == MoveType.four_twos):
        return create_move(player_type, 0, 0, previous_move_type)


def parse_move_string(previous_move_type, input_move, player,
                      hand, face_up_card, active_suit):
    '''
    This function parses a specified string and if it is a valid
    move it, returns that string.  Otherwise, it returns None.

    :param MoveType previous_move_type: Type of previous move made.
    :param str input_move: String specified as an input move
    :param PlayerType player: Current player either human (0) or computer (1)
    :param int hand: List of cards in the player's hand.
    :param int face_up_card: 0 to 51 for current face up card.
    :param int active_suit: 0 to 3 value of the suit.

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
    if(check_if_move_valid(previous_move_type, move, player, hand,
                           face_up_card, active_suit)):
        return move
    else:
        return None


def check_if_move_valid(previous_move_type, move, player,
                        hand, face_up_card, active_suit):
    '''
    This function parses a specified string and if it is a valid
    move it, returns that string.  Otherwise, it returns None.

    :param MoveType previous_move_type: Type of move made.
    :param str input_move: String specified as an input move
    :param PlayerType player: Current player either human (0) or computer (1)
    :param int hand: List of cards in the player's hand.
    :param int face_up_card: 0 to 51 for current face up card.
    :param int active_suit: 0 to 3 value of the suit.

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
    ValueError: active_suit must be between 0 and 3
    >>> check_if_move_valid(MoveType.normal_move,(1,40,0,0),1,[20,50,40],39,3)
    False
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
    >>> check_if_move_valid(MoveType.four_twos, (1, 0, 0, 8), 1, [3,1], 2,0)
    True
    >>> check_if_move_valid(MoveType.queen_of_spades, (1, 0, 0, 5),1,[1], 2,0)
    True
    >>> check_if_move_valid(MoveType.queen_of_spades, (1, 0, 0, 4),1,[1], 2,0)
    False
    >>> check_if_move_valid(MoveType.queen_of_spades, (1, 1, 0, 0),1,[1], 2,0)
    False
    >>> check_if_move_valid(MoveType.normal_move, (1, 7, 1, 0),1,[7,20], 2,0)
    True
    >>> check_if_move_valid(MoveType.normal_move, (1, 20, 3, 0),1,[20,7], 2,0)
    True
    >>> check_if_move_valid(MoveType.normal_move, (0, 4, 1, 0),0,[5,4],1,0)
    False
    >>> check_if_move_valid(MoveType.normal_move, (0, 4, 0, 0),0,[5,4],1,0)
    True
    '''

    # Check for valid input conditions.
    if(player != 0 and player != 1):
        raise ValueError("player must be either 0 or 1")
    if(len(hand) == 0):
        raise ValueError("The player's hand must have at least one card.")
    if(face_up_card < 0 or face_up_card > 51):
        raise ValueError("face_up_card must be between 0 and 51")
    if(active_suit < 0 or active_suit > 3):
        raise ValueError("active_suit must be between 0 and 3")

    # Extract some information on the move. This is used below.
    discarded_card = get_discard(move)
    specified_discard_suit = get_suit(move)
    numb_cards_to_draw = get_number_of_cards_to_draw(move)

    #  Check if the player in the move matches the expected value.
    if(get_player(move) != player):
        return False

    # Check special moves here.
    if(previous_move_type == MoveType.queen_of_spades):
        return move == get_special_move(MoveType.queen_of_spades, player)

    # Check the case where you need to draw cards.
    if(previous_move_type == MoveType.one_two
       or previous_move_type == MoveType.two_twos
       or previous_move_type == MoveType.three_twos):
        # If the player had to draw on a two, verify the move is valid.
        if(numb_cards_to_draw > 0):
            return move == get_special_move(previous_move_type, player)
        # Check if the move matches what was expected.
        else:
            return (get_card_rank(discarded_card) == MoveType.two
                    and get_card_suit(discarded_card) == get_suit(move))

    # If four two's played, next move must be a pickup.
    elif(previous_move_type == MoveType.four_twos):
        return move == get_special_move(previous_move_type, player)

    # Check the case where you need to draw cards.
    if(numb_cards_to_draw > 0):
        if(discarded_card == get_suit(move) == 0):
            return True
        else:
            return False

    # Check if the specified discarded card is in the player's hand.
    if(discarded_card not in hand):
        return False

    # You can play an 8 at any time.
    if(get_card_rank(discarded_card) == MoveType.eight):
        return True

    # Ensure if I am discarding a card, I specified the right suit.
    if(specified_discard_suit != get_card_suit(discarded_card)):
            return False

    # For a general discard, check if the suit and/or face card matches
    return (get_card_rank(discarded_card) == get_card_rank(face_up_card)
            or get_card_suit(discarded_card) == active_suit)


def parse_play_history(history):
    '''
    :param tuple history: List of tuples in the format:
                 (player_num, face_up_card, suit, number_of_cards)

    :returns: Tuple in the form (number_cards_player0, number_cards_player1,
                                 list_of_discarded_cards)

    >>> parse_play_history([(0,0,0,0)])
    (8, 8, [0])
    >>> parse_play_history([(0,1,2,0)])
    (8, 8, [1])
    >>> parse_play_history([(0,0,0,0),(1,0,0,1)])
    (8, 9, [0])
    >>> parse_play_history([(0,0,0,0),(1,0,0,1),(0,0,0,5)])
    (13, 9, [0])
    >>> parse_play_history([ (0,0,0,0),(1,0,0,1),(0,0,0,5),(1,13,1,0) ])
    (13, 8, [0, 13])
    >>> parse_play_history([ (0,39,3,0),(1,0,0,1),(0,0,0,5),(1,13,1,0) ])
    (13, 8, [39, 13])
    '''

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
        current_player = get_player(last_move)
        current_discard = get_discard(last_move)
        numb_drawn_cards = get_number_of_cards_to_draw(last_move)

        # If a card was drawn, then update cards per player
        if(numb_drawn_cards > 0):
            numb_cards_per_player[current_player] += numb_drawn_cards
        # Check in the case of a drawn card.
        elif(current_discard != previous_discard):
            previous_discard = current_discard
            discarded_cards.append(current_discard)
            numb_cards_per_player[current_player] -= 1

    # Return the play history.
    return (numb_cards_per_player[0], numb_cards_per_player[1],
            discarded_cards)


def build_available_card_list(hand, discarded_cards):
    '''
    Given the player's current hand and the list of discarded cards,
    build an array containing all unplayed cards.

    :param int hand: List of cards in the player's hand.
    :param int discarded_cards: List of discarded cards.

    :returns: List of all remaining cards not in the player's hand \
        and not yet played

    >>> build_available_card_list([],[])
    Traceback (most recent call last):
        ...
    ValueError: A player's hand must have at least 1 card.
    >>> build_available_card_list([3],[])
    Traceback (most recent call last):
        ...
    ValueError: discarded_cards must have at least 1 card.
    >>> build_available_card_list([3,4,5,3],[6,7,8,9,10])
    Traceback (most recent call last):
        ...
    RuntimeError: Data set error. A card in the hand and/or discarded card set\
 is duplicated.
    >>> build_available_card_list([3,4,5],[6,7,8,9,10,6])
    Traceback (most recent call last):
        ...
    RuntimeError: Data set error. A card in the hand and/or discarded card set\
 is duplicated.
    >>> build_available_card_list([3,4,5],[6,7,8,9,10,5])
    Traceback (most recent call last):
        ...
    RuntimeError: Data set error. A card in the hand and/or discarded card set\
 is duplicated.
    >>> build_available_card_list([32,4,3,44,11,7,8,9,30,20,34,18,17,16,15],\
[48,13,12,6,10,21,22,23,24,25,26,27,28])
    [0, 1, 2, 5, 14, 19, 29, 31, 33, 35, 36, 37, 38, 39, 40, 41,\
 42, 43, 45, 46, 47, 49, 50, 51]
    '''

    # The player must have at least card in his hand.
    if(len(hand) == 0):
        raise ValueError("A player's hand must have at least 1 card.")

    # Discarded cards must have at least one card.
    if(len(discarded_cards) == 0):
        raise ValueError("discarded_cards must have at least 1 card.")

    # Initially all cards available
    card_remaining = [True] * cards_per_deck

    # Iterate through all cards in the player hand and mark them not remaining
    for card in hand:
        # Check the card is not duplicated in the set.
        if(not card_remaining[card]):
            raise RuntimeError("Data set error. A card in the hand and/or "
                               + "discarded card set is duplicated.")
        card_remaining[card] = False

    # Iterate through all cards in discarded set and mark them not remaining
    for card in discarded_cards:
        # Check the card is not duplicated in the set.
        if(not card_remaining[card]):
            raise RuntimeError("Data set error. A card in the hand and/or "
                               + "discarded card set is duplicated.")
        card_remaining[card] = False

    # Initialize set of available cards.
    available_cards = []
    # Iterate through all the cards
    for i in range(0, cards_per_deck):
        if(card_remaining[i]):
            available_cards.append(i)

    # Check some array was built.
    if(len(available_cards) == 0):
        raise RuntimeError("When building the available card list, at the end "
                           + " it must have at least one element.")

    # Return the built array.
    return available_cards


def draw_cards(deck, max_numb_cards_to_draw):
    '''
    Function used to draw cards from the deck.

    :param int max_numb_cards_to_draw: Maximum number of cards the player is
        supposed to draw. The reason it is referred to as max is because there
        may not be enough cards on the deck for the size of the draw required.

    :returns: List of cards drawn from the deck.

    >>> draw_cards([], 4)
    Traceback (most recent call last):
        ...
    ValueError: Number of cards in the deck must be more than one
    >>> draw_cards([5,6,8,9,10,11], 4)
    ([11, 10, 9, 8], [5, 6])
    >>> draw_cards([10,11], 4)
    ([11, 10], [])
    >>> draw_cards([5,6,8,9,10,11], 2)
    ([11, 10], [5, 6, 8, 9])
    '''

    # Verify a valid deck
    if(len(deck) == 0):
        raise ValueError("Number of cards in the deck must be more than one")

    # Determine actual number of cards that will be drawn.
    numb_cards_to_draw = min(max_numb_cards_to_draw, len(deck))

    # Create array for drawn cards.
    drawn_cards = [None] * numb_cards_to_draw

    # Draw the cards off the deck
    for i in range(0, numb_cards_to_draw):
        drawn_cards[i] = deck.pop()

    # Return the drawn cards.
    return drawn_cards, deck


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
    ValueError: numb_drawn cards must be either 0, 1, 2, 4, 5, 6, or 8
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
       and numb_drawn_cards != 5 and numb_drawn_cards != 6
       and numb_drawn_cards != 8):
        raise ValueError("numb_drawn cards must be either 0, 1, 2, 4, 5, 6, "
                         + "or 8")
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

    # Ensure move is of expected size.
    if(len(move) != 4):
        raise ValueError("Move must be a tuple of length 4.")

    return move[0]


def get_discard(move):
    '''
    Extracts from a move the discarded card.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number for the discarded card.
    '''

    # Ensure move is of expected size.
    if(len(move) != 4):
        raise ValueError("Move must be a tuple of length 4.")

    return move[1]


def get_suit(move):
    '''
    Extracts from a move the currently active suit.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number for the current suit.
    '''

    # Ensure move is of expected size.
    if(len(move) != 4):
        raise ValueError("Move must be a tuple of length 4.")

    return move[2]


def get_number_of_cards_to_draw(move):
    '''
    Extracts from a move the number of cards to draw in this turn.

    :param Tuple move: Player move in the format:
        (player_numb, top_of_discard, suit, numb_drawn_cards)

    :returns: Integer number of cards to draw (>=0) in the form:
        (player_numb, top_of_discard, suit, numb_drawn_cards)
    '''

    # Ensure move is of expected size.
    if(len(move) != 4):
        raise ValueError("Move must be a tuple of length 4.")

    return move[3]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
