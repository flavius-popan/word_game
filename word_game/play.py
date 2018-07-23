import datetime as dt
import sys
from subprocess import call

from word_game.core import generate_puzzle, is_anagram, solve

MAX_LEVELS = 3

level = 1
player = None
start_time = None

unsolvable_puzzle = ''
intractable_presented = False


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
    global level, intractable_presented, unsolvable_puzzle
    # Present an unsolvable puzzle on final level but only once. Can be solved/skipped.
    if level == MAX_LEVELS and not intractable_presented:
        intractable_presented = True
        puzzle = unsolvable_puzzle
    else:
        puzzle = generate_puzzle(difficulty=level, is_solvable=True)
    guesses = []
    while level <= MAX_LEVELS:
        clear()
        draw_header()
        print('Guessed: {0}\n'.format(sorted(list(set(guesses))) if len(guesses) > 0 else '') if len(
            guesses) > 0 else '')

        if len(guesses) > 7:
            print("Stuck? Type 'new' to try another word\n")

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
            print('\nOptions: solve - show solutions\n\t new/next - generate a new puzzle on the same level\n\t'
                  ' restart - restart the whole game\n\t exit - quit the game\n\n\t Press any key to continue...')
            input()
            continue
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
    # TODO: Add data writer
    start()


def start():
    global player, start_time, level, unsolvable_puzzle
    # Pre-generate unsolvable puzzle before game begins
    unsolvable_puzzle = generate_puzzle(difficulty=3, is_solvable=False)
    clear()
    print("Welcome to the Anagram Game!\n")
    name = input("What's your name?: ")
    player = name if name else 'Player 1'
    perfection_ans = input("Are you a perfectionist? [Y or N]: ")
    perfection_ans.lower()
    start_time = dt.datetime.utcnow()
    play()


if __name__ == '__main__':
    start()
