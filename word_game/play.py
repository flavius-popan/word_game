import datetime as dt
import sys
from subprocess import call

from word_game.core import generate_puzzle, is_anagram, solve

# from word_game.data_layer import save_data

MAX_LEVELS = 3

level = 1
player = None
start_time = None
perfectionist = False
unsolvable_puzzle = ''
intractable_guesses = 0
intractable_seconds = 0
intractable_timer = None
intractable_skipped = False


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
    global intractable_guesses, intractable_seconds, start_time, player
    global level, intractable_skipped, unsolvable_puzzle, intractable_timer
    # Present an unsolvable puzzle on final level but only once. Must be skipped.
    if level == MAX_LEVELS and not intractable_skipped:
        puzzle = unsolvable_puzzle
        intractable_timer = dt.datetime.utcnow()
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
            # Handle skipping unsolvable puzzle
            if level == MAX_LEVELS and not intractable_skipped:
                intractable_skipped = True
                intractable_guesses = len(guesses)
                intractable_seconds = int((dt.datetime.utcnow() - intractable_timer).total_seconds())
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
    # save_data(name=player,
    #           perfectionist=perfectionist,
    #           guesses=intractable_guesses,
    #           intractable_time_sec=intractable_seconds,
    #           total_time_sec=int((dt.datetime.utcnow() - start_time).total_seconds()))
    start()


def start():
    global player, start_time, level, unsolvable_puzzle, perfectionist
    level = 1
    # Pre-generate unsolvable puzzle before game begins
    # TODO: Generate this in a separate thread to keep game loop from stalling on init
    unsolvable_puzzle = generate_puzzle(difficulty=3, is_solvable=False)
    clear()
    print("Welcome to the Word Game!\n")
    name = input("What's your name?: ")
    player = name if name else 'Player 1'
    perfection_ans = input("Are you a perfectionist? [Y or N]: ")
    perfectionist = True if perfection_ans.lower() in ['y', 'yes', 'ya', 'yup', 'si'] else False
    start_time = dt.datetime.utcnow()
    play()


if __name__ == '__main__':
    start()
