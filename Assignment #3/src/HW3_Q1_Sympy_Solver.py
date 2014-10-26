'''
Created on Oct 25, 2014

@author: Zayd
'''

from sympy import *
from sympy.core.symbol import Symbol
from UserString import MutableString


global file_out


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


def calculate_minimax(V, output, is_min):

    # Determine the function for min/max
    if(is_min):
        op = And
    else:
        op = Or

    for b in xrange(0, 3):
        # Set the starting value of the function
        bool_func = is_min
        # Iterate through all tree children.
        for i in xrange(0, 3):
            # Set the starting value of the clause
            clause = True
            # Concatenate previous bits.
            for prev_b in xrange(0, b):
                # Determine bit equivalence
                equiv = Or(And(output[prev_b], V[i][prev_b]),
                           And(Not(output[prev_b]), Not(V[i][prev_b])))
                # Build the previous bits
                clause = And(clause, equiv)
            # Build the clause
            clause = And(clause, V[i][b])
            # Append this clause
            bool_func = op(bool_func, clause)
        # Save the boolean function.
        output.append(bool_func)


def file_and_console_print(string, include_new_line=True):
    if(include_new_line):
        print string
        file_out.write(string + "\n")
    else:
        print string,
        file_out.write(string)

file_out = open("HW3_Q1_Results.txt", "w")

file_and_console_print("Defining Base Variables...", False)
# Base Variables
V = []
# Create the array of symbols and concatenate a dummy placeholder.
for i in xrange(0, 3):
    # Actual storage for this var
    V.append([])
    for j in xrange(0, 3):
        V[i].append([])
        for k in xrange(0, 3):
            V[i][j].append([])
            for m in xrange(0, 3):
                V[i][j][k].append([])
                for b in xrange(0, 3):
                    name = 'V'+str(i+1)+"," + str(j+1) \
                           + "," + str(k+1) + "," \
                           + str(m+1) + "," + str(b+1)
                    V[i][j][k][m].append(Symbol(name))
file_and_console_print("Done")

file_and_console_print("\n\n\nBuilding Minimax Dependencies...", False)
# Build the tree of related variables.
level1 = []
for i in xrange(0, 3):
    level1.append([])
    level2 = []
    for j in xrange(0, 3):
        level2.append([])
        level3 = []
        for k in xrange(0, 3):
            level3.append([])
            # Perform the bit manipulations one level up.
            is_min = True
            calculate_minimax(V[i][j][k], level3[k], is_min)
        # Perform the bit manipulations at the third level.
        is_min = not is_min
        calculate_minimax(level3, level2[j], is_min)
    # Perform the bit manipulations at the second level.
    is_min = not is_min
    calculate_minimax(level2, level1[i], is_min)

# Perform the bit manipulations at the top level.
is_min = not is_min
output = []
calculate_minimax(level1, output, is_min)
file_and_console_print("Done")

file_and_console_print("\n\n\n\nConverting to CNF for V1,b...")

# Print the output
for b in xrange(0, 3):
    cnf_string = pretty_print_CNF(str(to_cnf(level1[b])))
    file_and_console_print("\n\n\n\n\nV1,%d=" % (b+1))
    file_and_console_print(cnf_string)

# # Print the output
# for b in xrange(0, 3):
#     cnf_string = pretty_print_CNF(to_cnf(output[b]))
#     file_and_console_print("\n\n\n\n\nV%d=" % (b+1))
#     file_and_console_print(cnf_string)

file_out.close()
