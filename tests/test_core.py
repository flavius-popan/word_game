import unittest

from word_game.core import *


class TestGetRandomWord(unittest.TestCase):
    def test_length(self):
        max_length = 3
        self.assertLessEqual(len(get_random_word(max_length)), max_length)


class TestDifficultyRatings(unittest.TestCase):
    def test_0_diff(self):
        pass


class TestIsAnagram(unittest.TestCase):
    def test_correct(self):
        pass

    def test_incorrect(self):
        pass


if __name__ == '__main__':
    unittest.main()
