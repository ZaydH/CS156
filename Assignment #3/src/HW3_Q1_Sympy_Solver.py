'''
Created on Oct 25, 2014

@author: Zayd
'''

from sympy import *
from sympy.core.symbol import Symbol
from UserString import MutableString


def pretty_print_CNF(input_string):
    output_str = MutableString()
    # Remove nots and white space.
    input_string = input_string.replace("Not", "!")
    input_string = input_string.replace(" ", "")
    # Remove outer "And"
    input_string = input_string.replace("And(", "")
    # Remove trailing parenthesis
    input_string = input_string[:len(input_string)-1]
    # Split based off OR
    all_clauses = input_string.split("),Or(")
    for clause in all_clauses:
        # Remove any preceding ors
        clause = clause.replace("Or(", "")
        # Remove any trailing parenthesis
        if(clause[len(clause)-1] == ")"):
            clause = clause[:len(clause)-1]
        clause = clause.replace(",", "+")
        clause = clause.replace("(", "")
        clause = clause.replace(")", "")
        # Build output string.
        if(len(output_str) == 0):
            output_str += "(" + clause + ")"
        else:
            output_str += "&(" + clause + ")"

    return output_str


# Base Variables
V = []
V.append([])  # Add a dummy place holder to make it easier for reading
# Create the array of symbols and concatenate a dummy placeholder.
for i in xrange(1, 4):
    # Actual storage for this var
    V.append([])
    # Add a dummy placeholder
    V[i].append([])
    for j in xrange(1, 4):
        # Actual storage for this var
        V[i].append([])
        # Dummy placeholder
        V[i][j].append([])
        for k in xrange(1, 4):
            # Actual storage for this var
            V[i][j].append([])
            # Dummy placeholder
            V[i][j][k].append([])
            for m in xrange(1, 4):
                # Actual storage for this var
                V[i][j][k].append([])
                # Dummy placeholder
                V[i][j][k][m].append([])
                for b in xrange(1, 4):
                    V[i][j][k][m][b] = Symbol('V'+str(i)+","
                                              + str(j) + ","
                                              + str(k) + ","
                                              + str(m) + ","
                                              + str(b))

is_min = True
for i in xrange(1, 4):
    # Actual storage for this var
    V.append([])
    # Add a dummy placeholder
    V[i].append([])
    for j in xrange(1, 4):
        # Actual storage for this var
        V[i].append([])
        # Dummy placeholder
        V[i][j].append([])
        for k in xrange(1, 4):
            # Actual storage for this var
            V[i][j].append([])
            # Dummy placeholder
            V[i][j][k].append([])
            for m in xrange(1, 4):
                # Actual storage for this var
                V[i][j][k].append([])
                # Dummy placeholder
                V[i][j][k][m].append([])
                for b in xrange(1, 4):
                    # Switch to max.
                    is_min = not is_min



def calculate_minimax(V, loc, is_min):

    for b in xrange(1, 4):

        for i in xrange(1,4):
            # Set the starting value of the function
            bool_func = is_min
    
            bool_func = 