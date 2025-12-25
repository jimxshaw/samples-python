#!/usr/bin/env python3

# Exercise 4-2 (guess.py)

# Write a guessing game program. You will think of a number from 1 to 25,
# and the computer will guess until it figures out the number.

# Each time, the computer will ask:
#     "Is this your number?"

# You will enter:
#     "l" for too low,
#     "h" for too high,
#     or "y" when the computer has got it.

# Print appropriate prompts and responses.

max_val = 26
min_val = 0

print("Think of a number from 1 to 25 and the Program will try to guess it.")

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
