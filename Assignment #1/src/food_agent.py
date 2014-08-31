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
import sys


# def build_game_board(filename):
#     """
#     Function used to create a board file.
#     """
#     board_file = open(filename, "w")
#     board_file.write("@..#\n")
#     board_file.write("#.%#")
#     board_file.close()
#
#
#
# build_game_board("test.txt")
#
#
# def build_game_board2(filename):
#     """
#     Function used to create a board file.
#     """
#     board_file = open(filename, "w")
#     board_file.write(".......\n")
#     board_file.write(".#####.\n")
#     board_file.write(".#.....\n")
#     board_file.write(".#.###.\n")
#     board_file.write(".#.@.#%\n")
#     board_file.write(".###.##\n")
#     board_file.write("......#")
#     board_file.close()
# build_game_board2("test2.txt")
#
#
# def build_game_board3(filename):
#     """
#     Function used to create a board file.
#     """
#     board_file = open(filename, "w")
#     board_file.write("@#%")
#     board_file.close()
# build_game_board3("test3.txt")


def parse_board_file(filename):
    """Board File Parser

    This function parses the specified board file.

    :param str filename: Path to the board file.

    :returns: A tuple containing the following
        board: This is the parsed board file.
        start_loc: Location from where to start the search.
        goal_loc: Location from where to end the search.
    """
    #  Open the board file.
    board_file = open(filename, "r")
    #  Extract the board file as strings.
    file_lines = board_file.readlines()
    #  Close the output file.
    board_file.close()

    # Define variables used when building the board.
    board = []
    row = 0

    start_loc = (-1, -1)  # If valid start location exist, this is overwritten
    goal_loc = (-1, -1)  # If a valid goal location exist, this is overwritten

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
                    start_loc = (row, col)
                if character == "%":
                    goal_loc = (row, col)

        # Append the board row to the board and increment the row counter
        board.append(embedded_array)
        row = row + 1
    # Ensure a valid starting location was specified in the board file.
    if (start_loc[0] == -1 and start_loc[1] == -1):
        # print "No valid starting location in this puzzle, which " + \
        #     "makes it unsolvable."
        # print "That is too sad.  I must quit."
        sys.exit()  # Exit the program

    # Ensure a valid goal location was specified in the board file.
    if (goal_loc[0] == -1 and goal_loc[1] == -1):
        # print "No valid goal location in this puzzle making it unsolvable."
        # print "This is so sad. I must quit. This hurts me as " + \
        #     "much as it hurts you."
        sys.exit()  # Exit the program

    return (board, start_loc, goal_loc)
#  def parse_board_file(filename)


def perform_a_star_algorithm_search(board, start_loc, goal_loc, heuristic):

    # Store the board as it is traversed. Must do a deep copy
    traversed_board = []
    for board_row in board:
        traversed_board.append(list(board_row))

    # Store the board information
    BoardPath.set_board(board)
    BoardPath.set_goal(goal_loc)
    BoardPath.set_heuristic(heuristic)

    # Build the priority queue.
    priority_queue = []

    #  Queue the starting point of the search
    heapq.heappush(priority_queue, BoardPath(start_loc))
    # Mark the starting point checked
    traversed_board[start_loc[0]][start_loc[1]] = "#"

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
                traversed_board[new_location[0]][new_location[1]] = "#"
    # Return since no path was found.
    return None


#  Ensure a sufficient number of input arguments.
if len(sys.argv) != 2 + 1:  # First argument is the script itself
    print "The function expects requires exactly two input arguments."
    print "You specified " + str(len(sys.argv)-1) + " input arguments."
    print "This is so sad. I must quit. This hurts me as much as it hurts you."
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
