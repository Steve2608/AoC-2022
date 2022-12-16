import unittest

_05 = __import__('05')


class AoCTest(unittest.TestCase):

    data = _05.get_data(r'''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2''',
                        n_stacks=3)

    def test_part1(self):
        self.assertEqual('CMZ', _05.part1(*self.data))

    def test_part2(self):
        self.assertEqual('MCD', _05.part2(*self.data))


if __name__ == '__main__':
    unittest.main()
