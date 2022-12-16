import unittest

_09 = __import__('09')


class AoCTest(unittest.TestCase):

    data1 = _09.get_data(r'''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2''')
    data2 = _09.get_data(r'''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20''')

    def test_part1(self):
        self.assertEqual(13, _09.part12(self.data1)[0])

    def test_part2(self):
        self.assertEqual(36, _09.part12(self.data2)[1])


if __name__ == '__main__':
    unittest.main()
