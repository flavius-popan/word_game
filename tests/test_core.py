import unittest

from word_game.core import *


class TestDictLoader(unittest.TestCase):
    def test_wc(self):
        self.assertEqual(len(WORD_LIST), 58709)


class TestGetRandomWord(unittest.TestCase):
    def test_max_length(self):
        self.assertLessEqual(len(get_random_word()), 8)


class TestDifficultyRatings(unittest.TestCase):
    def test_0_diff(self):
        pass


class TestIsAnagram(unittest.TestCase):
    def test_correct(self):
        self.assertTrue(is_anagram('dog', 'god'))

    def test_incorrect(self):
        self.assertFalse(is_anagram('boy', 'toy'))


if __name__ == '__main__':
    unittest.main()
