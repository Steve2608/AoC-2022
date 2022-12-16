import unittest

_06 = __import__('06')


class AoCTest(unittest.TestCase):

    data1 = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
    data2 = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
    data3 = 'nppdvjthqldpwncqszvftbrmjlhg'
    data4 = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
    data5 = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'

    def test_part1(self):
        self.assertEqual(7, _06.solve(self.data1, n_distinct=4))
        self.assertEqual(5, _06.solve(self.data2, n_distinct=4))
        self.assertEqual(6, _06.solve(self.data3, n_distinct=4))
        self.assertEqual(10, _06.solve(self.data4, n_distinct=4))
        self.assertEqual(11, _06.solve(self.data5, n_distinct=4))

    def test_part2(self):
        self.assertEqual(19, _06.solve(self.data1, n_distinct=14))
        self.assertEqual(23, _06.solve(self.data2, n_distinct=14))
        self.assertEqual(23, _06.solve(self.data3, n_distinct=14))
        self.assertEqual(29, _06.solve(self.data4, n_distinct=14))
        self.assertEqual(26, _06.solve(self.data5, n_distinct=14))


if __name__ == '__main__':
    unittest.main()
