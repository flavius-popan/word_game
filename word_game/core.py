from itertools import permutations
from random import choice, shuffle

VOWELS = ['a', 'e', 'i', 'o', 'u']
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
RESERVED_WORDS = ['next', 'restart', 'skip', 'exit', 'solve']

MAX_LENGTH = 8
# Cut WORD_LIST down to max_length, strip newlines, and lower
WORD_LIST = [word.strip('\n').lower() for word in open("word_game/words.txt") if len(word) <= MAX_LENGTH]


def get_random_word() -> str:
    """Return a random word string from the dictionary."""
    random_word = choice(WORD_LIST)
    return random_word if random_word not in RESERVED_WORDS else get_random_word()


def calculate_difficulty_rating(word: str) -> int:
    """Computes an integer rating from 1-3 of how difficult an anagram is to solve.

    :param word: Can be any random string, either the word or the scrambled anagram.
    """
    difficulty = 1
    word = word.lower()
    word_length = len(word)

    if word_length < 4:
        difficulty = 1
    elif 4 <= word_length <= 5:
        difficulty = 2
    elif word_length > 5:
        difficulty = 3

    # I'm making an untested assumption that more vowels makes this easier. Hope its true ¯\_(ツ)_/¯
    # Calculate the ratio of vowels to consonants in a range of 0.0 (no vowels) to 1.0 (all vowels)
    # vowels_ratio = sum([Counter(word)[letter] for letter in VOWELS]) / len(word)
    # if vowels_ratio <= 0.5:
    #     difficulty += 1
    # elif vowels_ratio > 0.5:
    #     difficulty -= 1

    return difficulty


def generate_puzzle(difficulty: int = 1, make_solvable: bool = True) -> str:
    """Selects a word from the dictionary, shuffles it, and returns it as a string.

    :param difficulty: 1=Easy, 2=Normal, 3=Hard. Defaults to Easy.
    :param make_solvable: If set to False, returns a puzzle that cannot be solved. Defaults to True.
    """

    def random_replace_letter(letters: list):
        # TODO: Make sure it has at least one vowel
        # Replace consonant specifically to keep the word looking legit
        random_index = choice(range(len(letters)))
        letters[random_index] = choice(LETTERS)
        return letters

    while True:
        word = get_random_word()
        word_list = list(word)
        if calculate_difficulty_rating(word) == difficulty:
            shuffle(word_list)
            if ''.join(word_list) != word:  # Ensure shuffle doesn't produce the same word as answer
                break
        else:
            continue

    if make_solvable:
        word = ''.join(word_list)
        # Ensure we're not providing a word that is already in the dict
        return word if word not in WORD_LIST else generate_puzzle(difficulty, make_solvable)
    else:
        bad_puzzle = ''.join(random_replace_letter(word_list))
        return bad_puzzle if not solvable(bad_puzzle) else generate_puzzle(difficulty, make_solvable)


def solve(puzzle: str) -> set:
    """Attempts to find all anagrams from the answer.

    :param puzzle: Any string will do.
    """

    def permutation_generator(answer):
        for guess in permutations(answer, len(answer)):
            guess = ''.join(guess)
            if guess != answer and guess in WORD_LIST:
                yield guess

    anagrams = permutation_generator(puzzle)
    solutions = set(solution for solution in anagrams)  # EXPENSIVE! This is where optimizations should go.
    return solutions if len(solutions) > 0 else {}


def solvable(answer: str) -> bool:
    return True if solve(answer) else False


def is_anagram(scrambled_puzzle: str, solution: str) -> bool:
    """Helper method to verify solutions. Good for checking single guesses.

    :param scrambled_puzzle: The scrambled string provided by generate_puzzle().
    :param solution: The user's guess.
    """
    puzzle_list = list(scrambled_puzzle)
    puzzle_list.sort()
    answer_list = list(solution)
    answer_list.sort()

    if len(scrambled_puzzle) == len(solution):
        same = True
    else:
        return False

    i = 0
    while i < len(scrambled_puzzle) and same:
        if answer_list[i] == puzzle_list[i]:  # Compare letters at each index after sorting
            i += 1
        else:
            same = False

    return True if solution in WORD_LIST and same else False
