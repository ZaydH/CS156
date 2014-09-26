'''
Created on September 26, 2014

@author: Zayd Hammoudeh

Team Member #1: Zayd Hammoudeh (009418877)
Team Member #2: Muffins Hammoudeh
        (No student ID - she's my cat but was here with me
        while I worked so she deserves credit).
'''


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


# import everything from the crazy eights file.
from crazy_eights import *


#  Define lists used for printing later.
card_rank_names = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
                   "Eight", "Nine", "Ten", "Jack", "Queen", "King")
suit_names = ("Spades", "Hearts", "Diamonds", "Clubs")
cards_per_deck = 52


# Define empty array for the starting hands.
human_player_hand = []
computer_player_hand = []

print "Welcome to the Wild, Weird, and Funky World of Crazy Eights."

print build_initial_deck()

