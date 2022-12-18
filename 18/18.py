import itertools as it
from collections import deque
from typing import TypeAlias

from timing_util import print_elapsed, timestamp_nano

Coord: TypeAlias = tuple[int, int, int]


def get_data(content: str) -> list[Coord]:
    return [tuple(map(int, line.split(','))) for line in content.splitlines()]


def part1(data: list[Coord]) -> int:
    surface = len(data) * 6

    for (x1, y1, z1), (x2, y2, z2) in it.combinations(data, r=2):
        if x1 == x2:
            if y1 == y2:
                if abs(z1 - z2) == 1:
                    surface -= 2
            elif z1 == z2:
                if abs(y1 - y2) == 1:
                    surface -= 2
        elif y1 == y2:
            if z1 == z2 and abs(x1 - x2) == 1:
                surface -= 2

    return surface


def part2(data: list[Coord]) -> int:

    def bfs(start: Coord) -> set[Coord]:
        fringe = deque([start])
        visited = set()
        while fringe:
            curr = fringe.popleft()
            if curr in visited:
                continue

            visited.add(curr)
            cx, cy, cz = curr
            for x, y, z in [(cx, cy, cz - 1), (cx, cy, cz + 1), (cx, cy - 1, cz), (cx, cy + 1, cz), (cx - 1, cy, cz),
                            (cx + 1, cy, cz)]:
                # if one neighbour reaches the padded fringe -> we're not part of an internal structure
                if not (0 < x < n) or not (0 < y < n) or not (0 < z < n):
                    return

                if grid[x][y][z] == '.':
                    fringe.append((x, y, z))

        air.update(visited)

    # padding in every direction
    max_ = max(max(d) for d in data) + 1
    min_ = min(min(d) for d in data) - 1
    n = max_ - min_

    # create grid
    grid = list(list(list('.' for _ in range(n)) for _ in range(n)) for _ in range(n))
    for x, y, z in data:
        grid[x - min_][y - min_][z - min_] = '#'

    # search air-pockets
    air = set()
    for x, y, z in it.product(*([range(1, n)] * 3)):
        if grid[x][y][z] == '.' and (x, y, z) not in air:
            bfs((x, y, z))

    return part1(data) - part1(air)


if __name__ == '__main__':
    start = timestamp_nano()

    with open('18/input.txt') as in_file:
        data = get_data(in_file.read())

    print(f'part1: {part1(data)}')
    print(f'part2: {part2(data)}')

    print_elapsed(start)
