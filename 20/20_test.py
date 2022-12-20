import unittest

_20 = __import__('20')


class AoCTest(unittest.TestCase):

    data = _20.get_data(r'''1
2
-3
3
-2
0
4''')

    def test_part1(self):
        self.assertEqual(3, _20.solve(self.data))

    def test_part2(self):
        self.assertEqual(1623178306, _20.solve(self.data, encryption_key=811589153, n_mixing=10))


if __name__ == '__main__':
    unittest.main()
