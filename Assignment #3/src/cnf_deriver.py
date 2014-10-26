'''
Created on Oct 25, 2014

@author: Zayd
'''
import sys

# Flag to indicate if doctest is running.
global is_doctest
is_doctest = True


class CNF:

    NOT_OP = "~"
    OR_OP = "+"
    AND_OP = "&"
    OPERATORS = ["(", ")", NOT_OP, OR_OP, AND_OP]

    # Constructor for the solver.
    def __init__(self, prop_statement):
        # Remove all spaces.
        prop_statement = prop_statement.replace(" ", "")
        # Parse the statement array.
        symbol_array = []
        # Go through the prop statement and parse it into symbols and operators
        last_position = 0
        for index in xrange(0, len(prop_statement)):
            if(prop_statement[index] in CNF.OPERATORS):
                # Handle the case of two adjacent operators.
                if(last_position != index):
                    symbol_array.append(prop_statement[last_position:index])
                # Append the operator
                symbol_array.append(prop_statement[index])
                # Update the last position.
                last_position = index + 1

        # Handle the case where the statement ended in a variable.
        if(last_position < len(prop_statement)):
            symbol_array.append(prop_statement[last_position:])

        # Store the parsed statement.
        self.bool_func = symbol_array

    def is_single_variable(self):
        """

        >>> single_a = CNF("a")
        >>> single_a.is_single_variable()
        True
        >>> ab =CNF("ab")
        >>> ab.is_single_variable()
        True
        >>> not_ab = CNF("~ab")
        >>> not_ab.is_single_variable()
        True
        >>> not_ab_parent = CNF("~(ab)")
        >>> not_ab_parent.is_single_variable()
        False
        >>> a_plus_b = CNF("a+b")
        >>> a_plus_b.is_single_variable()
        False
        """
        # If the propositional string is more than two terms,
        # then it cannot be a single variable sentence.
        if(len(self.bool_func) > 2):
            return False

        # handle the case of not.
        if(len(self.bool_func) == 2 and self.bool_func[0] == CNF.NOT_OP
           and self.bool_func[1] not in CNF.OPERATORS):
            return True

        # Handle the case of a single variable.
        if(len(self.bool_func) == 1
           and self.bool_func[0] not in CNF.OPERATORS):
            return True

        # All other cases are false.
        return False

    def has_outer_parenthesis(self):
        """
        >>> a_plus_b = CNF("a+b")
        >>> a_plus_b.has_outer_parenthesis()
        False
        >>> has_paren1 = CNF("(a)")
        >>> has_paren1.has_outer_parenthesis()
        True
        >>> has_paren2 = CNF("(a+b)")
        >>> has_paren2.has_outer_parenthesis()
        True
        >>> c = CNF("c")
        >>> c.has_outer_parenthesis()
        False
        """
        # store the length of the string.
        len_self_bool = len(self.bool_func)
        # To have other parenthesis, must have at least two elements.
        if(len_self_bool < 2):
            return False

        # Check if it has other parenthesis.
        if(self.bool_func[0] == "("
           and self.bool_func[len_self_bool-1] == ")"):
            return True

        # Not outer parenthesis so return false.
        return False

    def remove_outer_parenthesis(self):
        # store the length of the string.
        self.bool_func = self.bool_func[1:len(self.bool_func) - 1]

    def add_outer_parenthesis(self):
        # store the length of the string.
        self.bool_func = ["("] + self.bool_func + [")"]

    def getFirstOperator(self):
        operator_and_location = self.getFirstOperatorAndLocation()
        return operator_and_location[0]

    def getFirstOperatorAndLocation(self):
        """

        >>> a_plus_b = CNF("a+b")
        >>> a_plus_b.getFirstOperator()
        ('+', 1)
        >>> ab = CNF("ab")
        >>> ab.getFirstOperator()

        >>> ab = CNF("(a+b)&(c+d)")
        >>> ab.getFirstOperator()
        ('&', 5)
        >>> ab = CNF("(a+b+(a&b))&(c+d)")
        >>> ab.getFirstOperator()
        ('&', 11)
        """
        # Keep track of the open parenthesis.
        open_paren_count = 0

        if(self.bool_func[0] == CNF.NOT_OP):
            return (CNF.NOT_OP, 0)

        # Go through the characters in the boolean function.
        for index in xrange(0, len(self.bool_func)):
            # Increment Open Parenthesis Count
            if(self.bool_func[index] == "("):
                open_paren_count += 1
            # Decrement Open Parenthesis Count
            elif(self.bool_func[index] == ")"):
                open_paren_count -= 1
            # Primary Operator Only if Not Between Parenthesis
            # and it is OR/AND.
            elif((self.bool_func[index] == CNF.AND_OP
                 or self.bool_func[index] == CNF.OR_OP)
                 and open_paren_count == 0):
                return (self.bool_func[index], index)

        # No operator found so return none.
        return None

    @staticmethod
    def merge_two_funcs(cnf1, op, cnf2):
        """
        >>> a_plus_b = CNF("(a+b)")
        >>> c_plus_d = CNF("(c+d)")
        >>> CNF.merge_two_funcs(a_plus_b, '+', c_plus_d)
        ['(', 'a', '+', 'b', ')', '+', '(', 'c', '+', 'd', ')']
        >>> CNF.merge_two_funcs(a_plus_b, '&', c_plus_d)
        ['(', 'a', '+', 'b', ')', '&', '(', 'c', '+', 'd', ')']
        """
        if(op != CNF.AND_OP and op != CNF.OR_OP):
            raise ValueError("Error: The operator must be either \""
                             + CNF.AND_OP + "\" or \"" + CNF.OR_OP + "\".")
        # build a new CNF
        new_cnf = CNF("")
        # Concatenate the two CNFs
        new_cnf.bool_func = list(cnf1.bool_func) + [op] + list(cnf2.bool_func)
        # Return the merged cnf
        if(not is_doctest):
            return new_cnf
        else:
            return new_cnf.bool_func

    def split_on_binary_operator(self, operator_loc=-1):
        """
        >>> merged_clause = CNF("(a+b)&(c+d)")
        >>> merged_clause.split_on_binary_operator()
        (['(', 'a', '+', 'b', ')'], ['(', 'c', '+', 'd', ')'])
        >>> merged_clause = CNF("(a+b)&(c+d)")
        >>> merged_clause.split_on_binary_operator(5)
        (['(', 'a', '+', 'b', ')'], ['(', 'c', '+', 'd', ')'])
        """
        # If no operate location is specified, then find it.
        if(operator_loc == -1):
            first_operator = self.getFirstOperator()
            operator_loc = first_operator[1]

        # Create the new clauses.
        left_clause = CNF("")
        right_clause = CNF("")

        # Get the left clause.
        left_clause.bool_func = list(self.bool_func[:operator_loc])
        right_clause.bool_func = list(self.bool_func[operator_loc+1:])

        # Return the split clauses.
        if(not is_doctest):
            return (left_clause, right_clause)
        else:
            return (left_clause.bool_func, right_clause.bool_func)

    def derive_cnf(self):

        # Termination condition of the recursion.
        # Terminate when only a single variable.
        if(self.is_single_variable()):
            return self

        # Check if this statement is nested in parenthesis.
        # If so, remove them and return again.
        if(self.has_outer_parenthesis()):
            self.remove_outer_parenthesis()
            return self.derive_cnf()

        # Get the first operator.
        first_operator = self.getFirstOperator()
        cur_op = first_operator[0]
        op_loc = first_operator[1]

        # Determine whether the first operator is a negation If so, drive it in
        if(cur_op == "~"):
            # Get if the statement is itself only a single variable.
            # If it is, then recurse.
            if(self.is_single_variable()):
                return self
            # Expand the negation.
            else:
                self.drive_in_negation()
                return self.derive_cnf()

        # Derive the left and right CNF clauses.
        split_clauses = self.split_on_binary_operator(op_loc)
        left_cnf = split_clauses[0].derive_cnf()
        right_cnf = split_clauses[1].derive_cnf()

        # Get a tuple of the next operator and its location.
        if(cur_op == "&"):
            # Determine if you need to add parenthesis
            # If they are not there, add them.
            if(not left_cnf.has_parenthesis()
               and not left_cnf.is_single_variable()):
                left_cnf.add_outer_parenthesis()

            if(not right_cnf.has_parenthesis()
               and not right_cnf.is_single_variable()):
                right_cnf.add_outer_parenthesis()
            # Return the CNF
            return CNF.merge_two_funcs(left_cnf, "&", right_cnf)

        # Handle the case of or.
        if(cur_op == "+"):
            if(left_cnf.is_single_variable())


if(__name__ == '__main__'):
    import doctest
    doctest.testmod()
    # Enables extra doctest printing for debug.
    is_doctest = True
