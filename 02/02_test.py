import unittest

_02 = __import__('02')


class AoCTest(unittest.TestCase):

    data = _02.get_data(r'''A Y
B X
C Z''')

    def test_part1(self):
        self.assertEqual(15, _02.part1(self.data))

    def test_part2(self):
        self.assertEqual(12, _02.part2(self.data))


if __name__ == '__main__':
    unittest.main()
