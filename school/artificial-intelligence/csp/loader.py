"""
loader.py: reads the input files into plain Python data.

.var file has one variable per line:
    A: 1 2 3 4 5
    F: 1 2           

.con file has one constraint per line where operator is one of  =  !  >  <
    A > B
    D = E            
"""

# Reads in a .var file.
# Returns a dictionary mapping variable name:
#   list of integer values in file order
#   {'A': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5], ..., 'F': [1, 2]}
def load_variables(path):
    # Python dictionaries remember insertion order so 
    # variables stay in file order.
    domains = {}

    with open(path) as file:
        for raw_line in file:
            # Remove the leading and trailing whitespace, such as
            # the newline "\n" and spaces at the end.
            line = raw_line.strip()

            # Skip blank lines.
            if not line:
                continue

            # Split the input "A: 1 2 3 4 5" at the colon to two parts with
            # first part being "A" and second being " 1 2 3 4 5".
            # Split's 1 argument means split at most once.
            name_part, values_part = line.split(":", 1)

            # Cleans the name in case it was "A :", for example.
            variable_name = name_part.strip()

            # Splitting with no argument splits on any run of whitespaces
            # and ignores leading and trailing spaces.
            # E.g. " 1 2 3 4 5".split() becomes ["1", "2", "3", "4", "5"].
            value_strings = values_part.split()
 
            values = []

            # Convert each string into an integer.
            for value_string in value_strings:
                values.append(int(value_string))
 
            domains[variable_name] = values

    return domains

# Reads in a .con file.
# Returns a list of tuples of (left_var, operator, right_var) in file order
#   [('A', '>', 'B'), ('B', '>', 'F'), ..., ('D', '=', 'E')]
def load_constraints(path):
    # This will be a list filled with 3 item tuples.
    constraints = []

    with open(path) as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line:
                continue

            # Input of "A > B".split() would output ["A", ">", "B"].
            # If a line has fewer than or more than 3 pieces then Python
            # would raise an error.
            left_variable, operator, right_variable = line.split()
 
            constraints.append((left_variable, operator, right_variable))

    
    return constraints

