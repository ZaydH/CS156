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

# Create the array of symbols and concatenate a dummy placeholder.
P = []
P.append([])

# Build the variables for the pigeons and holes.
for pigeon in xrange(1, 5):
    # Append an array for the variable
    P.append([])
    # Create a dummy holder for the first pigeon
    P[pigeon].append("")
    for hole in xrange(1, 4):
        P[pigeon].append(Symbol('P'+str(pigeon)+str(hole)))

# Build the solution to part A.
part_a_conjuncts = []
for pigeon in xrange(1, 5):
    term1 = And(P[pigeon][1], Not(P[pigeon][2]), Not(P[pigeon][3]))
    term2 = And(Not(P[pigeon][1]), (P[pigeon][2]), Not(P[pigeon][3]))
    term3 = And(Not(P[pigeon][1]), Not(P[pigeon][2]), (P[pigeon][3]))
    # Build the conjunction of the disjuncts.
    part_a_conjuncts.append(Or(term1, term2, term3))

# Build part A using conjuncts.
part_a = And(part_a_conjuncts[0], part_a_conjuncts[1],
             part_a_conjuncts[2], part_a_conjuncts[3])

# Build part B.
part_b = False
for hole in xrange(1, 4):
    part_b = Or(part_b, And(P[1][hole], P[2][hole]))
    part_b = Or(part_b, And(P[1][hole], P[3][hole]))
    part_b = Or(part_b, And(P[1][hole], P[4][hole]))
    part_b = Or(part_b, And(P[2][hole], P[3][hole]))
    part_b = Or(part_b, And(P[2][hole], P[4][hole]))
    part_b = Or(part_b, And(P[3][hole], P[4][hole]))

# Build the not PHP problem.
not_php = Not(And(part_a, part_b))
print pretty_print_CNF(str(to_cnf(not_php, True)))
