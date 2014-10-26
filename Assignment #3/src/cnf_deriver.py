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

    def getFirstOperator(self):
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
    def merge_two_cnf(cnf1, op, cnf2):
        """
        >>> a_plus_b = CNF("(a+b)")
        >>> c_plus_d = CNF("(c+d)")
        >>> CNF.merge_two_cnf(a_plus_b, '+', c_plus_d)
        ['(', 'a', '+', 'b', ')', '+', '(', 'c', '+', 'd', ')']
        >>> CNF.merge_two_cnf(a_plus_b, '&', c_plus_d)
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
                first_operator = self.getOperator()
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
        first_operator = self.getOperator()
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
            left_statement = left_cnf.to_string()
            if(not left_cnf.is_atomic() and not left_cnf.has_parenthesis()):
                left_statement = "(" + left_statement + ")"
            right_statement = right_cnf.to_string()
            if(not right_cnf.is_atomic() and not right_cnf.has_parenthesis()):
                right_statement = "(" + right_statement + ")"
            # Return the CNF
            return CNF(left_statement + "&" + right_statement)
        
        # Handle the case of or.
        if(cur_op == "+"):
#  
#     34     if (_op == BOP.OR)
#     35     {
#     36         if (( cnfLeft == null || cnfLeft.IsAtomic() || cnfLeft.Op == BOP.OR)
#     37             && (cnfRight == null || cnfRight.IsAtomic() || cnfRight.Op == BOP.OR))
#     38         //   +
#     39         // +   +
#     40         {
#     41             return new BoolExpr(BOP.OR, cnfLeft, cnfRight);
#     42         }
#     43         else if ((cnfLeft != null && cnfLeft.Op == BOP.AND)
#     44                 && (cnfRight == null || cnfRight.IsAtomic() || cnfRight.Op == BOP.OR))
#     45         //   +
#     46         // *   +
#     47         {
#     48             BoolExpr newLeft = new BoolExpr(BOP.OR, cnfLeft.Left, cnfRight);
#     49             BoolExpr newRight = new BoolExpr(BOP.OR, cnfLeft.Right, cnfRight);
#     50 
#     51             return new BoolExpr(BOP.AND, newLeft.ToCNF(), newRight.ToCNF());
#     52         }
#     53         else if ((cnfRight != null && cnfRight.Op == BOP.AND)
#     54                 && (cnfLeft == null || cnfLeft.IsAtomic() || cnfLeft.Op == BOP.OR))
#     55         //   +
#     56         // +   *
#     57         {
#     58             BoolExpr newLeft = new BoolExpr(BOP.OR, cnfLeft, cnfRight.Right);
#     59             BoolExpr newRight = new BoolExpr(BOP.OR, cnfLeft, cnfRight.Left);
#     60 
#     61             return new BoolExpr(BOP.AND, newLeft.ToCNF(), newRight.ToCNF());
#     62         }
#     63         else if ((cnfLeft != null && cnfLeft.Op == BOP.AND)
#     64                 && (cnfRight != null && cnfRight.Op == BOP.AND))
#     65         //   +
#     66         // *   *
#     67         {
#     68             BoolExpr newLeft = new BoolExpr(BOP.AND,
#     69                 new BoolExpr(BOP.OR, cnfLeft.Left, cnfRight.Left),
#     70                 new BoolExpr(BOP.OR, cnfLeft.Right, cnfRight.Left));
#     71 
#     72             BoolExpr newRight = new BoolExpr(BOP.AND,
#     73                 new BoolExpr(BOP.OR, cnfLeft.Left, cnfRight.Right),
#     74                 new BoolExpr(BOP.OR, cnfLeft.Right, cnfRight.Right));
#     75 
#     76             return new BoolExpr(BOP.AND, newLeft.ToCNF(), newRight.ToCNF());
#     77         }
#     78     }

            # Handle the case where an an error occurred.
            print ("Error Generating CNF. Exiting...")
            sys.exit(0)

if(__name__ == '__main__'):
    import doctest
    doctest.testmod()
    # Enables extra doctest printing for debug.
    is_doctest = True
