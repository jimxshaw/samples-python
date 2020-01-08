import sys, random

print("Welcome to the Game of Thrones Name Generator\n")
print("Your name in the world of A Song of Ice and Fire would be: ")

first_list = ["Jon", "Tyrion", "Cersei", "Daenerys", "Jorah", "Samwell", "Robert", "Arya", "Margery", "Stannis", "Lysa"]

last_list = ["Lannister", "Targaryen", "Baratheon", "Stark", "Tyrell", "Martel", "Arryn", "Clegane", "Bolton", "Tully"]

while True:
    first_name = random.choice(first_list)
    last_name = random.choice(last_list)

    print(f"Hello, {first_name} of House {last_name}!\n")

    try_again = input("Try again? (Press Enter or else n to quit)\n")
    if try_again.lower() == "n":
        break

input("\nPress Enter to exit")