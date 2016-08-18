def play_word_game():
    strikes = 0
    max_strikes = 3
    playing = True
    word = get_random_word()

    while playing:
        strikes += 1

        if strikes >= max_strikes:
            playing = False
    
    if strikes >= max_strikes:
        print("You lose")
    else:
        print("You win!")


def get_random_word():
    return "typewriter"

print("Game started")

play_word_game()

print("Game over")