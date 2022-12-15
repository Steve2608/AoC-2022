import unittest

_12 = __import__('12')


class Day01(unittest.TestCase):

    data = _12.get_data(r'''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi''')

    def test_part1(self):
        self.assertEqual(31, _12.part1(self.data[0], self.data[1], self.data[3]))

    def test_part2(self):
        p1 = _12.part1(self.data[0], self.data[1], self.data[3])
        self.assertEqual(29, _12.part2(self.data[0], self.data[2], self.data[3], p1))


if __name__ == '__main__':
    unittest.main()
