import unittest

_23 = __import__('23')


class AoCTest(unittest.TestCase):

    data1 = _23.get_data(r'''.....
..##.
..#..
.....
..##.
.....''')

    data2 = _23.get_data(r'''....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..''')

    def test_part1(self):
        self.assertEqual(25, _23.part12(self.data1, n_rounds=3))
        self.assertEqual(110, _23.part12(self.data2, n_rounds=10))

    def test_part2(self):
        self.assertEqual(20, _23.part12(self.data2, n_rounds=None))


if __name__ == '__main__':
    unittest.main()
