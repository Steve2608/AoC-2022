import unittest

_01 = __import__('01')


class Day01(unittest.TestCase):

    data = _01.get_data(r'''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000''')

    def test_part1(self):
        self.assertEqual(24_000, _01.part12(self.data)[0])

    def test_part2(self):
        self.assertEqual(45_000, _01.part12(self.data)[1])


if __name__ == '__main__':
    unittest.main()
