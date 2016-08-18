import random

def play_word_game():
    strikes = 0
    max_strikes = 3
    playing = True
    word = get_random_word()
    masked_word = list("_" * len(word))

    while playing:
        show_word(masked_word)
        letter = get_guess()
        letter_is_found = process_letter(letter, word, masked_word)

        if not letter_is_found:
            strikes += 1
            print_strikes(strikes)

        if strikes >= max_strikes:
            playing = False
            
        if not "_" in masked_word:
            playing = False

    if strikes >= max_strikes:
        print("You lose")
    else:
        print("You win!")


def get_random_word():
    words = ["orange", "banana", "pineapple", "watermelon", "grapefruit", "honeydew", "mango", "papaya"]
    word = words[random.randint(0, len(words) - 1)]
    return word


def show_word(word):
    for character in word:
        print(character, " ", end="")
    print("")


def get_guess():
    print("Enter a letter: ")
    return input() 


def process_letter(letter, secret_word, masked_word):
    result = False

    for i in range(0, len(secret_word)):
        if secret_word[i] == letter:
            result = True
            masked_word[i] = letter
    return result


def print_strikes(number_of_strikes):
    for i in range(0, number_of_strikes):
        print("X ", end="")
    print("")


print("Game started")

play_word_game()

print("Game over")