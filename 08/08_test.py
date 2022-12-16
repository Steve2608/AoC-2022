import unittest

_08 = __import__('08')


class AoCTest(unittest.TestCase):

    data = _08.get_data(r'''30373
25512
65332
33549
35390''')

    def test_part1(self):
        self.assertEqual(21, _08.part1(self.data))

    def test_part2(self):
        self.assertEqual(8, _08.part2(self.data))


if __name__ == '__main__':
    unittest.main()
