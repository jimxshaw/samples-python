#!/usr/bin/env python3

# Exercise 3-3 (string_fun.py)

# Write a script to prompt the user for a full name. Once the name is read in,
# do the following:

# - Print out the name as-is
# - Print the name in upper case
# - Print the name in title case
# - Print the number of occurrences of 'j'
# - Print the length of the name
# - Print the position (offset) of "jacob" in the string

# Run the program, and enter "john jacob jingleheimer smith"

full_name = input("Input your full name: ")

print(f"Full name: {full_name}")

print(f"Full name in upper case: {full_name.upper()}")

print(f"Full name in title case: {full_name.title()}")

print(f"Occurrences of the letter 'j': {full_name.lower().count('j')}")

print(f"Length of full name: {len(full_name)}")

print(f"Position of 'jacob': {full_name.find('jacob')}")
