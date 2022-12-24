import unittest

_24 = __import__('24')


class AoCTest(unittest.TestCase):

    data = _24.get_data(r'''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#''')

    def test_part1(self):
        self.assertEqual(18, next(_24.solve(self.data)))

    def test_part2(self):
        it = _24.solve(self.data)
        next(it)
        self.assertEqual(54, next(it))


if __name__ == '__main__':
    unittest.main()
