'''
Created on Aug 30, 2014

@author: Zayd Hammoudeh

Team Member #1: Zayd Hammoudeh (009418877)
Team Member #2: Muffins Hammoudeh
        (No student ID - she's my cat but was here with me
        while I worked so she deserves credit).
'''

import heapq
from board_path import BoardPath
from board_path import Location
import sys
import os.path


def parse_board_file(filename):
    """Board File Parser

    This function parses the specified board file.

    :param str filename: Path to the board file.

    :returns: A tuple containing the following
        board: This is the parsed board file.
        start_loc: Location from where to start the search.
        goal_loc: Location from where to end the search.
    """

    # Ensure the file exists.
    if(not os.path.isfile(filename)):
        sys.exit()

    #  Open the board file.
    board_file = open(filename, "r")
    #  Extract the board file as strings.
    file_lines = board_file.readlines()
    #  Close the output file.
    board_file.close()

    # Define variables used when building the board.
    board = []
    row = 0

    start_loc = Location()  # If valid start location exist this is overwritten
    goal_loc = Location()  # If a valid goal location exist this is overwritten

    #  Create the board
    for line in file_lines:
        embedded_array = []
        col = -1  # Start at -1 since auto-incremented.
        #  Iterate through the board file.
        for character in line:
            # If the character is not newline, add it to the board and parse it
            if character != "\n":
                col = col + 1  # Increment the column number.
                embedded_array.append(character)
                # Parse for special characters
                if character == "@":
                    # Ensure only one start location per file.
                    if start_loc.is_valid():
                        sys.exit()
                    start_loc = Location(row, col)
                elif character == "%":
                    # Ensure only one goal per file
                    if goal_loc.is_valid():
                        sys.exit()
                    goal_loc = Location(row, col)
                elif character != "." and character != "\n"\
                        and character != "#":
                    # Exit in the case of an invalid character.
                    sys.exit()

        # Append the board row to the board and increment the row counter
        board.append(embedded_array)
        row = row + 1
    # Ensure a valid starting location was specified in the board file.
    if (not start_loc.is_valid()):
        sys.exit()  # Exit the program

    # Ensure a valid goal location was specified in the board file.
    if (not goal_loc.is_valid()):
        sys.exit()  # Exit the program

    return (board, start_loc, goal_loc)
#  def parse_board_file(filename)


def perform_a_star_algorithm_search(untraversed_board, start_loc, goal_loc,
                                    heuristic):
    """A* Algorithm

    This function runs the A* algorithm on the specified untraversed board with
    specified start and goal locations and heuristic function name.
    """
    # Store the board as it is traversed. Must do a deep copy
    traversed_board = []
    for board_row in untraversed_board:
        traversed_board.append(list(board_row))

    # Store the board information
    BoardPath.set_untraversed_board(untraversed_board)
    BoardPath.set_goal(goal_loc)
    BoardPath.set_heuristic(heuristic)
    # Initially untraversed and traversed board are the same
    BoardPath.set_traversed_board(untraversed_board)

    # Build the priority queue.
    priority_queue = []

    #  Queue the starting point of the search
    heapq.heappush(priority_queue, BoardPath(start_loc))
    # Mark the starting point checked
    traversed_board[start_loc.get_row()][start_loc.get_column()] = "#"

    #  Continue iterating through the priority queue until the shortest cost
    #  path is found or the queue is empty.
    while len(priority_queue) > 0:
        path = heapq.heappop(priority_queue)
        #  If at the goal, you are done.
        if(path.is_at_goal()):
            path.print_path()
            sys.exit()

        #  Specify the valid move directions
        move_dir = ["r", "d", "l", "u"]
        #  Iterate through the move directions and valid moves
        for direction in move_dir:
            if (path.is_move_valid(direction, traversed_board)):
                # Move is valid so add this path to the priority queue
                new_path = path.clone()
                new_path.move(direction)
                heapq.heappush(priority_queue, new_path)

                # Mark the space for this space as now blocked.
                new_location = new_path.get_current_location()
                new_row = new_location.get_row()
                new_column = new_location.get_column()
                traversed_board[new_row][new_column] = "#"
                # Update the traversed board for the BoardPath class
                BoardPath.set_traversed_board(traversed_board)
    # Return since no path was found.
    return None


#  Ensure a sufficient number of input arguments are specified.
if len(sys.argv) != 2 + 1:  # First argument is the script itself
    sys.exit()  # Exit the program


# Extract the board file path.
board_file_path = sys.argv[1]

# Extract the heuristic function.
heuristic = sys.argv[2]
if (heuristic != "manhattan" and
        heuristic != "euclidean" and
        heuristic != "made_up"):
    # print "Invalid heuristics function."
    # "That is too sad. I must quit. This hurts me as much as it hurts you."
    sys.exit()  # Exit the program

# Parse the board file.
[original_board, start_loc, goal_loc] = parse_board_file(board_file_path)

perform_a_star_algorithm_search(original_board, start_loc, goal_loc, heuristic)
