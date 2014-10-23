'''
Created on Oct 18, 2014

@author: Zayd
'''

import string
import sys
import bisect
import datetime


# These variables are used to track the performance of the search
numb_backtrack_calls = 0
numb_var_sets = 0
enable_performance_printing = True
start_time = datetime.datetime.now()


# ----------------- CSPConstraint Class ---------------- #

class CSPConstraint:
    '''
    CSP Constraint Class:

    Constraint class for binary and unary constraints.
    '''

    # Complete set of supported variable relations.
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
            raise ValueError

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

    def get_domain(self):
        '''
        Variable Domain Accessor

        Returns the domain of a variable.

        :returns: int List of the object's current domain.
        '''
        return self._domain

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
        '''
        Assignment Consistency Checker

        For the implicit variable, this method checks that assigning the
        specified value to this variable is consistent with the specified
        parameter.  If it is consistent, it makes the assignment.

        :param dict assignment: Dictionary of variable assignments.
        :param int value: Value to be assigned to the variable.

        :returns: bool True if assignment is valid. False Otherwise.
        '''
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

    def get_degree(self, assignment):
        '''
        Variable Degree Accessor

        Determines the out degree of the implicit variable
        based off the current assignment.

        :param dict assignment: CSP Assignment as a dictionary

        :returns: int Degree of this variable.
        '''
        neighbors = []

        # Iterate through all binary constraints to
        # determine the variable's degree
        for constraint in self._binary_constraints:
            # Extracts the variables in the constraint
            variables = constraint.get_variables()

            # Extract name of the other variable.
            if(variables[0] == self.name):
                other_variable_name = variables[1]
            else:
                other_variable_name = variables[0]

            # Check if the other variable is not assigned.
            # If so, add the variable to neighbors..
            if(other_variable_name not in assignment
               and other_variable_name not in neighbors):
                neighbors.append(other_variable_name)

        # Return the out degree of this variable.
        return len(neighbors)

    def get_binary_constraints(self):
        '''
        Variable Binary Constraint Accessor

        Accessor to get an object's binary constraints.

        :returns: CSPConstraint List of the variable's binary constraints
        '''
        return self._binary_constraints

    def get_neighbors(self):
        '''
        Variable Neighbor List Constructor

        Builds and returns a list of the names of all neighbors of this
        variable.

        :returns: str List of the names of this variable's neighbors.
        '''
        neighbors = []
        # Go through all of the variable's binary constraints.
        for constraint in self._binary_constraints:
            constraint_vars = constraint.get_variables()
            # Iterate through variables in the binary constraints
            for var_name in constraint_vars:
                # Only add a variable to neighbors if it is none duplicate
                # and not itself.
                if(var_name != self.name and var_name not in neighbors):
                    neighbors.append(var_name)
                    break
        # Return the list of neighbors
        return neighbors

    def get_neighbor_reduction_count(self, assignment, value, neighbor):
        '''
        Neighbor Domain Reduction Count Checker

        Determines the number of elements removed from the neighbor's domain.
        This is used in the Least Constraining Value heuristic where the lower
        the reduction in a neighbor's domain, the better.

        :param int assignment: Dictionary of values assigned to CSP variables
        :param int value: Value to be assigned to the implicit variable.
        :param CSPVariable neighbor: Neighbor value whose domain is checked

        :returns: int Number of elements removed from the neighbor's domain.  
        If the neighbors domain is emptied (i.e. no remaining entries in the
        domain), it returns maxint.
        '''
        size_reduction = len(self.get_neighbor_inconsistent_values(assignment, 
                                                                   value, 
                                                                   neighbor))
        if(size_reduction == len(neighbor._domain)):
            return sys.maxint
        else:
            return size_reduction

    def get_neighbor_inconsistent_values(self, assignment, value, neighbor):
        '''
        Neighbor Domain Reduction Generator

        Generates the list of the neighbor's domain values that will be removed
        if the implicit variable is assigned to the specified "value" in this
        assignment..

        :param int assignment: Dictionary of values assigned to CSP variables
        :param int value: Value to be assigned to the implicit variable.
        :param CSPVariable neighbor: Neighbor value whose domain is checked

        :returns: int List of inconsistent values in neighbor's domain
        '''
        # Get neighbor values remove
        removed_neighbor_values = []

        # Iterate through the list of neighbor values and get if this
        # assignment reduces its domain.
        for neighbor_val in neighbor._domain:
            # Iterate through all binary constraints
            for constraint in neighbor._binary_constraints:
                # Get the variables in the constraint.
                constraint_vars = constraint.get_variables()
                
                # Get the name of the variables 
                if(neighbor.name == constraint_vars[0]):
                    other_variable_name = constraint_vars[1]
                    neighbor_first_in_constraint = True 
                else:
                    other_variable_name = constraint_vars[0]
                    neighbor_first_in_constraint = False
                
                # If the other value is this value, get its value
                if(other_variable_name == self.name):
                    other_value = value
                # If the value is already assigned, then get the assigned value
                elif(other_variable_name in assignment):
                    other_value = assignment[other_variable_name]
                # Otherwise, go to the next constraint.
                else:
                    continue
                
                # If the constraints are not satisfied, then exclude this value.
                if(neighbor_first_in_constraint and
                   not constraint.check_satisfaction(neighbor_val, other_value)) \
                   or (not neighbor_first_in_constraint and
                       not constraint.check_satisfaction(other_value, neighbor_val)):
                        # if it is not satisfied, either update the reduction
                        # counter or mark the variable for removal
                        removed_neighbor_values.append(neighbor_val)
                        break

        # Return elements removed from the neighbor's domain
        return removed_neighbor_values

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

    def apply_inference(self, domain_values_to_remove):
        '''
        Variable Inference Applier

        Applies the inference to the implicit variable by removing those
        domain values that are specified in the input list for removal.

        :param int domain_values_to_remove: Values to be removed from the
        variable's domain.
        '''
        # Iterate through the list of variables to remove and then remove them
        for val_to_remove in domain_values_to_remove:

            # Sanity error checking.
            if(val_to_remove not in self._domain):
                raise RuntimeError("Error: Trying to remove a domain value "
                                   + "that does not exist. Exiting...")

            # Remove the value
            self._domain.remove(val_to_remove)

    def remove_inference(self, domain_values_to_restore):
        '''
        Variable Inference Remover

        Removes the inference to the implicit variable by re-appending those
        domain values that were previously removed.

        :param int domain_values_to_restore: Values to be restored in the
        variable's domain.
        '''
#         # Iterate through the list of variables to restore
#         for val_to_restore in domain_values_to_restore:
# 
#             # Sanity error checking.
#             if(val_to_restore in self._domain):
#                 raise RuntimeError("Error: Trying to restore a domain value "
#                                    + "that already exists. Exiting...")
# 
#             # Remove the value
#             self._domain.append(val_to_restore)

        self._domain += domain_values_to_restore

        # For debug clarity sort it after restoration.
        self._domain.sort()


# --------------------- CSP Class  ---------------------------#


class CSP:
    '''
    CSP Solver class.  This mimics the "CSP" object in
    the pseudocode in the textbook.
    '''
    def __init__(self, filename, forward_checking_flag):
        '''
        CSP Constructor

        :param str filename: Name of the file containing the CSP information
        :param int forward_checking_flag: 1 if forward checking is enabled
                                          0 if it is disabled.

        Builds the constraint satisifaction definition. It reads from the
        specified file and then builds the list of variables, builds the
        variable domains, and creates an empty CSP assignment.
        '''
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
        '''
        Backtrack Search Main Call

        Result: Prints "NO SOLUTION" if no solution is found.
        Otherwise, it prints the solution.
        '''
        # Get variables for performance tracking
        global numb_backtrack_calls, numb_var_sets, enable_performance_printing, \
            start_time

        # Start with an empty assignment
        self._assignment = {}
        solution = CSP._backtrack(self)
        # Get the end time.
        end_time = datetime.datetime.now()

        # Check the case where no solution was found
        if(solution is None):
            handle_no_solution()

        # Sort the solution list.
        output_list = []  # List will be sorted before outputting the result
        for var_name in self._assignment:
            output_list.append((var_name, self._assignment[var_name]))

        # Sort the output list.
        output_list.sort(key=lambda item: item[0])

        # Print the list.
        first_variable = True  # Flag for whether to print a preceding new line
        for var_and_value in output_list:
            output_str = ""

            # Print preceding new line on all variables after the first one.
            if(not first_variable):
                output_str += "\n"
            first_variable = False

            # Build the output string with var name and value.
            output_str += var_and_value[0] + "=" + str(var_and_value[1])
            print output_str,

        # If performance printing is enabled, print the performance.
        if(enable_performance_printing):
            print "\n\nThere were %d calls to \"backtrack\"." \
                % (numb_backtrack_calls)
            print "The variables were reset %d times." % (numb_var_sets)
            # print the elapsed time
            print "The elapsed time is %d.%03ds." \
                % ((end_time - start_time).seconds,
                   (end_time - start_time).microseconds/1e3)

    @staticmethod
    def _backtrack(csp):
        '''
        Recursive Backtracking Search Function

        Called as a static method by a CSP object.  It recurses searching for a
        solution to the specified CSP
        '''
        # Get variables for performance tracking
        global numb_backtrack_calls, numb_var_sets, enable_performance_printing

        # If the assignment is complete, then return true.
        # No need to check consistency since it is checked during assignment
        if(csp.is_assignment_complete()):
            return csp._assignment

        # Increment the number of times increment is called.
        if(enable_performance_printing):
            numb_backtrack_calls += 1

        # Select the next variable to be assigned using MRV Heuristic
        next_var = csp.select_unassigned_variable()

        # Order the domain values for that variable.
        next_var_domain = csp.order_domain_variables(next_var)

        # Iterate through the domain variables
        for d_i in next_var_domain:
            # If performance tracking is enabled, track the number times
            # a variable is set
            if(enable_performance_printing):
                numb_var_sets += 1

            # Try to assign the value to the variable
            if(csp.assign_variable_value(next_var, d_i)):

                # Generate the list of inferences
                inferences = csp.inference(next_var, d_i)

                # If inferences is not empty, then update domains
                # and set the next variable's value.
                if(inferences is not None):
                    # Apply the inferences
                    csp.apply_inferences(inferences)
                    # Run backtrack search with the reduced domains
                    result = CSP._backtrack(csp)
                    # If a solution is found, return it
                    if(result is not None):
                        return result
                    # Since no solution found, remove the inferences
                    csp.remove_inferences(inferences)

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
#         complete_assn = True  # By default assignment is complete.
#         for var in self._variables:
#             # Check if the variable is unassigned
#             if(self._variables[var].is_unassigned()):
#                 # Assignment not complete since var is unassigned
#                 complete_assn = False
#                 break
        return len(self._assignment) == len(self._variables)

    def select_unassigned_variable(self):
        '''
        CSP Variable Selection Algorithm

        Implements the Minimum Remaining Variable (MRV) algorithm.  In the case
        where two variables have the same MRV score, it then uses the degree
        heuristic to break the tie as described on pages 216 and 217 of the
        textbook.

        :returns: CSPVariable - Variable with the smallest remaining domain.
        '''
        # Initialize the variables for the initial setting.
        fail_first_variable = None
        minimum_domain_size = sys.maxint
        best_var_degree = -1
        # Find the variable with the smallest domain
        for var_name in self._variables:
            var = self._variables[var_name]
            
            # Variable must not already be unassigned
            # And the domain size must be smaller than current min
            if(var.is_unassigned()):
                var_domain_size = var.get_domain_size()
                # Check if one domain is smaller than the other first.
                if (var_domain_size < minimum_domain_size):
                    fail_first_variable = var
                    minimum_domain_size = var_domain_size
                    best_var_degree = var.get_degree(self._assignment)
                    
                # If the domains are the same size, then use the degree
                # heuristic to break the tie.
                elif(var_domain_size == minimum_domain_size):
                    var_out_degree = var.get_degree(self._assignment)
                    # Select this node if its out degree is higher.
                    if (var_out_degree > best_var_degree):
                        fail_first_variable = var
                        minimum_domain_size = var_domain_size
                        best_var_degree = var_out_degree
#         
#         if(len(fail_first_variable._domain) > 1):
#             x=1
#             x=x+1

        # Verify a valid variable was selected.
        if(fail_first_variable is None):
            raise RuntimeError("No variable was selected for assignment.")

        return fail_first_variable

    def order_domain_variables(self, variable):
        '''
        Backtrack Domain Variable Sorter

        :returns: int List of domain variables with values most likely to
        succeed in search first.
        '''
        # Create the array that stores how much each domain values constrains
        # other values
        constraining_val_list = []

        # Iterate through all domain variables.
        variable_domain = variable.get_domain()
        # on a domain of length one, no need to do any ordering.
        if(len(variable_domain) == 1): 
            return variable_domain
        # Get a list of the names of neighbors
        neighbor_names = variable.get_neighbors()
        # Iterate through all domain variables and determine the resulting
        # reduction in the domain of other variables.
        for d_i in variable_domain:
            # Initialize no domain sizes.
            domain_reduction = 0
            # Iterate through the list of neighbors
            for neighbor_name in neighbor_names:
                neighbor = csp._variables[neighbor_name]
                # Only check for domain reduction if the variable is unassigned
                if(not neighbor.is_unassigned()):
                    continue
                # Get the reduction of the neighbor's domain with this assn.
                element_count = variable.get_neighbor_reduction_count(self._assignment,
                                                                      d_i,
                                                                      neighbor)
                domain_reduction += element_count
                
            if(not variable._check_assignment_consistent(self._assignment, d_i)):
                domain_reduction = sys.maxint               

            # Append the domain value to the list as a tuple which includes
            # the value and the total domain reduction.
            constraining_val_list.append((d_i, domain_reduction))

        # Sort the variable constrain counts based of number of constrained
        # domains.
        constraining_val_list.sort(key=lambda value: value[1])

        # Build the output list of values
        output_list = []
        for val in constraining_val_list:
            # Array index 0 is the value
            output_list.append(val[0])
        # Output the list.
        return output_list

    def inference(self, variable, value):
        '''
        Arc Consistency Inference Algorithm

        This function generates an associative array of variable values
        to be removed given the assignment of "value" to the variable
        "variable".

        :param: CSPVariable variable: Variable to be assigned a value
        :param: int value: Value to be assigned to parameter "variable".

        :returns: Dictionary of values to be removed for the unassigned
        neighbors of "variable" if forward checking is enabled. Otherwise
        it returns an empty dictionary.
        '''
        # Iinitialize the inferences
        inferences = {}
        # If forward checking is not enabled, then return empty inferences
        if(not self._forward_check_enable):
            return inferences

        # Get a list of the variables neighbors
        neighbor_names = variable.get_neighbors()
        # Iterate through the neighbors
        for neighbor_name in neighbor_names:
            # Get the neighbor variable
            neighbor = csp._variables[neighbor_name]
            # Only check unassigned neighbors
            if(not neighbor.is_unassigned()):
                continue

            # Get the list of values to remove from the neighbor's domain
            val_to_remove = variable.get_neighbor_inconsistent_values(self._assignment,
                                                                      value,
                                                                      neighbor)

            # If the set of values to remove is empty, then go to next neighbor
            if(len(val_to_remove) == 0):
                continue
            # If after applying inferences the neighbor's domain is empty,
            # then return no inferences
            if(len(val_to_remove) == len(neighbor.get_domain())):
                return None

            # Since all criteria met, store the updated inference
            inferences[neighbor_name] = val_to_remove

        # Return the set of inferences
        return inferences

    def apply_inferences(self, inferences):
        '''
        CSP Inference Applies

        Applies the inferences specified in the input parameter "inferences"
        to all unassigned variables.

        :param dict inferences: Associative array of variable names and
        lists of domain variables to be removed for that variable.
        '''
        # Iterate through the variables whose domain is to be reduced through
        # inference and apply the inferences.
        for var_name in inferences:
            # Get the list of domain values to be removed from the variable's
            # domain
            values_to_remove = inferences[var_name]
            # Get the variable object
            var = self._variables[var_name]
            # Apply the inference
            var.apply_inference(values_to_remove)

    def remove_inferences(self, inferences):
        '''
        CSP Inference Remover

        Removes the inferences defined in the input parameter "inferences"
        from all unassigned variables.

        :param dict inferences: Associative array of variable names and
        lists of domain variables to be removed for that variable.
        '''
        # Iterate through the variables whose domain was reduced through
        # inference and remove the inferences.
        for var_name in inferences:
            # Get the list of domain values to be restored for the variable
            values_to_restore = inferences[var_name]
            # Get the variable object
            var = self._variables[var_name]
            # Remove the inference
            var.remove_inference(values_to_restore)


def handle_no_solution():
    '''
    Generic Handler of an invalid input and when there is no solution.

    Prints "NO SOLUTION" and cleanly exits the program.
    '''
    print "NO SOLUTION"
    sys.exit(0)

'''-----------------------------------------------------------------------
                         Parse Input Arguments
------------------------------------------------------------------------'''
# Verify the right number of input arguments specified.
if(len(sys.argv) > 3):
    handle_no_solution()

# Get the name of the file containing the csp definition
csp_info_file_name = sys.argv[1]

# Verify a valid flag for forward checking.
if(sys.argv[2] != "0" and sys.argv[2] != "1"):
    handle_no_solution()
# Extract the forward checking flag.
forward_checking_flag = int(sys.argv[2])

'''-----------------------------------------------------------------------
                   Build the CSP and then Run Search
------------------------------------------------------------------------'''

# Build the CSP
csp = CSP(csp_info_file_name, forward_checking_flag)

csp.execute_backtrack_search()
