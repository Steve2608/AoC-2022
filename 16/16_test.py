import unittest

_16 = __import__('16')


class Day01(unittest.TestCase):

    data = _16.get_data(r'''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II''')

    def test_part1(self):
        self.assertEqual(1651, _16.part1(self.data))

    def test_part2(self):
        self.assertEqual(1707, _16.part2(self.data))


if __name__ == '__main__':
    unittest.main()
