'''
Created on Aug 30, 2014

@author: Zayd Hammoudeh
'''

from math import sqrt


class BoardPath:
    """Board Path Class

    This class manages a path through the board.

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
        self._path = []
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
            abs(self._current_loc(1) - self._goal_loc(1))

    def calculate_euclidean_dist(self):
        """Manhattan Distance Calculator

        Calculates difference between current location and\
        the goal location using Manhattan distance.

        :returns: A* Distance using Manhattan distance.
        """
        x_dist = self._current_loc(0) - self._goal_loc(0)
        y_dist = self._current_loc(1) - self._goal_loc(1)
        # Note ** is power operator in Python
        return self._current_cost + sqrt(x_dist**2 + y_dist**2)

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
            assert self._current_loc[1] > 0,\
                "You tried to move off the left edge of the board."
            # Update the current location
            self._current_loc = (self._current_loc[0],
                                 self._current_loc[1] - 1)

        elif (direction == "u"):
            # Verify the move does not take you off the board.
            assert self._current_loc[0] > 0,\
                "You tried to move off the top of the board."
            # Update the current location
            self._current_loc = (self._current_loc[0] - 1,
                                 self._current_loc[1])

        elif (direction == "r"):
            current_row = self._current_loc[0]
            # Verify the move does not take you off the board.
            assert self._current_loc[1] + 1 < len(self._board[current_row]),\
                "You tried to move off the right edge of the board."
            # Update the current location
            self._current_loc = (self._current_loc[0],
                                 self._current_loc[1] + 1)

        elif (direction == "d"):
            # Verify the move does not take you off the board.
            assert self._current_loc[0] + 1 < len(self._board),\
                "You tried to move off the bottom of the board."
            # Update the current location
            self._current_loc = (self._current_loc[0] + 1,
                                 self._current_loc[1])

        else:
            assert False, "Invalid move direction."

        # Update the path.
        self._path.append(self._current_loc)
        # Increment the move cost.
        self._current_cost = self._current_cost + 1

    def is_at_goal(self):
        """Goal Checker

        This function checks if the goal has been reached.

        :returns:
            **True** if at the goal
            **False** otherwise
        """
        return (self._current_loc[0] == self._goal_loc[0] and
                self._current_loc[1] == self.goal_loc[1])

    @staticmethod
    def set_goal(goal_loc):
        """Goal Setter

        This function sets the goal for the board.

        :param goal_loc: Board goal. Tuple in format (row, column)
        """
        BoardPath._goal_loc = goal_loc

    @staticmethod
    def set_board(board):
        """Board Setter

        This function stores the board configuration.

        :param board: Two dimensional board.
        """
        BoardPath._board = board

    def print_path(self):
        """Path Printer

        This function prints the object's path through the path to the console

        :returns: Nothing.
        """
        temp_board = self._board
        step_numb = 0
        prev_row = -1
        prev_col = -1
        # Iterate through each board configuration.
        for loc in self._path:
            # Depending on if this is the initial setup or not
            # Process the next print out.
            if (step_numb == 0):
                print "Initial:"
            else:
                temp_board[prev_row][prev_col] = "."
                temp_board[loc[0]][loc[1]] = "@"
                # Print the step number
                print ""
                print "Step {0}:".format(step_numb)

            #  Print the board
            for board_row in temp_board:
                # Build the string from the array then print it
                board_str = "".join(board_row)
                print board_str

            #  Store the previous location for next time through the loop.
            prev_row = loc[0]
            prev_col = loc[1]
            step_numb += 1

        #  Check if the target is reached
        final_loc = self._path[len(self._path) - 1]
        if (final_loc == self._goal_loc):
            print "Problem Solved! I had some noodles!"
