# Propositional Resolution Theorem Prover.
# Input: First n-1 lines = Knowledge Base clauses (CNF),
#           last line = clause to test. Literals 
#           are space-separated. Negation is a '~' prefix.
# Output: Every clause in the final KB, numbered with parents {i, j}
#           then 'Valid' or 'Fail'.

import sys

# Constants.
NEGATION = "~"
CONTRADICTION = "Contradiction"
VALID = "Valid"
FAIL = "Fail"
NO_PARENTS = None # Market for clauses that came fro the input file.

# Literal helpers.
def negate_literal(literal):
    # Return the complement of a literal: p -> ~p, ~p -> p.
    if literal.startswith(NEGATION):
        return literal[1:]
    
    return NEGATION + literal

# Clause helpers.
# A clause is stored as a tuple of ltieral. The tuple keeps left-to-right
# order, which is needed for printing. The frozenset(clause) is the 
# order-free identity, which is needed for redudancy.
def remove_duplicate_literals(literals):
    # Drop the repeated literals and keep the first occurrence's position.
    seen = set()
    unique_literals = []

    for literal in literals:
        if literal not in seen:
            seen.add(literal)
            unique_literals.append(literal)

    return tuple(unique_literals)

def parse_clause(line):
    # Turn one input line like '~p q' into a clause tuple ('~p', 'q').
    return remove_duplicate_literals(line.split())

def is_tautology(clause):
    # True if the clause contains both a literal and its complement.
    literal_set = set(clause)

    return any(negate_literal(literal) in literal_set for literal in clause)

def negate_goal(goal_clause):
    # Negate the goal: ~(a v b v c) = ~a ^ ~b ^ ~c.
    # Return a list of unit clauses, in left-to-right order.
    return [(negate_literal(literal),) for literal in goal_clause]

# Resolution.
def resolve(clause_i, clause_j):
    # Find every complementary pair.
    # Time complexity is O(1) membership checks.
    clause_j_literals = set(clause_j)

    clashing_literals_in_i = []

    for literal in clause_i:
        complement = negate_literal(literal)
        if complement in clause_j_literals:
            clashing_literals_in_i.append(literal)

    # Exactly one clash or nothing useful.
    number_of_clashes = len(clashing_literals_in_i)

    if number_of_clashes != 1:
        return None

    # The single pair being resolved on.
    literal_removed_from_i = clashing_literals_in_i[0] # E.g. 'z'.
    literal_removed_from_j = negate_literal(literal_removed_from_i) # E.g. '~z'.

    # Leftovers, clause_i's first then clause_j's.
    leftover_literals = []

    for literal in clause_i:
        if literal != literal_removed_from_i:
            leftover_literals.append(literal)

    for literal in clause_j:
        if literal != literal_removed_from_j:
            leftover_literals.append(literal)

    # Drop repeats. A () would mean Contradiction.
    resolvent = remove_duplicate_literals(leftover_literals)

    return resolvent

# Output.
def format_clause_line(clause_number, clause, parents):
    # Build one output line, e.g. '9. q ~p y {4,2}' or '1. ~p q {}'.
    clause_text = " ".join(clause) if clause else CONTRADICTION
    parents_text = "{}" if parents is NO_PARENTS else "{%d,%d}" % parents
    
    return "%d. %s %s" % (clause_number, clause_text, parents_text)

# Main program.
def read_input_file(file_path):
    # Return (kb_clauses, goal_clause) from the KB file, skipping blank lines.
    with open(file_path) as input_file:
        lines = [line.strip() for line in input_file if line.strip()]

    kb_clauses = [parse_clause(line) for line in lines[:-1]]
    goal_clause = parse_clause(lines[-1])

    return kb_clauses, goal_clause

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <input.kb>")
        sys.exit(1)
 
    kb_clauses, goal_clause = read_input_file(sys.argv[1])
 
    # Parallel lists where index k holds clause k+1 and its parents.
    clauses = [] # List of clause tuples in the order they were added.
    parents = [] # List of (i, j) tuples. or NO_PARENTS.
    seen_clauses = set() # Frozensets of every clause in the KB with O(1) lookup.
 
    # Load the KB then the negated goal's unit clauses.
    for clause in kb_clauses + negate_goal(goal_clause):
        clauses.append(clause)
        parents.append(NO_PARENTS)
        seen_clauses.add(frozenset(clause))
 
    # Execute the resolution loop.
    # TODO

    found_contradiction = False
 
    # Print the KB then the verdict.
    for index, clause in enumerate(clauses):
        print(format_clause_line(index + 1, clause, parents[index]))

    print(VALID if found_contradiction else FAIL)

if __name__ == "__main__":
    main()
