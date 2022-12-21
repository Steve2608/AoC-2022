import unittest

_21 = __import__('21')


class AoCTest(unittest.TestCase):

    data = _21.get_data(r'''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32''')

    def test_part1(self):
        self.assertEqual(152, _21.part1(self.data))

    def test_part2(self):
        self.assertEqual(301, _21.part2(self.data))


if __name__ == '__main__':
    unittest.main()
