import sys

#     
# #---------------------------------------------------#
# #     Function used to create a board file.         #
# #---------------------------------------------------#
# def build_game_board(filename):
#     board_file = open(filename, "w")
#     board_file.write("@..#\n")
#     board_file.write("#.%#")
#     board_file.close()
#     
# 
# 
# build_game_board("test.txt")

#------------------------------------------------------------#
#  This function parses the board file.                      
#  
#  Input Parameters:                                    
#    filename: Path to the board file name.
#
#  Return Values:
#    board: This is the parsed board file.
#    start_loc: Location from where to start the search.
#    goal_loc: Location from where to end the search.
#    
#------------------------------------------------------------#
def parse_board_file(filename):
    #---- Open the board file.
    board_file = open(filename, "r")
    #----- Extract the board file as strings.
    file_lines = board_file.readlines()
    #----- Close the output file.
    board_file.close()
       
    # Define variables used when building the board.
    board = []
    row = 0
    start_loc = (-1, -1) # If a valid starting location is found, then it is overwritten
    goal_loc = (-1, -1) # If a valid goal location is found, then it is overwritten
    
    # Create the board 
    for line in file_lines:
        embedded_array = [];
        col = -1 # Start at -1 since auto-incremented.
        #---- Iterate through the board file.
        for character in line:
            # If the character is not new line, add it to the board and parse it.
            if character != "\n":
                col = col + 1 # Increment the column number. 
                embedded_array.append(character)
                # Parse for special characters
                if character == "@": start_loc = (row, col) 
                if character == "%": goal_loc = (row, col)
    
        # Append the board row to the board and increment the row counter
        board.append(embedded_array)
        row = row + 1
    # Ensure a valid starting location was specified in the board file.
    if (start_loc[0] == -1 and start_loc[1] == -1):
        print "No valid starting location in this puzzle, which makes it unsolvable."
        print "That is too sad.  I must quit."
        sys.exit() # Exit the program
    
    # Ensure a valid goal location was specified in the board file.
    if (goal_loc[0] == -1 and goal_loc[1] == -1):
        print "No valid goal location in this puzzle, which makes it unsolvable."
        print "That is too sad.  I must quit."
        sys.exit() # Exit the program
    
    return (board, start_loc, goal_loc)
# def parse_board_file(filename): 



# Ensure a sufficient number of input arguments.
if len(sys.argv) != 2 + 1: # First argument is the script itself
    print "The function expects requires exactly two input arguments."
    print "You specified " + str(len(sys.argv)-1) + " input arguments."
    print "That is too sad.  I must quit."
    sys.exit() # Exit the program
    
board_file_path = sys.argv[0]

# Parse the board file.
[original_board, start_loc, goal_loc] = parse_board_file("test.txt")



# Store the board as it is traversed.
traversed_board = original_board

