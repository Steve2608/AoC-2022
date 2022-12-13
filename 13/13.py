import math
from functools import cmp_to_key
from time import perf_counter_ns as timestamp_nano


def cmp_distress(left, right):
    if isinstance(left, int):
        # both are integers, return integer difference
        if isinstance(right, int):
            return left - right

        # right is list but left isn't
        left = [left]
    else:
        # left is list but right isn't
        right = [right]

    # (now) both are lists
    for l, r in zip(left, right):
        # compare until first disparity
        if (c := cmp_distress(l, r)) != 0:
            return c

    # otherwise return difference in lengths
    return len(left) - len(right)


def part1(data: str):
    pairs = [list(map(eval, batch.split("\n"))) for batch in data.split("\n\n")]
    return sum(i for i, (le, ri) in enumerate(pairs, 1) if cmp_distress(le, ri) < 0)


def part2(data: str, dividers: tuple):
    signals = sorted(
        list(map(eval, filter(bool, data.split('\n')))) + list(dividers),
        key=cmp_to_key(cmp_distress)
    )
    return math.prod(signals.index(d) + 1 for d in dividers)


if __name__ == '__main__':
    start = timestamp_nano()

    with open('13/input.txt') as in_file:
        data = in_file.read()

    print(f'part1: {part1(data)}')
    print(f'part2: {part2(data, dividers=([[6]], [[2]]))}')

    end = timestamp_nano()
    print(f'time: {(end - start) / 1e6:.3f}ms')
