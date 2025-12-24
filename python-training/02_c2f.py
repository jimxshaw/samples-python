#!/usr/bin/env python3

# Exercise 3-1 (c2f.py)

# Write a Celsius to Fahrenheit converter. Your script should prompt the user for a Celsius
# temperature, then print out the Fahrenheit equivalent.

# The program prompts the user, and the user enters the temperature to be converted.

# The formula is F = ((9 * C) / 5) + 32. Be sure to convert the user-entered value into a float.

# Test your script with the following values: 100, 0, 37, -40.

input_float = float(input("Input a temperature in Celcius: "))

result = ((9 * input_float) / 5) + 32

print(input_float, "Celcius is", result, "Fahrenheit")
