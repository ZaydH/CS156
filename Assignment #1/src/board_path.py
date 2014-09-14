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
    _traversed_board_size = -1

    def __init__(self, start_loc=None):
        '''
        Constructor
        '''

        # If no start location is specified, use a dummy one
        if(start_loc is None):
            start_loc = Location()

        # Create object variables
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
        x_dist = self._current_loc.get_column() - self._goal_loc.get_column()
        y_dist = self._current_loc.get_row() - self._goal_loc.get_row()
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

        # Distance is at least the Manhattan distance as cannot move diagonal
        heuristic_distance = self.calculate_manhattan_dist()

        # Assume two board parts in the priority queue have the same weight.
        # For those board paths with higher actual cost and lower estimated
        # cost, there is more assurance in the accuracy of the actual cost
        # than in the estimated cost.  Give a very small penalty (i.e. less
        # than one step) to prefer a path with a higher known cost than a
        # path with a higher estimated cost.
        # Extract the number of portion of the move cost that is estimated
        estimated_cost = heuristic_distance - self._current_cost
        # Estimated cost penalty is normalized to a maximum of 0.1 steps
        # This is achieved by dividing the estimate cost by the size of the
        # board. Since the estimated cost can never be larger than the board
        # size, this is less than or equal to 1. To normalize to a maximum of
        # 0.1, just multiply the number by 0.1.  This is than added to the
        # heuristic distance determined so far.
        estimated_cost_penalty = 0.1 * estimated_cost
        estimated_cost_penalty /= BoardPath._traversed_board_size
        # Add what is essentially an "uncertainty penalty"
        heuristic_distance += estimated_cost_penalty

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
            heuristic_distance += board_length * board_width
            return heuristic_distance

        # If all next steps that load directly to the goal are blocked, then
        # it takes at least two additional moves to get around the blocked
        # paths it (due to an obstacle or already traversed square) so add
        # two to the heuristic distance to include that cost.
        if self._is_all_direct_next_moves_blocked(BoardPath._traversed_board):
            heuristic_distance += 2

        # In a heap, if two nodes have the same cost, the object that was
        # put into the heap first in many implementations will be on top of the
        # heap. To make the algorithm more efficient, apply a slight penalty to
        # a non valid solution to ensure if an invalid solution and a valid
        # solution have the same cost that the valid solution would always be
        # on top of the heap. This is done by giving all non-valid solutions a
        # penalty term that is greater than zero and less than the minimum step
        # size (e.g. in this case 0 < 0.1 < 1).
        heuristic_distance += 0.1

        # Return heuristic distance
        return heuristic_distance

    def _is_all_direct_next_moves_blocked(self, reference_board=None):
        """Direct Blocked Path Checker

        This function checks whether if all direct next moves from the
        current location are blocked by an unpassable object or the
        edge of the board.  This can be used to determine a penalty
        factor when calculating the heuristic.

        This function is used in the made_up heuristics function.

        :returns: True if next move is blocked and False otherwise
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
        # Case #3 - Goal and current location are diagonal from one another
        else:
            number_invalid_conditions = 0
            # Case 3A - Check if need to move down but it is blocked
            if self._current_loc.get_row() < self._goal_loc.get_row() \
                    and not self.is_move_valid("d", reference_board):
                number_invalid_conditions += 1
            # Case 3B - Check if need to move up but it is blocked
            if self._current_loc.get_row() > self._goal_loc.get_row() \
                    and not self.is_move_valid("u", reference_board):
                number_invalid_conditions += 1
            # Case 3C - Check if need to move right but it is blocked
            if self._current_loc.get_column() < self._goal_loc.get_column() \
                    and not self.is_move_valid("r", reference_board):
                number_invalid_conditions += 1
            # Case 3D - Check if need to move left but it is blocked
            if self._current_loc.get_column() > self._goal_loc.get_column() \
                    and not self.is_move_valid("l", reference_board):
                number_invalid_conditions += 1
            # Only two direct moves when need to move diagonal. If invalid
            # count equals two, then return true as condition met.
            if number_invalid_conditions == 2:
                return True
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
            if (self._current_loc.get_column() == 0):
                return False
        # Verify an up move does not take you off the board.
        elif (direction == "u"):
            # Verify the move does not take you off the board.
            if (self._current_loc.get_row() == 0):
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
        current_row = self._current_loc.get_row()
        current_column = self._current_loc.get_column()

        # Calculate the new location for a left move
        if (direction == "l"):
            return Location(current_row, current_column - 1)
        # Calculate the new location for an up move
        elif (direction == "u"):
            return Location(current_row - 1, current_column)
        # Calculate the new location for a right move
        elif (direction == "r"):
            return Location(current_row, current_column + 1)
        # Calculate the new location for a down move
        elif (direction == "d"):
            return Location(current_row + 1, current_column)
        return Location()

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
        # Extract the size of the traversed board
        # This is stored and used in "made_up" heuristic analysis
        BoardPath._traversed_board_size = 0
        for board_row in board:
            BoardPath._traversed_board_size += len(board_row)

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
                temp_board[loc.get_row()][loc.get_column()] = "@"
                # Print the step number
                print ""
                print "Step {0}:".format(step_numb)

            #  Print the board
            for board_row in temp_board:
                # Build the string from the array then print it
                board_str = "".join(board_row)
                print board_str

            #  Store the previous location for next time through the loop.
            prev_row = loc.get_row()
            prev_col = loc.get_column()
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

    def __ne__(self, other):
        """
        Special function for != operator
        """
        return not (self == other)
