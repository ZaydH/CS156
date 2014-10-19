'''
Created on Oct 18, 2014

@author: Zayd
'''

import string
import sys
import bisect


def handle_no_solution():
    print "NO SOLUTION"
    sys.exit(0)


class CSPConstraint:

    _variable_relation = ["eq", "ne", "lt", "gt"]

    @staticmethod
    def _parse_constraint(constraint_text):
        '''
        This function parses the string that is read from the file
        that defines the constraint.

        :param str constraint_text: File string defining the input constraint

        >>> CSPConstraint._parse_constraint("Zayd ne 3")
        ['Zayd', 'ne', 3]
        >>> CSPConstraint._parse_constraint("a234 gt dFS")
        ['a234', 'gt', 'dFS']
        >>> CSPConstraint._parse_constraint("234 gt dFS")

        >>> CSPConstraint._parse_constraint("a234 gt dFS sd")

        >>> CSPConstraint._parse_constraint("a234 gtne dFS")

        '''
        # Verify the constraint has exactly three terms.
        constraint_items = constraint_text.split()
        if(len(constraint_items) != 3):
            return None

        # Verify the item is a properly formatted variable.
        variable1 = constraint_items[0]
        if(variable1[0] not in string.ascii_letters):
            return None

        # Ensure the object is of the correct relation type. If not return none
        if(constraint_items[1] not in CSPConstraint._variable_relation):
            return None

        try:
            # Check if the last item is an integer.  If so, update the array
            integer_constraint = int(constraint_items[2])
            constraint_items[2] = integer_constraint
            return constraint_items
        except:
            # Third item in Tuple not an integer so ensure it
            # is in the right variable name format.
            variable2 = constraint_items[2]
            if(variable2[0] in string.ascii_letters):
                return constraint_items

        # Last item is neither an integer nor a variable name so return None.
        return None

    def __init__(self, constraint_text):
        '''
        Constructor for the CSPConstraint class.

        :param str constraint_text: File text defining the constraint
        '''
        #  Parse the constraint
        constraint_items = CSPConstraint._parse_constraint(constraint_text)
        # Check if the constraint was correctly parseable.
        if(constraint_items is None):
            handle_no_solution()

        # Extract the operator for the constraint (e.g. "ne", "eq", etc.)
        self._operator = constraint_items[1]
        # Check if there is a unary or binary constraint.
        if(isinstance(constraint_items[2], (int, long))):
            self._variables = (constraint_items[0],)
            self._constraint_integer = constraint_items[2]
        # If not an integer, it is a binary constraint.
        else:
            self._variables = (constraint_items[0], constraint_items[2])
            self._constraint_integer = None

    def is_binary_constraint(self):
        '''
        Constraint Size Property

        Returns True if this is a binary constraint and False
        if it is a unary constraint.
        '''
        if(len(self._variables) == 1):
            return False
        else:
            return True

    @property
    def operator(self):
        '''
        Constraint Operator Accessor

        :returns: Operator: [ne, eq, lt, gt] as a String
        '''
        return self._operator

    def get_variables(self):
        '''
        Constraint Variable(s)

        Returns a Tuple of the name (string) of the one or two
        variables in the constraint.

        :returns: Tuple str of the variable(s) in the constraint.
        '''
        return self._variables

    @property
    def integer_constraint(self):
        '''
        Constraint Integer Accessor

        Applicable for unary constraints only.

        :returns: Operator: [ne, eq, lt, gt] as a String
        '''
        if(len(self._variables) != 1):
            raise RuntimeError("Error - Cannot extract integer value from "
                               + "a non-unary constraint")
        return self._constraint_integer

    def check_satisfaction(self, variable1_value, variable2_value):
        '''
        Constraint Satisfaction Checker

        Checks whether the two specified variables satisfy the constraint.
        Only works for binary constraints.

        :returns: bool True if the constraint is satisfied and False otherwise.
        '''
        if(not self.is_binary_constraint()):
            raise RuntimeError("Method \"check_satisfication\" only supports "
                               + "binary constraints.")

        # Check the four possible constrain conditions
        if(self.operator == "ne"):
            return variable1_value != variable2_value
        elif(self.operator == "eq"):
            return variable1_value == variable2_value
        elif(self.operator == "lt"):
            return variable1_value < variable2_value
        elif(self.operator == "gt"):
            return variable1_value > variable2_value

        raise RuntimeError("Invalid operator specified for constraint check")

# ------------------ CSP Variable Class ---------------------- #


class CSPVariable:

    def __init__(self, name):
        '''
        Constructor for the CSP Variable class.

        By default, it stores the variables name (which is immutable)
        and creates empty lists for its unary and binary constraints
        as well as for its domain.
        '''
        self._name = name
        # Start with an empty domain and then build it later.
        self._domain = []
        self._unary_constraints = []
        self._binary_constraints = []
        self._unassigned = True

    def hash(self):
        '''
        Hash Definition for CSPVariable Class

        The CSPVariable class uses the variable name (string)
        as its hash.
        '''
        return self._name.hash()

    @property
    def name(self):
        '''
        Variable Name Property

        Accessor for the variable's name.

        :returns: str Variable's name
        '''
        return self._name

    def build_initial_domain(self):
        '''
        Initial Domain Builder:
        Builds the Variable's  Domain Based Solely Off Unary Constraints.
        Result of this Function
        '''
        starting_value = 0
        ending_value = sys.maxint  # Get the integer maximum
        illegal_values = []  # This represents the "ne" values.
        eq_value = -1  # A constraint can have a single "eq" value so track it

        #  Cycle through all constraints
        for constraint in self._unary_constraints:
            operator = constraint.operator
            constraint_int = constraint.integer_constraint
            # Handle the case of an equal operator
            if(operator == "eq"):
                # Check no other equal value has been specified
                if(eq_value == -1):
                    eq_value = constraint_int
                # More than one nonidentical eq constraint so  domain is empty
                elif(eq_value != constraint_int):
                    self._domain = []
                    return
            # Track the set of illegal values.
            elif(operator == "ne"):
                # Find the insort location
                insort_location = bisect.bisect_left(illegal_values,
                                                     constraint_int)
                # Verify there is not a duplicate.  If not a duplicate, then
                # insert the integer into the array.
                if(insort_location == len(illegal_values)
                   or illegal_values[insort_location + 1] != constraint_int):
                    illegal_values.insert(insort_location, constraint_int)

            # Track worst case end value only
            elif(operator == "gt"):
                # Since greater than the real value is one less
                constraint_int = constraint_int + 1
                # Update ending value if needed
                if(starting_value < constraint_int):
                    starting_value = constraint_int

            # Track worst case starting value only
            elif(operator == "lt"):
                # Since greater than the real value is one less
                constraint_int = constraint_int - 1
                # Update starting value if needed
                if(ending_value > constraint_int):
                    ending_value = constraint_int

        # Process the equal value first since it is a special case
        if(eq_value != -1):
            if(eq_value >= starting_value and eq_value <= ending_value):
                self._domain = [eq_value]
                return

        # Iterate through the possible domain values.
        illegal_val_itr = 0
        domain = []
        for domain_val in xrange(starting_value, ending_value+1):
            # Find the corresponding location in the illegal value array
            # for this integer value.
            while(illegal_val_itr < len(illegal_values)
                  and illegal_values[illegal_val_itr] < domain_val):
                illegal_val_itr += 1

            # Ensure the value has not been specifically excluded.
            if(illegal_val_itr == len(illegal_values)
               or illegal_values[illegal_val_itr] != domain_val):
                domain.append(domain_val)

        # Use the newly built domain value.
        self._domain = domain
        return

    def add_constraint(self, constraint):
        '''
        Constraint Adder

        Mutator that will add the specified constraint to the variable.
        Method manages handling of binary and unary constraints itself.
        '''
        # If it is a binary constraint append it to the binary constraints
        if(constraint.is_binary_constraint()):
            self._binary_constraints.append(constraint)
        # Add it to the unary constraints
        else:
            self._unary_constraints.append(constraint)

    def _check_assignment_consistent(self, assignment, value):
        # Assume consistency and verified in the function.
        assignment_consistent = True

        # Iterate through all the variable's binary constraints.
        for constraint in self._binary_constraints:
            # Get the variables
            variables = constraint.get_variables()
            # Verify if this variable is the first one.
            if(variables[0] == self._name):
                is_first_var = True  # If variable is first one in constraint
                other_variable_name = variables[1]
            else:
                is_first_var = False  # If variable is first one in constraint
                other_variable_name = variables[0]

            # If other variable is not assigned, go to next constraint
            if(other_variable_name not in assignment):
                continue
            else:
                # Get the other variable's value
                other_value = assignment[other_variable_name]

            # Check if the constraint is satisfied
            if((is_first_var
                and not constraint.check_satisfaction(value, other_value))
               or (not is_first_var
                   and not constraint.check_satisfaction(other_value, value))):
                # Constraint not satisfied
                assignment_consistent = False
                break

        # Return the result.
        return assignment_consistent

    def get_domain_size(self):
        '''
        Domain Size Accessor:

        Returns the number of elements in the domain
        :returns: int Domain size - Number of elements in the domain
        '''
        return len(self._domain)

    def get_variable_degree(self, assignment):
        '''
        '''
        out_degree = 0  # Set default outdegree of this variable.

        # Iterate through all binary constraints to
        # determine the variable's degree
        for constraint in self._binary_constraints:
            # Extracts the variables in the constraint
            variables = constraint.get_variables()

            # Extract name of the other variable.
            if(variables[0] == self.name()):
                other_variable_name = variables[1]
            else:
                other_variable_name = variables[0]

            # Check if the other variable is not assigned.
            # If so, increment the degree heuristic.
            if(other_variable_name not in assignment):
                out_degree += 1

        # Return the outdegree of this variable.
        return out_degree

    def is_unassigned(self):
        '''
        Variable Assignment Status:
        :returns: True if the variable is unassigned
        '''
        return self._unassigned

    def set_unassigned_state(self, unassigned_state):
        '''
        Variable Assignment State Mutator

        Updates whether a variable is unassigned or assigned

        :param bool unassigned state: True if variable unassigned,
                                      False otherwise
        '''
        self._unassigned = unassigned_state


# --------------------- CSP Class  ---------------------------#


class CSP:
    '''
    CSP Solver class.  This mimics the "CSP" object in
    the pseudocode in the textbook.
    '''
    def __init__(self, filename, forward_checking_flag):

        self._variables = {}
        self._binary_constraints = []
        self._assignment = {}
        # Set whether forward checking is enabled
        if(forward_checking_flag == 1):
            self._forward_check_enable = True
        else:
            self._forward_check_enable = False

        # Parse the file information.
        try:
            for file_line in open(filename):
                # Remove trailing newline
                file_line = file_line.rstrip("\n")
                # Building the binary constraint
                constraint = CSPConstraint(file_line)
                # Get the variables in the constraint
                constraint_vars = constraint.get_variables()
                # Check if the variable needs to be added to the list
                for var in constraint_vars:
                    if(var not in self._variables):
                        new_var = CSPVariable(var)
                        self._variables[var] = new_var
                    # Add the constraint to the variable
                    self._variables[var].add_constraint(constraint)

                # The class also stores references to the binary constraints
                if(constraint.is_binary_constraint()):
                    self._binary_constraints.append(constraint)
        except:
            handle_no_solution()

        # Build the domain for each variable
        for var_name in self._variables:
            temp_var = self._variables[var_name]
            temp_var.build_initial_domain()

    def execute_backtrack_search(self):
        # Start with an empty assignment
        self._assignment = {}
        solution = CSP._backtrack(self)

        # Check the case where no solution was found
        if(solution is None):
            handle_no_solution()

        first_variable = True  # Flag for whether to print a preceding new line
        for var_name in self._assignment:
            output_str = ""

            # Print preceding new line on all variables after the first one.
            if(not first_variable):
                output_str += "\n"
            first_variable = False

            # Build the output string with var name and value.
            output_str += var_name + "=" + str(self._assignment[var_name])
            print output_str,

    @staticmethod
    def _backtrack(csp):
        # If the assignment is complete, then return true.
        # No need to check consistency since it is checked during assignment
        if(csp.is_assignment_complete()):
            return csp._assignment

        # Select the next variable to be assigned using MRV Heuristic
        next_var = csp.select_unassigned_variable()

        # Order the domain values for that variable.
        next_var_domain = csp.order_domain_variables(next_var)

        for d_i in next_var_domain:
            # Try to assign the value to the variable
            if(csp.assign_variable_value(next_var, d_i)):

                result = CSP._backtrack(csp)
                if(result is not None):
                    return result

                # Assignment was not successful so remove it.
                csp.remove_variable_assignment(next_var)
        return None

    def assign_variable_value(self, variable, value):
        '''
        CSP Assignment Function

        Function to check if a variable can be assigned to a specified value.
        If the assignment is successful, the function returns True.  Otherwise,
        it returns False.

        :param CSPVariable variable: Variable to be assigned a value.
        :param int value: Value to assign to the variable.

        :returns: True if assignment successful. False otherwise.
        '''
        if(variable._check_assignment_consistent(self._assignment, value)):
            variable.set_unassigned_state(False)  # Set the variable assigned
            self._assignment[variable.name] = value
            return True
        # Not a consistent assignment so return False.
        else:
            return False

    def remove_variable_assignment(self, variable):
        '''
        Variable Assignment Remover

        Removes a value assignment to the specified variable.

        :param CSPVariable variable: Variable whose assignment is to be removed
        '''
        # Ensure not trying to remove the value of an unassigned variable
        if(variable.name not in self._assignment):
            raise ValueError("Error: Trying to remove the value of an "
                             + "assigned variable")
        # Remove the assignment from the dictionary.
        del self._assignment[variable.name]
        # Make the variable as unassigned.
        variable.set_unassigned_state(True)

    def is_assignment_complete(self):
        '''
        Assignment Completeness Checker

        Determines whether the CSP assignment is complete.

        :returns: bool - True if Assignment is complete. False otherwise.
        '''
        complete_assn = True  # By default assignment is complete.
        for var in self._variables:
            # Check if the variable is unassigned
            if(self._variables[var].is_unassigned()):
                # Assignment not complete since var is unassigned
                complete_assn = False
                break
        return complete_assn

    def select_unassigned_variable(self):
        '''
        CSP Variable Selection Algorithm

        Implements the Minimum Remaining Variable (MRV) algorithm.

        :returns: CSPVariable - Variable with the smallest remaining domain.
        '''
        # Initialize the variables for the initial setting.
        fail_first_variable = None
        minimum_domain_size = sys.maxint
        # Find the variable with the smallest domain
        for var_name in self._variables:
            var = self._variables[var_name]
            # Variable must not already be unassigned
            # And the domain size must be smaller than current min
            if(var.is_unassigned()
               and var.get_domain_size() < minimum_domain_size):
                fail_first_variable = var
                minimum_domain_size = var.get_domain_size

        # Verify a valid variable was selected.
        if(fail_first_variable is None):
            raise RuntimeError("No variable was selected for assignment.")

        return fail_first_variable

    def order_domain_variables(self, variable):
        # FIX ME - Need to implement code to order domain variables.
        print "Need to order domain variables"
        return variable._domain


'''-----------------------------------------------------------------------
                         Parse Input Arguments
------------------------------------------------------------------------'''
# Verify the right number of input arguments specified.
if(len(sys.argv) > 3):
    handle_no_solution()

# Get the name of the file containing the csp definition
csp_info_file_name = sys.argv[1]

# Verify a valid flag for forward checking.
if(sys.argv[2] != "1" and sys.argv[2] != "2"):
    handle_no_solution()
# Extract the forward checking flag.
forward_checking_flag = int(sys.argv[2])

'''-----------------------------------------------------------------------
                   Build the CSP and then Run Search
------------------------------------------------------------------------'''

# Build the CSP
csp = CSP(csp_info_file_name, forward_checking_flag)

csp.execute_backtrack_search()
