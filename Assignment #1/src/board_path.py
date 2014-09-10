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
    _goal_loc = None
    _untraversed_board = []
    _heuristic = ""
    _traversed_board = []

    def __init__(self, start_loc):
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
        other._path = self._path[:]
        other._current_loc = self._current_loc
        return other

    def get_current_location(self):
        """Current Location Accessor

        Function to get the current location for this path.

        :returns: Tuple of the current location in the format (row, column)
        """
        return self._current_loc

    def get_distance(self, heuristic=""):
        """Distance Calculator

        Flexible function for calculating the distance. Depending on the
        specified heuristic (either explicit in call or implicit with
        class), different distances can be returned for the same functions.

        :returns: Distance using the specified or class heuristic function.
        """
        # If no heuristic is specified, used the default
        if(heuristic == ""):
            heuristic = BoardPath._heuristic

        if(heuristic == "manhattan"):
            return self.calculate_manhattan_dist()
        elif(heuristic == "euclidean"):
            return self.calculate_euclidean_dist()
        elif(heuristic == "made_up"):
            return self.calculate_made_up_dist()
        else:
            assert False, "Invalid distance heuristic"

    def calculate_manhattan_dist(self):
        """Manhattan Distance Calculator

        Calculates difference between current location and\
        the goal location using Manhattan distance.

        :returns: A* Distance using Manhattan distance.
        """
        return self._current_cost + abs(self._current_loc.get_row() - self._goal_loc.get_row()) +\
            abs(self._current_loc.get_column() - self._goal_loc.get_column())

    def calculate_euclidean_dist(self):
        """Euclidean Distance Calculator

        Calculates difference between current location and\
        the goal location using Euclidean distance.

        Euclidean distance is defined as:
            = sqrt( (x2-x1)^2 + (y2-y1)^2 )

        :returns: A* Distance using Euclidean distance.
        """
        x_dist = self._current_loc.get_row() - self._goal_loc.get_row()
        y_dist = self._current_loc.get_column() - self._goal_loc.get_column()
        # Note ** is power operator in Python
        return self._current_cost + sqrt(x_dist**2 + y_dist**2)

    def calculate_made_up_dist(self):
        """Custom Zayd Special Distance Calculator

        Calculates difference between current location and\
        the goal location using Zayd's distance heuristic.

        :returns: A* Distance using Zayd's distance heuristic
        """

        # Ensure if current state equals goal, cost is only the current cost
        if self._goal_loc == self._current_loc:
            return self._current_cost

        # Start with the current cost so far as the foundation of A*
        heurstic_distance = self._current_cost

        # Distance is at least the Manhattan distance as cannot move diagonal
        manhattan_distance = self.calculate_manhattan_dist()

        # Update heuristic distance with minimum additional cost.
        heurstic_distance += manhattan_distance

        # In case where all neighboring spaces are blocked or already
        # traversed, then set the path cost prohibitively large so it is
        # given minimum priority.
        if not (self.is_move_valid("d", BoardPath._traversed_board)) \
                and not (self.is_move_valid("u", BoardPath._traversed_board)) \
                and not (self.is_move_valid("l", BoardPath._traversed_board)) \
                and not (self.is_move_valid("r", BoardPath._traversed_board)):
            # Total board area is sufficient as a prohibitive distance
            board_length = len(BoardPath._traversed_board)
            board_width = len(BoardPath._traversed_board[0])
            heurstic_distance += board_length * board_width
            return heurstic_distance

        # If all next steps that load directly to the goal are blocked, then
        # it takes at least two additional moves to get around it so add two
        # to the heuristic distance to include that cost.
        if self._is_all_direct_next_steps_blocked(BoardPath._traversed_board):
            heurstic_distance += 2

        # Return heuristic distance
        return heurstic_distance

    def _is_all_direct_next_paths_blocked(self, reference_board=None):
        """Direct Blocked Path Checker
        """
        # Use untraversed board if none is specified
        if reference_board is None:
            reference_board = BoardPath._untraversed_board

        # Case #1 - Goal and Current Location in the Same Row
        if self._current_loc.get_row() == self._goal_loc.get_row():
            # Case 1A - Need to move left but path is blocked
            if self._current_loc.get_column() > self._goal_loc.get_column() and\
                    not self.is_move_valid("l", reference_board):
                return True
            # Case 1B - Need to move left but path is blocked
            elif self._current_loc.get_column() < self._goal_loc.get_column() and\
                    not self.is_move_valid("r", reference_board):
                return True
            else:
                return False

        # Case #2 - Goal and Current Location in the Same Row
        if self._current_loc.get_column() == self._goal_loc.get_column():
            # Case 2A - Need to move left but path is blocked
            if self._current_loc.get_row() > self._goal_loc.get_row() and\
                    not self.is_move_valid("u", reference_board):
                return True
            # Case 1B - Need to move left but path is blocked
            elif self._current_loc.get_row() < self._goal_loc.get_row() and\
                    not self.is_move_valid("d", reference_board):
                return True
            else:
                return False

    def is_move_valid(self, direction, reference_board=None):
        """Mover Checker

        Verifies whether a move is valid for a given path.

        :param str direction:
            Possible values for direction are:
                * u - Moves one space up.
                * d - Moves one space down.
                * l - Moves one space left.
                * r - Moves one space right.
        """
        # Verify a left move does not take you off the board.
        if (direction == "l"):
            if (self._current_loc[1] == 0):
                return False
        # Verify an up move does not take you off the board.
        elif (direction == "u"):
            # Verify the move does not take you off the board.
            if (self._current_loc[0] == 0):
                return False
        # Verify a right move does not take you off the board.
        elif (direction == "r"):
            current_row = self._current_loc.get_row()
            max_column_number = len(self._untraversed_board[current_row])
            if self._current_loc.get_column() + 1 == max_column_number:
                return False
        # Verify a down move does not take you off the board.
        elif (direction == "d"):
            if self._current_loc.get_row() + 1 == len(self._untraversed_board):
                return False
        else:
            assert False, "Invalid move direction."

        #  Get the new location for a move in the specified direction.
        new_location = self._calculate_move_location(direction)
        new_row = new_location.get_row()
        new_col = new_location.get_column()
        #  Verify the space is available
        if(reference_board is None):
            return BoardPath._untraversed_board[new_row][new_col] != "#"
        else:
            return reference_board[new_row][new_col] != "#"

    def _calculate_move_location(self, direction):
        """Move Location Calculator

        Calculates the new location for a move in the specified direction.

        :param direction: String specifying the move direction.
            Possible values for direction are:
                * u - Moves one space up.
                * d - Moves one space down.
                * l - Moves one space left.
                * r - Moves one space right.

        :returns: Location: Location for the next move. If the direction
            is invalid, it returns the default location object
        """

        new_location = Location()

        # Calculate the new location for a left move
        if (direction == "l"):
            return (self._current_loc[0], self._current_loc[1] - 1)
        # Calculate the new location for an up move
        elif (direction == "u"):
            return (self._current_loc[0] - 1, self._current_loc[1])
        # Calculate the new location for a right move
        elif (direction == "r"):
            return (self._current_loc[0], self._current_loc[1] + 1)
        # Calculate the new location for a down move
        elif (direction == "d"):
            return (self._current_loc[0] + 1, self._current_loc[1])
        return (-1, -1)

    def move(self, direction):
        """Mover Function

        Moves the path to a new location.

        :param str direction:
            Possible values for direction are:
                * u - Moves one space up.
                * d - Moves one space down.
                * l - Moves one space left.
                * r - Moves one space right.
        """
        #  Ensure the move is valid
        assert self.is_move_valid(direction), "Tried to make an invalid move"
        #  Calculate the move location.
        self._current_loc = self._calculate_move_location(direction)
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
        return self._current_loc.get_row() == BoardPath._goal_loc.get_row() and \
            self._current_loc.get_column() == BoardPath._goal_loc.get_column()

    @staticmethod
    def set_goal(goal_loc):
        """Goal Setter

        This function sets the goal for the board.

        :param goal_loc: Board goal. Location object.
        """
        BoardPath._goal_loc = goal_loc

    @staticmethod
    def set_untraversed_board(board):
        """Untraversed Board Setter

        This function stores the untraversed board configuration.

        :param board: Two dimensional board.
        """
        BoardPath._untraversed_board = board

    @staticmethod
    def set_traversed_board(board):
        """Traversed Board Setter

        This function stores the traversed board configuration.

        :param board: Two dimensional board.
        """
        BoardPath._traversed_board = board

    @staticmethod
    def set_heuristic(heuristic):
        """Heuristic Setter

        This function stores the board path heuristic

        :param heuristic: Name of the heuristic approach.
            Valid values are "manhattan", "euclidean", and "made_up"
        """
        BoardPath._heuristic = heuristic

    def print_path(self):
        """Path Printer

        This function prints the object's path through the path to the console

        :returns: Nothing.
        """
        temp_board = self._untraversed_board
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

    def __lt__(self, other):
        """Less Than Operator

        Less than operator used for the distance of two BoardPath objects.

        :returns: True if the distance of self is less than other.
            False otherwise.
        """
        return self.get_distance() < other.get_distance()


'''
Created on Sep 10, 2014

@author: Zayd Hammoudeh
'''


class Location:

    def __init__(self, row_number=-1, column_number=-1):
        '''
        Constructor

        :param row_number: Integer Row Number of location
        :param column_number: Integer Column Number of location
        '''
        self._row_number = row_number
        self._column_number = column_number

    def get_row(self):
        """Row Number Accessor

        Accessor to get the row number of this location.

        :returns: Integer row number of this location
        """
        return self._row_number

    def get_column(self):
        """Column Number Accessor

        Accessor to get the column number of this location.

        :returns: Integer column number of this location
        """
        return self._column_number

    def is_valid(self):
        """Valid Location Checker

        Checks whether this location is valid.

        :returns: True if a valid location and False otherwise
        """
        if self.get_row() != -1 and self.get_column() != -1:
            return True
        else:
            return False

    def __eq__(self, other):
        """
        Special function for == operator
        """
        # Ensure same class and values match
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
