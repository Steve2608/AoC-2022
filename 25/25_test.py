import unittest

_25 = __import__('25')


class AoCTest(unittest.TestCase):

    data = _25.get_data(r'''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122''')

    def test_part1(self):
        self.assertEqual('2=-1=0', _25.part1(self.data))


if __name__ == '__main__':
    unittest.main()
