import random

print("Input your favorite number")

number = input()

print("Your favorite number is " + number)

minNumber = 1
maxNumber = 100

magicNumber = random.randint(minNumber, maxNumber)

message = "The magic number is within {0} and {1}, inclusive"
print(message.format(minNumber, maxNumber))

found = False

while not found:
    print("Guess the magic number!")
    guess = int(input())
    
    if guess == magicNumber:
        found = True
    if guess < magicNumber:
        print("Too low")
    if guess > magicNumber:
        print("Too high")

print("You got it!")
