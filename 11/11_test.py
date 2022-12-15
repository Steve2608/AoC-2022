from copy import deepcopy
import unittest

_11 = __import__('11')


class Day01(unittest.TestCase):

    data = _11.get_data(r'''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1''')

    def test_part1(self):
        self.assertEqual(10605, _11.part1(deepcopy(self.data), rounds=20, worry_decay=3))

    def test_part2(self):
        self.assertEqual(2713310158, _11.part2(deepcopy(self.data), rounds=10_000))


if __name__ == '__main__':
    unittest.main()
