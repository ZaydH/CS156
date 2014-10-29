'''
Created on Oct 28, 2014

@author: Zayd Hammoudeh

Team Member #1: Zayd Hammoudeh (009418877)
Team Member #2: Muffins Hammoudeh
        (No student ID - she's my cat but was here with me
        while I worked so she deserves credit).
'''

import copy

# Initialize a counter to track step number in DPLL
global step_numb
step_numb = 0


def DPLL(clauses, assn, model):
    """
    Recursive DPLL algorithm to determine satisfiability of a set of CNF
    clauses.  It returns True if the clauses are satisfiable and
    False otherwise.
    """
    # Increment the step number
    global step_numb
    step_numb += 1
    # Check for an invalid condition.
    if(has_empty_clause(clauses)):
        print "Step #" + str(step_numb) + ": Empty clause found. Recursing..."
        return False
    # Check if all clauses were satisfied
    if(all_clauses_satisfied(clauses)):
        print "Step #" + str(step_numb) + ": Satisfying assignment found."
        return True

    symbol = find_pure_symbol(clauses, assn, model)
    if(symbol is not None):
        print "Step #" + str(step_numb) + ": Symbol \"" + symbol + "\" is a pure" + \
            " symbol. It was assigned to \"" + str(assn[symbol]) + "\"."
        return DPLL(clauses, assn, model)

    # Check for unit clause
    symbol = find_unit_clause(clauses, assn, model)
    if(symbol is not None):
        print "Step #" + str(step_numb) + ": Unit clause found for symbol \"" \
            + symbol + "\". It was assigned to \"" + str(assn[symbol]) + "\"."
        return DPLL(clauses, assn, model)

    # Select symbol to test
    symbol = model[0]

    # Assign symbol to true and false to see if it returns a value.
    clauses_copy = copy.deepcopy(clauses)
    assn_copy = copy.deepcopy(assn)
    model_copy = copy.deepcopy(model)
    pos_literal = "+" + symbol
    update_clauses_and_model_for_symbol(pos_literal, clauses_copy, assn_copy,
                                        model_copy)
    print "Step #" + str(step_numb) + ": Try assigning symbol \"" \
        + symbol + "\" to \"True\"."
    pos_result = DPLL(clauses_copy, assn_copy, model_copy)
    if(pos_result):
        assn = assn_copy
        model = model_copy
        return True

    # Assign symbol to true and false to see if it returns a value.
    print "\nAssigning symbol \"" + symbol + "\" to \"True\" failed."
    step_numb += 1
    print "Step #" + str(step_numb) + ": Try assigning symbol \"" \
        + symbol + "\" to \"False\"."
    neg_literal = "-" + symbol
    update_clauses_and_model_for_symbol(neg_literal, clauses, assn, model)
    return DPLL(clauses, assn, model)


def has_empty_clause(clauses):
    """
    Iterate through all clauses and look for an empty
    clause.  If an empty clause is found, return true
    else return false.
    """
    for clause in clauses:
        if(len(clause) == 0):
            return True
    return False


def all_clauses_satisfied(clauses):
    """
    Check if any clauses still exist.  If no clauses
    exist, then a satisfying assignment has been found. Otherwise
    not all clauses satisfied.
    """
    if(len(clauses) == 0):
        return True
    return False


def find_pure_symbol(clauses, assn, model):
    all_elements = []
    # Go through all clauses and make a list of literals.
    for clause in clauses:
        for literal in clause:
            # Add this literal to the list.
            all_elements.append(literal)

    # See if this symbol is a positive or negative literal.
    pure_symbol_found = False
    for symbol in model:
        has_pos_symbol = ("+" + symbol in all_elements)
        has_neg_symbol = ("-" + symbol in all_elements)

        # Has both positive and negative literals.
        if(has_pos_symbol and has_neg_symbol):
            continue
        else:
            pure_symbol_found = True
            break
    # If no pure symbol found, then return.
    if(not pure_symbol_found):
        return None

    # Determine literal for this symbol.
    if(has_pos_symbol):
        literal = "+" + symbol
        assn[symbol] = True
    else:
        literal = "-" + symbol
        assn[symbol] = False

    # Iterate through the list of clauses and remove any clause
    # having this literal.
    update_clauses_and_model_for_symbol(literal, clauses, assn, model)

    # Return the symbol.
    return symbol


def find_unit_clause(clauses, assn, model):
    """
    Go through and find any clause with only one variable.
    If it exists, update clauses and set that value to whatever
    value makes the clause true.
    """
    # Iterate through all clauses and see if a unit clause
    # is found.
    unit_clause_found = False  # Checked in loop
    for clause in clauses:
        if(len(clause) == 1):
            unit_clause_found = True
            break

    # No unit clause found so return false.
    if(not unit_clause_found):
        return None

    # Extract literal.
    literal = clause[0]
    update_clauses_and_model_for_symbol(literal, clauses, assn, model)

    # Return true to go to the next variable.
    symbol = literal[1:]
    return symbol


def update_clauses_and_model_for_symbol(literal, clauses, assn, model):
    # Extract literal sign.
    literal_sign = literal[0]
    # Extract the symbol name
    symbol = literal[1:]
    # Remove any clauses that also has this variable.
    i = 0
    while(i < len(clauses)):
        if(literal in clauses[i]):
            clauses.pop(i)
        else:
            i += 1

    # Update the assignment and model.
    if(literal_sign == "+"):
        assn[symbol] = True
        negated_literal = "-" + symbol
    else:
        assn[symbol] = False
        negated_literal = "+" + symbol

    # Iterate through the list and remove the negated literal from the clause
    for clause in clauses:
        if(negated_literal in clause):
            clause.remove(negated_literal)

    # Remove symbol from the model.
    model.remove(symbol)


# Build the clauses.
initial_clauses = []
# Build the clauses from part A.
for i in xrange(1, 5):
    for j in xrange(1, 3):
        for k in xrange(j+1, 4):
            first_symbol = "-P" + str(i) + "," + str(j)
            second_symbol = "-P" + str(i) + "," + str(k)
            initial_clauses.append([first_symbol, second_symbol])
    # Build clause with three variables.
    first_symbol = "+P" + str(i) + ",1"
    second_symbol = "+P" + str(i) + ",2"
    third_symbol = "+P" + str(i) + ",3"
    initial_clauses.append([first_symbol, second_symbol, third_symbol])

# Build the clauses for part B.
for hole in xrange(1, 4):
    for i in xrange(1, 4):
        for j in xrange(i+1, 5):
            first_symbol = "-P" + str(i) + "," + str(hole)
            second_symbol = "-P" + str(j) + "," + str(hole)
            initial_clauses.append([first_symbol, second_symbol])

print "The clauses are below.  A plus sign (\"+\") before a symbol name " \
    + "indicates a positive literal.\nA minus sign (\"-\") before a symbol " \
    + "name indicates a negated literal."
print initial_clauses
print "\n"

# Build the model.
model = []
for pigeon in xrange(1, 5):
    for hole in xrange(1, 4):
        model.append("P" + str(pigeon) + "," + str(hole))

print "The model is: ",
print model
print "\n"
symbol = ""
# temp_array = ["+" + symbol for symbol in model]
# initial_clauses = []
# initial_clauses.append(temp_array)

# Create the assignment
assignment = {}

# Call DPLL
result = DPLL(initial_clauses, assignment, model)

# Print the result.
if(result is False):
    print "\nThese clauses are unsatisfiable."
else:
    print "\nThese clauses are satisfiable."
