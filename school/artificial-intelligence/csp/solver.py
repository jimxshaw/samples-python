"""
solver.py: backtracking search for a CSP with optional forward checking.

Data shapes used:
    domains: dict name that are list of ints {'A': [1, 2, 3], ...}.

    constraints: list of (left, op, right) tuples [('A', '>', 'B'), ...].

    assignment: list of (name, value) tuples IN THE ORDER THEY WERE MADE!
                  [('F', 1), ('E', 1), ('A', 5)]
                  NOTE: use a list, not a dict, because the output prints assignments
                   in the order the search made them!

Heuristics required:
    pick variable: most constrained (smallest current domain)
                    - tie: most constraining (most constraints with
                       UNASSIGNED variables)
                    - tie: alphabetical
    order values: least constraining value (rules out the fewest values
                    in the unassigned neighbors' current domains)
                    - tie: smaller value first
"""

# Each operator mapped to a small function that tests two values.
# E.g. OPERATORS['>'](5, 3) -> True, 
#       OPERATORS['!'](2, 2) -> False.
OPERATORS = {
    "=": lambda a, b: a == b,
    "!": lambda a, b: a != b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
}

# Returns True if giving var1 = var1 and var2 = var2 breaks no 
# constraints between var1 and var2.
def satisfies(constraints, var1, value1, var2, value2):
    # Look at every constraint one at a time and unpack them into 3 pieces.
    for left_variable, operator, right_variable in constraints:
        # Convert the operator symbol into a test function.
        test = OPERATORS[operator]

        # Scenario 1: here the constraint is written in the same order
        # we were asked about: (var1, operator, var2). So we plug in the
        # values as is: value1 operator value2.
        if left_variable == var1 and right_variable == var2:
            if not test(value1, value2):
                # Even one broken rule is enough to fail.
                return False

        # Scenario 2: here the constraint is flipped: (var2, operator, var1).
        # So we keep the constraint's order and put each value with its own 
        # variable: value2 operator value1.
        # E.g. constraint ('A', '>' 'B') and asked about B = 2, A = 5
        #       so we test 5 > 2 with the A value on the left and NOT 2 > 5.
        elif left_variable == var2 and right_variable == var1:
            if not test(value2, value1):
                return False

        # Scenario 3: here the constraint is not between var1 and var2
        # so we skip it.

    # Getting here means every constraint was checked between the pair
    # and none failed. This also covers the scenario where no constraint
    # links the pair. With no rules between them then any two values are allowed. 
    return True

# Returns the set of variables that share at least one constraint with var.
# E.g. neighbors(constraints, 'A') -> {'B', 'C', 'D'}
def neighbors(constraints, var):
    # A set holds each name at most once so if two constraints link the same
    # pair of variables then that neighbor is still listed only once.
    neighbor_set = set()

    # Look at every constraint one at a time. Each constraint is a 3 item
    # tuple like ('A', '>', 'B'). We unpack the tuple by giving each
    # piece its own name.
    for left_variable, operator, right_variable in constraints:
        # Scenario 1: if var is on the LEFT side then the other variable
        # is on the right.
        if left_variable == var:
            neighbor_set.add(right_variable)
        # Scenario 2: if var is on the RIGHT side then the other variable
        # is on the left.
        elif right_variable == var:
            neighbor_set.add(left_variable)

        # Scenario 3: if var is on neither side then we skip it because
        # this constraint has nothing to do with var.

        # The unpacked operator is not used because neighbors only cares
        # about who is connect and not how they're connected.    

    return neighbor_set

# Returns the name of the next variable to assign using
# most constrained -> most constraining -> alphabetical.
def select_unassigned_variable(domains, assignment, constraints):
    # First, figure out which variables still need a value.
    assigned_names = set()
    for variable_name, value in assignment:
        assigned_names.add(variable_name)

    unassigned_names = []
    for variable_name in domains:
        if variable_name not in assigned_names:
            unassigned_names.append(variable_name)

    # Second, walk the candidates in alphabetical order and keep the best
    # one seen so far. Because we go alphabetically and only replace the
    # current best when a candidate is strictly better. A full tie is 
    # automatically won by the alphabetically first name.
    best_name = None
    best_domain_size = None
    best_degree = None

    for candidate in sorted(unassigned_names):
        # Rule 1: most constrained is the fewest values
        # left, meaning smaller wins.
        domain_size = len(domains[candidate])

        # Rule 2: most constraining is involved in the most constraints with
        # other unassigned variables, meaning bigger wins. Constrains with
        # already assigned variables don't count because they can't 
        # restrict any future choice anymore.
        degree = 0
        for left_variable, operator, right_variable in constraints:
            if (left_variable == candidate 
                    and right_variable not in assigned_names 
                    and right_variable != candidate):
                degree += 1
            elif (right_variable == candidate 
                    and left_variable not in assigned_names 
                    and left_variable != candidate):
                degree += 1

        # Decide if this candidate beats the best so far.
        if best_name is None:
            is_better = True # First candidate.
        elif domain_size < best_domain_size:
            is_better = True # Rule 1 decides.
        elif domain_size == best_domain_size and degree > best_degree:
            is_better = True # Tie means rule 2 decides.
        else:
            is_better = False # Worse or a full tie. Earlier name keeps it.

        if is_better:
            best_name = candidate
            best_domain_size = domain_size
            best_degree = degree

    return best_name

# Return var's current domain values as a list sorted by
# least constraining value. Ties goes to smaller value first.
def order_domain_values(var, domains, assignment, constraints):
    # First, which neighbors of var are still unassigned? Only
    # their options matter, meaning assigned variables have
    # nothing left to rule out.
    assigned_names = set()
    for variable_name, value in assignment:
        assigned_names.add(variable_name)

    unassigned_neighbors = []
    for neighbor in neighbors(constraints, var):
        if neighbor not in assigned_names:
            unassigned_neighbors.append(neighbor)

    # Second, for each candidate value, count how many neighbor values it
    # would rule out. 
    # E.g. Choosing A=5 under "A > B" rules out only B=5. 
    #       Choosing A=2 rules out B=2, B=3, B=4, B=5. Fewer is better.
    scored_values = [] # Will hold (ruled_out_count, value) pairs.

    for value in domains[var]:
        ruled_out_count = 0
        for neighbor in unassigned_neighbors:
            for neighbor_value in domains[neighbor]:
                if not satisfies(constraints, var, value, neighbor, neighbor_value):
                    ruled_out_count += 1
        scored_values.append((ruled_out_count, value))

    # Third, sort the pairs. Python sorts tuples item by item, such as 
    # sorting by last name then first name.
    #   - First by ruled_out_count, smallest first. (least constraining)
    #   - On a tie, by value, smallest first. (the tie-breaker)
    # so both rules come from this one sort.
    scored_values.sort()
    
    # Fourth, strip off the counts and return just the values in order.
    ordered_values = []
    for ruled_out_count, value in scored_values:
        ordered_values.append(value)

    return ordered_values

# Build one output line. Must match the sample .out file exactly.
# E.g. "1. F=1, E=1, A=5, B=1  failure"
#      "3. F=1, E=1, A=5, B=2, C=2, D=1  solution"
def format_branch(branch_number, assignment, status):    
    pair_strings = []

    # Turn each (name, value) pair into a "NAME=value" string.
    # Assignment is a list in the order the search made
    # the assignments like [('F', 1), ('E', 1), ('A', 5)] so
    # the output keeps that order.
    for variable_name, value in assignment:
        pair_strings.append(variable_name + "=" + str(value))

    # E.g. ["F=1", "E=1", "A=5"] becomes "F=1, E=1, A=5".
    pairs_text = ", ".join(pair_strings)

    # Status is the word "failure" or "solution" input by the caller.
    line = str(branch_number) + ". " + pairs_text + "  " + status

    return line

# Run backtracking search and return the list of formatted branch lines
# with every failed branch plus the solution line if one is found.
def solve(domains, constraints, use_forward_checking):
    # Every branch line we produce goes here in order. 
    branch_lines = []

    # Recursive helper function is defined here so it can see the branch_lines list,
    # constraints and use_forward_checking boolean without passing them
    # around every call.
    #   assignment: list of (name, value) pairs made so far in order.
    #   current_domains: dictionary name of list of values still allowed.
    # Returns True as soon as a solution is found, so every caller up to the chain
    # can stop, or returns False if this whole subtree is a dead end.
    def backtrack(assignment, current_domains):
        # Base case: every variable has a value so this is the solution.
        if len(assignment) == len(domains):
            line_number = len(branch_lines) + 1
            branch_lines.append(format_branch(line_number, assignment, "solution"))
            
            return True

        # Choose which variable is next then the order to try its values.
        variable = select_unassigned_variable(current_domains, 
                                                assignment, 
                                                constraints)
        ordered_values = order_domain_values(variable, 
                                                current_domains, 
                                                assignment,
                                                constraints)
        
        for value in ordered_values:
            # The branch we're about to try is everything so far plus this one.
            # Build a new list so the original is not touched and the next
            # loop iteration starts clean.
            new_assignment = assignment + [(variable, value)]

            # Consistency check asks does variable = value break a constraint
            # with any variable that is already assigned?
            is_consistent = True

            for assigned_name, assigned_value in assignment:
                if not satisfies(constraints, variable, value, assigned_name, assigned_value):
                    is_consistent = False
                    # One broken constraint is enough.
                    break

            if not is_consistent:
                # Dead end: record this branch as a failure, try next value.
                line_number = len(branch_lines) + 1
                branch_lines.append(format_branch(line_number, new_assignment, "failure"))
                continue

            # Make a copy of the domains for the next level and fix this variable's
            # domain to just the chosen value. Copying means anything the next level
            # changes is thrown away automatically when we come back up. That is
            # the "undo" of backtracking.
            next_domains = {}                
            for name in current_domains:
                next_domains[name] = list(current_domains[name])
            next_domains[variable] = [value]

            # Forward Checking only in "fc" mode.
            # Look ahead, for every unassigned neighbor of the variable we just we
            # throw away the values that no longer work with variable = value.
            # If some neighbor ends up with nothing left, it can never be assigned
            # so this branch is already dead. Record it as a failure now
            # instead of discovering it later.
            if use_forward_checking:
                # Names that have a value including the one just chosen.
                assigned_names = set()
                for assigned_name, assigned_value in new_assignment:
                    assigned_names.add(assigned_name)

                domain_wiped_out = False

                for neighbor in neighbors(constraints, variable):
                    # Assigned neighbors were already checked above.
                    if neighbor in assigned_names:
                        continue

                    # Keep only the neighbor's values that still work.
                    # We edit next_domains (our private COPY), so the
                    # pruning is undone automatically if we backtrack.
                    surviving_values = []
                    for neighbor_value in next_domains[neighbor]:
                        if satisfies(constraints, variable, value, neighbor, neighbor_value):
                            surviving_values.append(neighbor_value)
                    next_domains[neighbor] = surviving_values

                    # Empty domain = this neighbor has no possible value.
                    if len(surviving_values) == 0:
                        domain_wiped_out = True
                        # No need to prune the remaining neighbors.
                        break    

                if domain_wiped_out:
                    line_number = len(branch_lines) + 1
                    branch_lines.append(format_branch(line_number, new_assignment, "failure"))
                    # Try the next value for this variable.
                    continue 

            # Recursion here, go one level deeper with the bigger assignment.
            # If that finds a solution, stop here too and pass True up.
            if backtrack(new_assignment, next_domains):
                return True

            # Otherwise the loop moves on to the next value.

        # Every value for this variable failed so this subtree is a dead end.
        # Return False so the level above tries its next value.
        return False

    # Kick off the search where nothing is assigned yet with full original domains.
    backtrack([], domains)

    return branch_lines
