#!/usr/bin/env python3

# Exercise 4-1 (c2f_loop.py)

# Redo c2f.py to repeatedly prompt the user for a Celsius temperature to convert
# to Fahrenheit and then print the result. If the user just presses Return,
# go back to the top of the loop. Quit when the user enters "q".

user_input = ""

while True:
    user_input = input("Input a temperature in Celcius or q to Quit: ")

    if user_input == "q":
        break
    elif user_input == "":
        continue
    else:
        result = ((9 * float(user_input)) / 5) + 32
        print(user_input, "Celcius is", result, "Fahrenheit")
