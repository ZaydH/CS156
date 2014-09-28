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


#  Define lists used for printing later.
card_rank_names = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
                   "Eight", "Nine", "Ten", "Jack", "Queen", "King")
suit_names = ("Spades", "Hearts", "Diamonds", "Clubs")
# cards_per_deck = 52


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

#     for i in range(0, cards_per_deck-1):
#         for j in range(i+1, cards_per_deck):
#             if(temp_deck[i] == temp_deck[j]):
#                 print "Duplicates at index " + str(i) + "and index " + str(j)

    # Return the temporary deck
    return temp_deck


def check_and_print_victory_conditions():
    '''
    At the end of a game, this function checks to see which player one.
    After checking who won, it prints a message to the console.

    :params None.

    :returns: None.

    Only side effect is printing a message to the screen.
    '''
    human_winning_string = "You won.  However, you still stink."
    computer_winning_string = "The computer won. You are a huge loser."

    # Case #1: Human has less cards so s/he wins.
    if(len(human_player_hand) < len(computer_player_hand)):
        print human_winning_string

    # Case #2: Computer has less cards so it wins.
    elif(len(human_player_hand) > len(computer_player_hand)):
        print computer_winning_string

    # Case #3: Computer and player have same number of cards so
    # the person with the lowest value card in their hand wins.
    else:
        # Set the minimum card value for both
        min_human_card = min_computer_card = cards_per_deck
        # Get the smallest card in the human player's hand.
        for i in range(0, len(human_player_hand)):
            # Check if current card is less than current minimum
            if(human_player_hand[i] < min_human_card):
                min_human_card = human_player_hand[i]

        # Get the smallest card in the computer player's hand.
        for i in range(0, len(computer_player_hand)):
            # Check if current card is less than current minimum
            if(computer_player_hand[i] < min_computer_card):
                min_computer_card = computer_player_hand[i]

        if(min_computer_card < min_human_card):
            print computer_winning_string
        else:
            print human_winning_string


# Build the deck for the game as well as the player's hands.
deck = build_initial_deck()
human_player_hand = draw_cards(deck, 8)
computer_player_hand = draw_cards(deck, 8)

# Sort the hand arrays.
human_player_hand.sort()
computer_player_hand.sort()

print "Welcome to the Wild, Weird, and Funky World of Crazy Eights.\n"
print "I am generous enough to give you the option to choose whether"
print " you want  go first or second.\n"

# Have the user enter whether they are going first or second.
entered_string = ""
first_time_in_loop = True
while(entered_string != "1" and entered_string != "2"):

    # If not the first time through the loop print an error message.
    if(not first_time_in_loop):
        print"\nInvalid entry.\n"
    first_time_in_loop = False

    #  Get the user input.
    entered_string = raw_input("To go first, type \"1\" and press enter. "
                               + "Otherwise to go second,\ntype \"2\" and "
                               + "press enter. Type your selection here:  ")
    print ""  # Print a blank line.

# Extract from what the user entered as play order
# the player marked in the initial move.
current_player = (int(entered_string) + 1) % 2

# Initialize the play history by taking one card off the deck.
face_up_card = draw_cards(1)[0]  # Draw a card to start the deck.
face_up_suit = get_card_suit(face_up_card)
# Store the last move in case special circumstances must be handled
last_move = create_move(current_player, face_up_card,
                        get_card_suit(face_up_card), 0)

# Add initial move to the history
play_history = [last_move]


#  Continue playing the game until the deck is empty.
while(len(deck) > 0 and len(human_player_hand) > 0
      and len(computer_player_hand) > 0):

    # Display the play history until this point.
    print "Current Play History:"
    print play_history, "\n"

    # Handle the player's turn
    if(current_player == PlayerType.human):
        print "Its your turn.",
        print "Your current hand is: ", human_player_hand, "\n"

        move_type = check_for_special_move_type(play_history)

        # Check if computer player a queen of spades on last play.
        if(move_type == MoveType.queen_of_spades):
            print "Your opponent played a queen of spades."
            print "You are forced to draw five cards."
            last_move = get_special_move(MoveType.queen_of_spades)
        else:

            # Last move will be set in the while loop.
            last_move = None
            # Keep looping until the player enters a valid move.
            while(last_move is None):

                input_move_string = raw_input("Enter your move in form (0, "
                                              + "card_number, card_suit, " +
                                              "number_cards_to_draw):\n")

                # Parse the specified string
                last_move = parse_move_string(move_type, input_move_string,
                                              PlayerType.human,
                                              human_player_hand,
                                              face_up_card, face_up_suit)

                # Check if the last move was valid.
                if(last_move is None):
                    print "The move you entered: ", input_move_string, \
                        " is invalid."
                    print "Enter a valid move and try again.\n"

    # Handle the computer's turn
    elif(current_player == PlayerType.computer):
        #  Define the partial state.
        partial_state = (face_up_card, face_up_suit,
                         computer_player_hand, play_history)

        #  Extract the computer's move.
        last_move = CrazyEight.move(partial_state)

        # Print the turn
        print "Computer's Turn:\n"
        print "The computer's move was: ", last_move

    # Append this move to the play history.
    play_history += [last_move]

    # Get if any ca1rds need to be drawn in this turn.
    numb_cards_to_draw = get_number_of_cards_to_draw(last_move)
    # If cards need to be drawn, then draw them from the deck.
    if(numb_cards_to_draw > 0):
        # Check if the current player is the computer
        if(current_player == PlayerType.computer):
            computer_player_hand += draw_cards(deck, numb_cards_to_draw)
        # Check if the current player is the human
        elif(current_player == PlayerType.human):
            # Extract the cards to be drawn by the player.
            drawn_cards = draw_cards(deck, numb_cards_to_draw)
            if(numb_cards_to_draw > 1):
                print "You drew cards: ", drawn_cards
            else:
                print "You drew card: ", drawn_cards
            # Add the drawn cards to the player's hand
            human_player_hand += drawn_cards

    #  Check if on the last turn a player discarded a card
    discarded_card = get_discard(play_history[len(play_history) - 1])
    if(discarded_card != 0 and numb_cards_to_draw == 0):
        # Store the discarded card and get its suit
        face_up_card = discarded_card
        face_up_suit = get_card_suit(face_up_card)

        if(current_player == PlayerType.human):
            human_player_hand.remove(discarded_card)
        elif(current_player == PlayerType.computer):
            computer_player_hand.remove(discarded_card)

    # Switch to the next player only if last card played was not a jack.
    if(check_for_special_move_type(play_history) != MoveType.jack):
        current_player = (current_player+1) % 2

# Once the deck is empty, check and print who won.
check_and_print_victory_conditions()
