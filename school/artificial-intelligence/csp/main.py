"""
main.py 

Usage:
    python3 main.py <file.var> <file.con> <none or fc>

This file only puts things together. The real functionalities are in:
    loader.py: reads the .var and .con files into Python data.
    solver.py: runs backtracking search, with or without forward checking.

Requirements: stdout is graded byte-for-byte. Only the branch lines may be
printed to stdout. Send any debugging output to stderr instead:
    print("debug stuff", file=sys.stderr)
"""
import sys
import loader
import solver

def main():
    # Step 1, check the command line arguments.
    # First argument argv[0] is the script name so we need 4 total arguments.
    if len(sys.argv) != 4:
        print("How to use: python3 main.py <file.var> <file.con> <none or fc>", file = sys.stderr)
        sys.exit(1)

    var_path = sys.argv[1]
    con_path = sys.argv[2]
    mode = sys.argv[3]

    if mode not in ("none", "fc"):
        print("Third argument must be 'none' or 'fc'!", file = sys.stderr)
        sys.exit(1)

    # Step 2, load the problem.
    # domains: dict like {'A': [1, 2, 3, 4, 5], 'B': [...], ...}.
    # constraints: list of tuples like [('A', '>', 'B'), ('D', '=', 'E')].
    domains = loader.load_variables(var_path)
    constraints = loader.load_constraints(con_path)

    # Step 3, execute the solve.
    # The solver returns the branch lines as a list of already formatted strings,
    # like ["1. F=1, E=1, A=5, B=1  failure", ...].
    use_forward_checking = (mode == "fc")
    branch_lines = solver.solve(domains, constraints, use_forward_checking)

    # Step 4, print out each branch on its own line. Nothing else outputs to stdout.
    for line in branch_lines:
        print(line)

if __name__ == "__main__":
    main()
