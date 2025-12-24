#!/usr/bin/env python3

# Exercise 3-2 (c2f_batch.py)

# Create another C to F converter. This time, your script should take the Celsius temperature from
# the command line and output the Fahrenheit value. What you will type:

#     python c2f_batch.py 100

# Test with the values from c2f.py.

# These two programs should be identical, except for the input.

import sys

input_float = float(sys.argv[1])

result = ((9 * input_float) / 5) + 32

print("Input temperature of", input_float, "Celcius is", result, "Fahrenheit")
