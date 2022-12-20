from timing_util import Timing


def solve(data: str, n_distinct: int, offset: int = 0) -> int:
    for i in range(offset + n_distinct, len(data)):
        if (len(set(data[i - n_distinct:i])) == n_distinct):
            return i
    return -1


if __name__ == '__main__':
    with Timing():
        with open('06/input.txt') as in_file:
            data = in_file.read()

        p1 = solve(data, 4)
        print(f'part1: {p1}')
        print(f'part2: {solve(data, 14, p1 - 4)}')
