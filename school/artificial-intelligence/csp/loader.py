"""
loader.py: reads the input files into plain Python data.

.var file has one variable per line:
    A: 1 2 3 4 5
    F: 1 2           
    NOTE: lines may have trailing spaces!

.con file has one constraint per line where operator is one of  =  !  >  <
    A > B
    D = E            
    NOTE: the last line may have no newline at the end!
"""

# Reads in a .var file.
# Returns a dictionary mapping variable name:
#   list of integer values in file order
#   {'A': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5], ..., 'F': [1, 2]}
def load_variables(path):
    """
      - open the file and loop over its lines
      - skip blank lines (after .strip())
      - split each line on ':' to separate the name from the values
      - .split() the values part, and convert each piece with int(...)
    """
    # TODO: step 1
    raise NotImplementedError("load_variables")

# Reads in a .con file.
# Returns a list of tuples of (left_var, operator, right_var) in file order
#   [('A', '>', 'B'), ('B', '>', 'F'), ..., ('D', '=', 'E')]
def load_constraints(path):
    """
      - skip blank lines
      - .split() with no argument splits on any whitespace -> 3 pieces
    """
    # TODO: step 1
    raise NotImplementedError("load_constraints")
