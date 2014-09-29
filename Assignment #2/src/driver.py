'''
Created on September 26, 2014

@author: Zayd Hammoudeh

Team Member #1: Zayd Hammoudeh (009418877)
Team Member #2: Muffins Hammoudeh
        (No student ID - she's my cat but was here with me
        while I worked so she deserves credit).
'''

# import everything from the crazy eights file.
from crazy_eights import *


def build_initial_deck():
    '''
    Builds the initial deck of cards.

    :returns: List of 52 cards shuffled.
    '''
    # Initialize the array
    temp_deck = [None] * cards_per_deck

    # Load the deck
    for i in range(0, cards_per_deck):
        temp_deck[i] = i

    # Shuffle the temporary deck
    shuffle_deck(temp_deck)

    # Return the temporary deck
    return temp_deck


def perform_human_player_move(player, player_hand, face_up_card, active_suit):
    '''
    :returns: Move - The human player's move.
    '''
    # Print the initial information.
    print "Its your turn player #" + str(player)
    print "Your hand (using card ID format) is: ", player_hand
    print_player_hand(player, player_hand)
    previous_move_type = check_for_special_move_type(play_history)

    # Check if computer player a queen of spades on last play.
    if(previous_move_type == MoveType.queen_of_spades):
        print "Your opponent played a queen of spades."
        print "You are forced to draw five cards."
        human_player_move = get_special_move(MoveType.queen_of_spades,
                                             PlayerType.human)

    # For other plays, player is not forced to move.
    else:

        # Last move will be set in the while loop.
        human_player_move = None
        # Keep looping until the player enters a valid move.
        while(human_player_move is None):

            input_move_string = raw_input("Enter your move in form ("
                                          + str(player) + ", card_number, "
                                          + "card_suit, number_cards_to_draw):"
                                          + "\n")

            # Parse the specified string
            human_player_move = parse_move_string(previous_move_type,
                                                  input_move_string, player,
                                                  player_hand, face_up_card,
                                                  active_suit)

            # Check if the last move was valid.
            if(human_player_move is None):
                print ("The move you entered: " + str(input_move_string)
                       + " is invalid.")
                print "Enter a valid move and try again.\n"

    # Print the selected move.
    print_move_action(human_player_move)

    # Return the move made by the player.
    return human_player_move


# Build the deck for the game as well as the player's hands.
game_deck = build_initial_deck()

if(enable_debug_actions):
    # For debug purposes, display the starting game_deck.
    print "The game deck is: ", game_deck

human_player_hand, game_deck = draw_cards(game_deck, 8)
computer_player_hand, game_deck = draw_cards(game_deck, 8)

# Sort the hand arrays.
human_player_hand.sort()
computer_player_hand.sort()

print "Welcome to the Wild, Weird, and Funky World of Crazy Eights.\n"
print "I am generous enough to give you the option to choose whether"
print "you want to go first or second.\n"

# Have the user enter whether they are going first or second.
entered_string = ""
first_time_in_loop = True
while(entered_string != "1" and entered_string != "2"):

    # If not the first time through the loop print an error message.
    if(not first_time_in_loop):
        print"Invalid entry.\n"
    first_time_in_loop = False

    #  Get the user input.
    entered_string = raw_input("To go first, type \"1\" and press enter. "
                               + "Otherwise to go second,\ntype \"2\" and "
                               + "press enter. Type your selection here:  ")

# Extract from what the user entered as play order
# the player marked in the initial move.
current_player = (int(entered_string) + 1) % 2

# Initialize the play history by taking one card off the deck.
drawn_cards, game_deck = draw_cards(game_deck, 1)  # Draw first discard.
face_up_card = drawn_cards[0]
# Only for first play is the active suit guaranteed to be face card suit
active_suit = get_card_suit(face_up_card)
# Store the last move in case special circumstances must be handled
last_move = create_move((current_player+1) % 2, face_up_card,
                        get_card_suit(face_up_card), 0)

# Add initial move to the history
play_history = [last_move]
# Print the initial move for improved human readability.
rank_string = card_rank_names[get_card_rank(face_up_card)]
suit_string = suit_names[active_suit]
print "\n\nThe start of the discard pile is a " + rank_string + " with suit " \
      + suit_string + " [" + str(active_suit) + "]."


#  Continue playing the game until the deck is empty.
while(not at_game_end(game_deck, human_player_hand, computer_player_hand)):

    # Display the play history until this point.
    print "\nCurrent Play History:"
    print play_history
    # Under certain circumstances print the number of cars in the game deck.
    if(enable_debug_actions or len(game_deck) <= 5):
        print "There are " + str(len(game_deck)) + " cards left in the deck."
    print "\n"

    # Handle the player's turn
    if(current_player == PlayerType.human):

        # Perform the human player's turn.
        last_move = perform_human_player_move(PlayerType.human,
                                              human_player_hand,
                                              face_up_card,
                                              active_suit)

    # Handle the computer's turn
    elif(current_player == PlayerType.computer):

        # Print the turn
        print "Computer's Turn:"

        if(enable_debug_actions):
            # During debug, print the computer player's hand for tracking.
            print_player_hand(PlayerType.computer, computer_player_hand)

        #  Define the partial state.
        partial_state = (face_up_card, active_suit,
                         computer_player_hand, play_history)
        #  Extract the computer's move.
        last_move = CrazyEight.move(partial_state)
        # Print the selected move.
        print "The computer's move was: ", last_move
        print_move_action(last_move)
        # If the computer's hand has three or less cards, print the number
        if(len(computer_player_hand) <= 3):
            card_str = " card"
            # If more than one card print plural.
            if(len(computer_player_hand) > 1):
                card_str += "s"
            # Print the number of cards the computer has.
            print "The computer has " + str(len(computer_player_hand)) \
                  + card_str

    # Append this move to the play history.
    play_history += [last_move]

    # Get if any ca1rds need to be drawn in this turn.
    SimplifiedState.process_card_drawing(last_move, game_deck,
                                         human_player_hand,
                                         computer_player_hand, True)

    #  Check if on the last turn a player discarded a card
    face_up_card, active_suit =\
        SimplifiedState.process_discarded_card(last_move, human_player_hand,
                                               computer_player_hand,
                                               face_up_card, active_suit)

    if(enable_debug_actions):
        # For debug show the player hands.
        print_player_hand(PlayerType.human, human_player_hand)
        print_player_hand(PlayerType.computer, computer_player_hand)

    # Switch to the next player only if last card played was not a jack.
    if(check_for_special_move_type(play_history) != MoveType.jack):
        current_player = SimplifiedState.update_next_player(current_player)
    else:
        if(current_player == PlayerType.computer):
            print "\n\nThe computer player a jack so you lose your turn.\n"
        else:
            print "\n\nThe computer lost its turn because you played a jack.\n"

# Once the deck is empty, check and print who won.
check_and_print_victory_conditions(human_player_hand, computer_player_hand)
