import unittest

_19 = __import__('19')


class AoCTest(unittest.TestCase):

    data = _19.get_data(
        r'''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''
    )

    def test_part1(self):
        self.assertEqual(33, _19.part1(self.data))

    def test_part2(self):
        self.assertEqual(56*62, _19.part2(self.data))


if __name__ == '__main__':
    unittest.main()
