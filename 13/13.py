import math
from functools import cmp_to_key

from timing_util import Timing


def cmp_distress(left, right) -> int:
    # both are integers, return integer difference
    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]

    # (now) both are lists
    for l, r in zip(left, right):
        # compare until first disparity
        if (c := cmp_distress(l, r)) != 0:
            return c

    # otherwise return difference in lengths
    return len(left) - len(right)


def part1(data: str) -> int:
    pairs = [list(map(eval, batch.split("\n"))) for batch in data.split("\n\n")]
    return sum(i for i, (le, ri) in enumerate(pairs, 1) if cmp_distress(le, ri) < 0)


def part2(data: str, dividers: tuple) -> int:
    packets = sorted(list(map(eval, filter(bool, data.split('\n')))) + list(dividers), key=cmp_to_key(cmp_distress))
    return math.prod(packets.index(d) + 1 for d in dividers)


if __name__ == '__main__':
    with Timing():
        with open('13/input.txt') as in_file:
            data = in_file.read()

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data, dividers=([[6]], [[2]]))}')
