import unittest

_14 = __import__('14')


class Day01(unittest.TestCase):

    data = _14.get_data(r'''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9''')

    def test_part1(self):
        self.assertEqual(24, _14.part1(self.data))

    def test_part2(self):
        self.assertEqual(93, _14.part2(self.data))


if __name__ == '__main__':
    unittest.main()
