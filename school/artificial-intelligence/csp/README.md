## Run

    python3 main.py <file.var> <file.con> <none|fc>

- `none` runs plain backtracking search.
- `fc` runs backtracking with forward checking.
- Python 3 only, no external libraries.

## Files

- `main.py`: entry point. Checks the arguments, calls the loader and solver, prints the branch lines.
- `loader.py`: reads the .var and .con files.
- `solver.py`: backtracking search, forward checking, and the heuristics:
  - variable: most constrained, then most constraining, then alphabetical
  - value: least constraining, then smaller value first

## Output

Each branch is printed on its own line as `N. VAR=val, ...  failure|solution`. Nothing else goes to stdout. b