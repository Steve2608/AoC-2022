import unittest

_03 = __import__('03')


class Day01(unittest.TestCase):

    data = _03.get_data(r'''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw''')

    def test_part1(self):
        self.assertEqual(157, _03.part1(self.data))

    def test_part2(self):
        self.assertEqual(70, _03.part2(self.data))


if __name__ == '__main__':
    unittest.main()
