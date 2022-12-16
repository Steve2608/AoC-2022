import unittest

_04 = __import__('04')


class AoCTest(unittest.TestCase):

    data = _04.get_data(r'''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8''')

    def test_part1(self):
        self.assertEqual(2, _04.part1(self.data))

    def test_part2(self):
        self.assertEqual(4, _04.part2(self.data))


if __name__ == '__main__':
    unittest.main()
