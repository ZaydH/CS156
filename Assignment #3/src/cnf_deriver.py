'''
Created on Oct 25, 2014

@author: Zayd
'''
class CNF:

    NOT_OP = "~"
    OR_OP = "+"
    AND_OP = "&"

    # Constructor for the solver.
    def __init__(self, prop_statement):
        # Remove all spaces.
        prop_statement = prop_statement.replace(" ", "")
        # Parse the statement array.
        symbol_array = []
        operators = ["(", ")", CNF.NOT_OP, CNF.OR_OP, CNF.AND_OP]

#         # Remove preceding operators
#         while(prop_statement[0] in operators):
#             # Store the character in the symbol array.
#             symbol_array.append(prop_statement[0])
#             # Remove the preceding symbol.
#             prop_statement = prop_statement[1:]

        # Go through the prop statement and parse it into symbols and operators
        last_position = 0
        for index in xrange(0, len(prop_statement)):
            if(prop_statement[index] in operators):
                # Handle the case of two adjacent operators.
                if(last_position != index):
                    symbol_array.append(prop_statement[last_position:index])
                # Append the operator
                symbol_array.append(prop_statement[index])
                # Update the last position.
                last_position = index + 1
        

    def is_single_variable(self):
        
        
        # If the propositional string is more than two letters,
        # then it cannot be a single variable sentence.
        if(self[0] == NOT_OP and )

    def derive_cnf(self):

        # Termination condition of the recursion.
        # Terminate when only a single variable.
        if(self.is_single_variable()):
            return self

        # Check if this statement is nested in parenthesis.
        # If so, remove them and return again.
        if(self.has_parenthesis()):
            self.remove_outer_parenthesis()
            return self.derive_cnf()

        # Get the next operator.
        next_operator = self.getOperator()

        # Determine whether the first operator is a negation If so, drive it in
        if(next_operator == "~"):
            # Get if the statement is itself only a single variable.
            # If it is, then recurse.
            if(self.isSingleVariable()):
                return self
            # Expand the negation.
            else:
                self.drive_in_negation()
                return self.derive_cnf()

        # Derive the left and right cnf clauses.
        clauses = self.split_on_binary_operator()
        left_cnf = clauses[0].derive_cnf()
        right_cnf = clauses[1].derive_cnf()

        # Get a tuple of the next operator and its location.
        if(next_operator == "&"):
            # Determine if you need to add parenthesis
            left_statement = left_cnf.to_string()
            if(not left_cnf.is_atomic() and not left_cnf.has_parenthesis()):
                left_statement = "(" + left_statement + ")"
            right_statement = right_cnf.to_string()
            if(not right_cnf.is_atomic() and not right_cnf.has_parenthesis()):
                right_statement = "(" + right_statement + ")"
            # Return the CNF
            return PropositionalStatement(left_statement + "&"
                                          + right_statement)
        # Handle the case of or.
        if(next_operator == "+"):

    34     if (_op == BOP.OR)
    35     {
    36         if (( cnfLeft == null || cnfLeft.IsAtomic() || cnfLeft.Op == BOP.OR)
    37             && (cnfRight == null || cnfRight.IsAtomic() || cnfRight.Op == BOP.OR))
    38         //   +
    39         // +   +
    40         {
    41             return new BoolExpr(BOP.OR, cnfLeft, cnfRight);
    42         }
    43         else if ((cnfLeft != null && cnfLeft.Op == BOP.AND)
    44                 && (cnfRight == null || cnfRight.IsAtomic() || cnfRight.Op == BOP.OR))
    45         //   +
    46         // *   +
    47         {
    48             BoolExpr newLeft = new BoolExpr(BOP.OR, cnfLeft.Left, cnfRight);
    49             BoolExpr newRight = new BoolExpr(BOP.OR, cnfLeft.Right, cnfRight);
    50 
    51             return new BoolExpr(BOP.AND, newLeft.ToCNF(), newRight.ToCNF());
    52         }
    53         else if ((cnfRight != null && cnfRight.Op == BOP.AND)
    54                 && (cnfLeft == null || cnfLeft.IsAtomic() || cnfLeft.Op == BOP.OR))
    55         //   +
    56         // +   *
    57         {
    58             BoolExpr newLeft = new BoolExpr(BOP.OR, cnfLeft, cnfRight.Right);
    59             BoolExpr newRight = new BoolExpr(BOP.OR, cnfLeft, cnfRight.Left);
    60 
    61             return new BoolExpr(BOP.AND, newLeft.ToCNF(), newRight.ToCNF());
    62         }
    63         else if ((cnfLeft != null && cnfLeft.Op == BOP.AND)
    64                 && (cnfRight != null && cnfRight.Op == BOP.AND))
    65         //   +
    66         // *   *
    67         {
    68             BoolExpr newLeft = new BoolExpr(BOP.AND,
    69                 new BoolExpr(BOP.OR, cnfLeft.Left, cnfRight.Left),
    70                 new BoolExpr(BOP.OR, cnfLeft.Right, cnfRight.Left));
    71 
    72             BoolExpr newRight = new BoolExpr(BOP.AND,
    73                 new BoolExpr(BOP.OR, cnfLeft.Left, cnfRight.Right),
    74                 new BoolExpr(BOP.OR, cnfLeft.Right, cnfRight.Right));
    75 
    76             return new BoolExpr(BOP.AND, newLeft.ToCNF(), newRight.ToCNF());
    77         }
    78     }


            # Handle the case where an an error occurred.
            print ("Error Generating CNF. Exiting...")
            sys.exit(0)
