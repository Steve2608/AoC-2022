import unittest

_18 = __import__('18')


class AoCTest(unittest.TestCase):

    data = _18.get_data(r'''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5''')

    def test_part1(self):
        self.assertEqual(64, _18.part1(self.data))

    def test_part2(self):
        self.assertEqual(58, _18.part2(self.data))


if __name__ == '__main__':
    unittest.main()
