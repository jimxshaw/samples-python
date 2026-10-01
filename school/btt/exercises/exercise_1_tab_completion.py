"""
Exercise 1: Tab completion warm-up

None of the functions below do anything yet. Each one has a comment
describing what it should do and a `pass` placeholder instead of real
code.

For each function: delete the `pass` line, put your cursor there, and
start typing. Once GitHub Copilot is enabled, it will offer a suggestion as gray "ghost
text." Press Tab to accept it, Esc to dismiss it, or keep typing your
own version.
"""
import math

def square(n):
    # Return the square of n.
    return n * n

print("square")
print(square(7))

def is_prime(n):
    # Return True if n is prime, False otherwise.
    if n <= 1:
        return False

    # 2 is the only even prime number.
    if n == 2:
        return True

    # Exclude all other event numbers.
    if n % 2 == 0:
        return False

    # Check add factors up to the square root of n.
    for i in range(3, int(math.sqrt(n) + 1), 2):
        if n % i == 0:
            # Found a factor so it's not prime.
            return False

    # No factors found so it's prime.
    return True

print("is_prime")
print(is_prime(247323))


def filter_by_length(strings, min_length):
    # Return only the strings from `strings` that are at least
    # `min_length` characters long.
    results = []

    for string in strings:
        if len(string) <= min_length:
            results.append(string)

    return results

print("filter_by_length")
print(filter_by_length(["hello", "world", "a", "woah", "serious", "what", "development"], 4))

def reverse_sentence(sentence):
    # Reverse the word order of `sentence`.
    # "hello world" becomes "world hello".
    return " ".join(sentence.split()[::-1])

print("reverse_sentence")
print(reverse_sentence("hello world"))
