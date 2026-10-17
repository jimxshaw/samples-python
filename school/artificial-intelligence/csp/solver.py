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
def satisfies(constraints, var1, val1, var2, val2):
    """
    Warning: a constraint ('A', '>', 'B') must also be checked when you are
    asked about (B, A) -- the order of the arguments may be flipped.
    """
    # TODO: step 2
    raise NotImplementedError("satisfies")

# Returns the set of variables that share at least one constraint with var.
# E.g. neighbors(constraints, 'A') -> {'B', 'C', 'D'}
def neighbors(constraints, var):
    # A set holds each name at most once so if two constraints link the same
    # pair of variables then that neighbor is still listed only once.
    neightbor_set = set()

    # Look at every constraint one at a time. Each constraint is a 3 item
    # tuple like ('A', '>', 'B'). We unpack the tuple by giving each
    # piece its own name.
    for left_variable, operator, right_variable in constraints:
        # Scenario 1: if var is on the LEFT side then the other variable
        # is on the right.
        if left_variable == var:
            neightbor_set.add(right_variable)
        # Scenario 2: if var is on the RIGHT side then the other variable
        # is on the left.
        elif right_variable == var:
            neightbor_set.add(left_variable)

        # Scenario 3: if var is on neither side then we skip it because
        # this constraint has nothing to do with var.

        # The unpacked operator is not used because neighbors only cares
        # about who is connect and not how they're connected.    

    return neightbor_set

# Returns the name of the next variable to assign using
# most constrained -> most constraining -> alphabetical.
def select_unassigned_variable(domains, assignment, constraints):
    # TODO: step 4 (start with plain alphabetical in step 3)
    raise NotImplementedError("select_unassigned_variable")

# Return var's current domain values as a list sorted by
# least constraining value. Ties goes to smaller value first.
def order_domain_values(var, domains, assignment, constraints):
    # TODO: step 4 (start with plain ascending order in step 3)
    raise NotImplementedError("order_domain_values")

# Build one output line. Must match the sample .out file exactly.
# E.g. "1. F=1, E=1, A=5, B=1  failure"
#      "3. F=1, E=1, A=5, B=2, C=2, D=1  solution"
def format_branch(branch_number, assignment, status):
    """
      - branch number, then a period, then ONE space
      - "NAME=value" with no spaces around '='
      - pairs separated by ", "
      - TWO spaces before "failure" / "solution"
    """
    # TODO: step 3
    raise NotImplementedError("format_branch")

# Run backtracking search and return the list of formatted branch lines
# with every failed branch plus the solution line if one is found.
def solve(domains, constraints, use_forward_checking):
    """
    Failure rules:
      - none mode: the new assignment breaks a constraint with an
                   already-assigned variable
      - fc mode:   additionally, after pruning neighbors' domains, some
                   unassigned variable is left with an EMPTY domain
    """
    # TODO: steps 3 and 5
    raise NotImplementedError("solve")
