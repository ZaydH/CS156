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
cards_per_deck = 52


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


def draw_cards(max_numb_cards_to_draw):
    '''
    Function used to draw cards from the deck.

    :param int max_numb_cards_to_draw: Maximum number of cards the player is
        supposed to draw. The reason it is referred to as max is because there
        may not be enough cards on the deck for the size of the draw required.

    :returns: List of cards drawn from the deck.
    '''

    # Determine actual number of cards that will be drawn.
    numb_cards_to_draw = min(max_numb_cards_to_draw, len(deck))

    # Create array for drawn cards.
    drawn_cards = [None] * numb_cards_to_draw

    # Draw the cards off the deck
    for i in range(0, numb_cards_to_draw):
        drawn_cards[i] = deck.pop()

    # Return the drawn cards.
    return drawn_cards


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
human_player_hand = draw_cards(8)
computer_player_hand = draw_cards(8)


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

# Extract from what the user entered as play order
# the player marked in the initial move.
current_player = int(entered_string) - 1


# Initialize the play history by taking one card off the deck.
next_card = draw_cards(1)[0]  # Draw a card to start the deck.
# Store the last move in case special circumstances must be handled
last_move = create_move(current_player, next_card,
                        determine_card_suit(next_card), 0)
# Add initial move to the history
play_history = [last_move]
print play_history


#  Continue playing the game until the deck is empty.
while(len(deck) > 0 and len(human_player_hand) > 0
      and len(computer_player_hand) > 0):

    # Get if any cards need to be drawn in this turn.
    numb_cards_to_draw = get_number_of_cards_to_draw(last_move)
    # If cards need to be drawn, then draw them from the deck.
    if(numb_cards_to_draw > 0):
        # Check if the current player is the computer
        if(current_player == 0):
            computer_player_hand += draw_cards(numb_cards_to_draw)
        # Check if the current player is the human
        elif(current_player == 1):
            # Extract the cards to be drawn by the player.
            drawn_cards = draw_cards(numb_cards_to_draw)
            if(numb_cards_to_draw > 1):
                print "You drew cards: " + drawn_cards
            else:
                print "You drew card: " + drawn_cards
            # Add the drawn cards to the player's hand
            human_player_hand += drawn_cards

    # Switch to the next player.
    current_player = (current_player+1) % 2

# Once the deck is empty, check and print who won.
check_and_print_victory_conditions()
