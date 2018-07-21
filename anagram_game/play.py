import datetime as dt
import sys
from subprocess import call

from anagram_game.core import generate_puzzle, is_anagram, solve

MAX_LEVELS = 3

level = 1
player = None
start_time = None


def clear():
    call(["clear"])


def draw_header():
    global level, player, start_time

    def pretty_time():
        time_since = dt.datetime.utcnow() - start_time
        time_tuple = divmod(time_since.days * 86400 + time_since.seconds, 60)
        return "{:02}:{:02}".format(*time_tuple)

    clear()
    header = "Name: {0} | Level: {1}/{2} | Time: {3}".format(player,
                                                             level if level < MAX_LEVELS else MAX_LEVELS,
                                                             MAX_LEVELS, pretty_time())
    print(header)
    print('-' * len(header))


def play():
    global level
    puzzle = generate_puzzle(difficulty=level, make_solvable=True)
    guesses = []
    while level <= MAX_LEVELS:
        clear()
        draw_header()
        print('Guessed: {0}\n'.format(sorted(list(set(guesses))) if len(guesses) > 0 else '') if len(
            guesses) > 0 else '')
        guess = input('{0} => '.format(puzzle))
        if is_anagram(scrambled_puzzle=puzzle, solution=guess):
            level += 1
            play()
        elif guess == 'exit':
            sys.exit()
        elif guess == 'solve':
            print('\tAnswers: ', [solution for solution in solve(puzzle)], '\n')
            input('Press any key to continue...')
            play()
        elif guess in ['new', 'next']:
            print('\n')
            play()
        elif guess == 'restart':
            start()
        elif guess == 'help':
            print('\tOptions: solve, new/next, restart, exit')
        elif guess == 'skip':
            level += 1
            if level > MAX_LEVELS:
                break
            else:
                play()
        else:
            guesses.append(guess)
            continue

    clear()
    draw_header()
    print("\nCongratulations, you win!\nPress any key to restart...")
    input()
    start()


def start():
    global player, start_time, level
    start_time = dt.datetime.utcnow()
    level = 1
    clear()
    print("Welcome to Flavius' Super Awesome Anagram Game!\n")
    name = input("What's your name?: ")
    player = name if name else 'Player 1'
    play()


if __name__ == '__main__':
    start()
