import sys

from .core import generate_puzzle, is_anagram, solve
from subprocess import call


def clear():
    call(["clear"])


def play(difficulty=2):
    puzzle = generate_puzzle(int(difficulty), make_solvable=True)
    print('Puzzle: ', puzzle)
    while True:
        guess = input('Guess: ')
        if is_anagram(scrambled_puzzle=puzzle, solution=guess):
            print('Well done!\n')
            play(difficulty)
        elif guess == 'exit':
            sys.exit()
        elif guess == 'solve':
            print([solution for solution in solve(puzzle)], '\n')
            play(difficulty)
        elif guess in ['new', 'next']:
            print('\n')
            play(difficulty)
        else:
            print('Nope!')
            continue


def start():
    clear()
    print("Welcome to Flavius' Super Awesome Anagram Game! Press Enter to Begin...\n")
    preferred_difficulty = input('Pick a Difficulty [0-3]: ')
    print()
    if preferred_difficulty == '':
        preferred_difficulty = 2
    play(preferred_difficulty)
