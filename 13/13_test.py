import unittest

_13 = __import__('13')


class AoCTest(unittest.TestCase):

    data = r'''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''

    def test_part1(self):
        self.assertEqual(13, _13.part1(self.data))

    def test_part2(self):
        self.assertEqual(140, _13.part2(self.data, dividers=([[2]], [[6]])))


if __name__ == '__main__':
    unittest.main()
