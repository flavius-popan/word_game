import datetime as dt
import sys
from subprocess import call

from .core import generate_puzzle, is_anagram, solve

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
    header = "Name: {0} | Level: {1} | Time: {2}".format(player, level, pretty_time())
    print(header)
    print('-' * len(header), '\n')


def play():
    global level
    draw_header()
    puzzle = generate_puzzle(difficulty=level, make_solvable=True)
    while level != 4:
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
            play()
        else:
            continue

    print('Congratulations! You win!\n')
    input("Press any key to restart...")


def start():
    global player, start_time
    start_time = dt.datetime.utcnow()
    clear()
    print("Welcome to Flavius' Super Awesome Anagram Game!\n")
    name = input("What's your name?: ")
    player = name if name else 'Player 1'
    play()
