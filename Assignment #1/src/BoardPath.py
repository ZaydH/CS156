'''
Created on Aug 30, 2014

@author: Zayd Hammoudeh
'''

import sys


class BoardPath:
    """
    classdocs
    """
    #  These are the class "static" style variables.
    _goal_loc = ()
    _board = []

    def __init__(self, start_loc=(-1, -1)):
        '''
        Constructor
        '''
        self._current_cost = 0
        self._current_loc = start_loc
        self._path.append(start_loc)

    def clone(self):
        """Board Path Cloner
        This function is used to clone the BoardPath object.
        :returns: Cloned BoardPath object
        """
        #  Run the constructor.
        other = BoardPath()
        #  Copy the object variables
        other._current_cost = self._current_cost
        other._path = self._path
        other._current_loc = self._current_loc
        return other

    def calculate_manhattan_dist(self):
        """Manhattan Distance Calculator

        Calculates difference between current location and\
        the goal location using Manhattan distance.

        :returns: A* Distance using Manhattan distance.
        """
        return self._current_cost + abs(self._current_loc(0) - self._goal_loc(0)) +\
            abs(self._current_loc(1) - self._goal_loc(1))  # Y Difference

    def move(self, direction):
        """Mover Function

        :param str direction:
            Possible values for direction are:
                * u - Moves one space up.
                * d - Moves one space down.
                * l - Moves one space left.
                * r - Moves one space right.
        """
        if (direction == "l"):
            # Verify the move does not take you off the board.
            if(self._current_loc(0) == 0):
                print "Error: You tried to move off the left edge of the board."\
                    "Self Destructing."
                sys.exit()
            # Update the current location
            self._current_loc = (self._current_loc(0)-1, self._current_loc(1))

        elif (direction == "u"):
            # Verify the move does not take you off the board.
            if(self._current_loc(1) == 0):
                print "Error: You tried to move off the top of the board."\
                    "Self Destructing."
                sys.exit()
            # Update the current location
            self._current_loc = (self._current_loc(0),
                                 self._current_loc(1)-1)

        elif (direction == "r"):
            current_row = self._current_loc(0)
            # Verify the move does not take you off the board.
            assert self._current_loc(0) + 1 < len(self._board[current_row]),\
                "Error: You tried to move off the right edge of the board."\
                "Self Destructing."
            
            # Update the current location
            self._current_loc = (self._current_loc(0) + 1,
                                 self._current_loc(1)-1)
        else
            print "Error: You tried to move off the right edge of the board."\
                "Self Destructing."
            sys.exit()

        # Update the path.
        self._path.add(self._current_loc)
        # Increment the move cost.
        self._current_cost = self._current_cost + 1
