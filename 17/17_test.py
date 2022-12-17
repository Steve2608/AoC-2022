import unittest

_17 = __import__('17')


class AoCTest(unittest.TestCase):

    data = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

    def test_part1(self):
        self.assertEqual(3068, _17.solve(self.data, n_steps=2022))

    def test_part2(self):
        self.assertEqual(1514285714288, _17.solve(self.data, n_steps=1_000_000_000_000))


if __name__ == '__main__':
    unittest.main()
