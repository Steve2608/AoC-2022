import re
from typing import TypeAlias

from timing_util import print_elapsed, timestamp_nano

Coord: TypeAlias = tuple[int, int]


def get_data(content: str) -> list[tuple[Coord, Coord]]:
    data = [
            tuple(
                map(
                    int,
                    re.search(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)',
                              line).groups())) for line in content.splitlines()
        ]
    return [((l[0], l[1]), (l[2], l[3])) for l in data]


def dist(a: Coord, b: Coord) -> int:
    return sum(abs(i - j) for i, j in zip(a, b))


def deltoids(data: list[tuple[Coord, Coord]]) -> list[tuple[int, int, int]]:
    deltoids = []
    for s, b in data:
        d = dist(s, b)
        deltoids.append((s[1] - d, s[1] + d, s[0]))

    return deltoids


def ranges(delts: list[tuple[int, int, int]], target_y: int) -> list[tuple[int, int]]:
    # [start, end] in target_y
    ranges = []
    for (dl, dr, x) in delts:
        if dl <= target_y <= dr:
            span = min(target_y - dl, dr - target_y)
            ranges.append((x - span, x + span))

    return ranges


def part1(data: list[tuple[Coord, Coord]], target_y: int) -> int:

    def simplify_ranges(ranges: list[tuple[int, int]]) -> tuple[int, int]:
        # sorting ranges by start
        r = sorted(ranges)
        a1, a2 = r[0]
        for b1, b2 in r[1:]:
            # ranges are assumed to simplify down to a single one for part1
            if (a1 <= b1 <= a2 <= b2) or (a2 + 1 == b1):
                a2 = b2
            elif not (a1 <= b1 and b2 <= a2):
                raise ValueError('Unreachable state')

        return a1, a2

    sensors = set([s for s, _ in data])
    beacons = set([b for _, b in data])

    # max/min y coordinate for each sensors range
    delts = deltoids(data)
    rngs = ranges(delts, target_y)

    min_, max_ = simplify_ranges(rngs)
    # sum of range
    n = max_ - min_ + 1

    # subtracting 'S's
    for sx, sy in sensors:
        if sy == target_y:
            if min_ <= sx <= max_:
                n -= 1

    # subtracting 'B's
    for bx, by in beacons:
        if by == target_y:
            if min_ <= bx <= max_:
                n -= 1

    return n


def part2(data: list[tuple[Coord, Coord]], min_y: int, max_y: int) -> int:

    def simplify_ranges(ranges: list[tuple[int, int]]) -> int | None:
        # sorting ranges by start
        r = sorted(ranges)
        a1, a2 = r[0]
        for b1, b2 in r[1:]:
            if (a1 <= b1 <= a2 <= b2) or (a2 + 1 == b1):
                a2 = b2
            elif not (a1 <= b1 and b2 <= a2):
                # assuming there's only a single free space, the NEXT x-coordinate has to be it
                # so we take the lower range's max and +1 to it
                return a2 + 1

    # max/min y coordinate for each sensors range
    delts = deltoids(data)

    for target_y in range(min_y, max_y + 1):
        # [start, end] in target_y
        rngs = ranges(delts, target_y)

        if x := simplify_ranges(rngs):
            # tuning freq
            return x * 4000000 + target_y


if __name__ == '__main__':
    start = timestamp_nano()

    with open('15/input.txt') as in_file:
        data = get_data(in_file.read())

    print(f'part1: {part1(data, 2_000_000)}')
    print(f'part2: {part2(data, 0, 4_000_000)}')

    print_elapsed(start)
