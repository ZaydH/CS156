'''
Created on Oct 25, 2014

@author: Zayd
'''

# Import the necessary Sympy Libraries for conversion to CNF
from sympy import And, Or, Not, to_cnf
from sympy.core.symbol import Symbol
# Use the MutableString class which is similar to the Java
# StringBuffer/StringBuilder classes.
from UserString import MutableString


# This flag sets whether to solve all the way to the tree root
# or to stop at level 1 as described in the question.
solve_to_tree_root = False
if(solve_to_tree_root):
    numb_level1_children = 3
else:
    numb_level1_children = 1


def pretty_print_CNF(input_string):
    """
    SymPy returns the CNF information in a form that is
    more line with its implementation that what is easily readable
    Modify the string to make it more readable in text.

    :returns: Converted CNF string.
    """
    output_str = MutableString()
    input_string_mutable = MutableString(input_string)
    # Remove nots and white space.
    input_string_mutable = input_string_mutable.replace("Not", "!")
    input_string_mutable = input_string_mutable.replace(" ", "")
    # Remove outer "And"
    input_string_mutable = input_string_mutable.replace("And(", "")
    # Remove trailing parenthesis
    input_string_mutable = input_string_mutable[:len(input_string_mutable)-1]
    # Split based off OR
    all_clauses = input_string_mutable.split("),Or(")
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

    # Replace period with commas
    output_str = output_str.replace(".", ",")
    return str(output_str)


def calculate_minimax(V, output, is_min):
    """
    This function builds the minimax tree.  It takes V which is the variables
    in the previous level of the tree (this is in terms of Vi,j,k,m,b) and
    then outputs the next level of the tree into output.  User can select
    whether they want to do min or max manipulation.

    :param Symbol V: List of positional SymPy symbols.
    :param Symbol output: List of the minimax bit values for the previous level
    :param bool is_min: Boolean flag whether to treat the operation as a min
    operation of a max operation.

    :returns: None
    """
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


def file_and_console_print(print_string, include_new_line=True):
    """
    This function takes a string and prints to the console and
    writes it to the output file.

    :param str print_string: String to be printed.
    :param bool include_new_line: Boolean flag whether to append
    a new line at the end of the string.  Default is True.

    :returns: None
    """
    file_out = open("HW3_Q1_Results.txt", "a")
    if(include_new_line):
        print print_string
        file_out.write(print_string + "\n")
    else:
        print print_string,
        file_out.write(print_string)
    file_out.close()


# Define all propositional symbols V_(i,j,k,m,b) and build
# These symbols will be used in the CNF representations.
file_and_console_print("Defining Base Variables...", False)
V = []
for i in xrange(0, numb_level1_children):
    # Actual storage for this var
    V.append([])
    for j in xrange(0, 3):
        V[i].append([])
        for k in xrange(0, 3):
            V[i][j].append([])
            for m in xrange(0, 3):
                V[i][j][k].append([])
                for b in xrange(0, 3):
                    name = 'V'+str(i+1)+"." + str(j+1) \
                           + "." + str(k+1) + "." \
                           + str(m+1) + "." + str(b+1)
                    V[i][j][k][m].append(Symbol(name))
file_and_console_print("Done")

# Build the tree of related variables.
file_and_console_print("\n\n\nBuilding Minimax Dependencies...", False)
level1 = []
for i in xrange(0, numb_level1_children):
    level1.append([])
    level2 = []
    # Build the minimax variables for level 2
    # These variables will be used to generate variable in level 1
    for j in xrange(0, 3):
        level2.append([])
        level3 = []
        # Build the minimax variables for level 3
        # These variables will be used to generate variable in level 2
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

if(solve_to_tree_root):
    # Perform the bit manipulations at the top level (#0)
    is_min = not is_min
    level0_root = []
    calculate_minimax(level1, level0_root, is_min)
    file_and_console_print("Done")


# Print the expression for move 1 in level 1 (i.e. bits V1,b).
# This is NOT in CNF form.
for b in xrange(0, 3):
    file_and_console_print("\n\n\n\nPrinting V1,%d in non-CNF Form" % (b+1))
    non_cnf_string = pretty_print_CNF(str(level1[0][b]))
    file_and_console_print("\nV1,%d=" % (b+1))
    file_and_console_print(non_cnf_string)
    file_and_console_print("Printing V1,%d in non-CNF Form...Done" % (b+1))

# Print the CNF for move 1 in level 1 (i.e. bits V1,b).
for b in xrange(0, 3):
    file_and_console_print("\n\n\n\nConverting to CNF for V1,%d" % (b+1))
    temp_expression = to_cnf(level1[0][b], False)
    # Uncomment the line below to simplify the expression
    # temp_expression = to_cnf(temp_expression, True)
    cnf_string = pretty_print_CNF(str(temp_expression))
    file_and_console_print("\nV1,%d=" % (b+1))
    file_and_console_print(cnf_string)
    file_and_console_print("Converting to CNF for V1,%d...Done" % (b+1))

# This will print the statements all the way to the tree root.
if(solve_to_tree_root):
    # Print the expression for move 1 in level 1 (i.e. bits V1,b).
    # This is NOT in CNF form.
    for b in xrange(0, 3):
        file_and_console_print("\n\n\n\nPrinting V%d in non-CNF Form" % (b+1))
        non_cnf_string = pretty_print_CNF(str(level0_root[b]))
        file_and_console_print("\nV%d=" % (b+1))
        file_and_console_print(non_cnf_string)
        file_and_console_print("Printing V%d in non-CNF Form...Done" % (b+1))

    # Print the CNF for the root (level 0) (i.e. bits Vb).
    file_and_console_print("\n\n\n\nConverting to CNF for V%d..." % (b+1))
    for b in xrange(0, 3):
        temp_expression = to_cnf(level0_root[b], False)
        # Uncomment the line below to simplify the expression
        # temp_expression = to_cnf(temp_expression, True)
        cnf_string = pretty_print_CNF(str(temp_expression))
        file_and_console_print("\n\n\n\n\nV%d=" % (b+1))
        file_and_console_print(cnf_string)
        file_and_console_print("Converting to CNF for V%d...Done" % (b+1))
