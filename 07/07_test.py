import unittest

_07 = __import__('07')


class Day01(unittest.TestCase):

    data = _07.get_data(r'''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k''')

    def test_part1(self):
        self.assertEqual(95437, _07.part1(self.data))

    def test_part2(self):
        self.assertEqual(24933642, _07.part2(self.data))


if __name__ == '__main__':
    unittest.main()
