#!/usr/bin/env python3

# Exercise 4-3 (guessx.py)

# Write a guessing game program. You will think of a number from 1 to 25,
# and the computer will guess until it figures out the number.

# Each time, the computer will ask:
#     "Is this your number?"

# You will enter:
#     "l" for too low,
#     "h" for too high,
#     or "y" when the computer has got it.

# Get the maximum number from the command line or 
# prompt the user to input the maximum.

# Print appropriate prompts and responses.

import sys

max_val = 26
min_val = 0

if len(sys.argv) < 2:
    max_val = int(input("Input a maximum integer: "))
else:
    max_val = int(sys.argv[1])

print(f"Think of a number from 1 to {max_val} and the Program will try to guess it.")

while True:
    guess = int((max_val + min_val) / 2)

    response = input(f"Is your number {guess}? ")

    if response == "y":
        print("I got it!")
        break
    elif response == "h":
        max_val = guess
    elif response == "l":
        min_val = guess
    else:
        continue


