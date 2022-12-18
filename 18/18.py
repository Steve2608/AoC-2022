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
        if x1 == x2 and y1 == y2 and abs(z1 - z2) == 1 or x1 == x2 and abs(y1 - y2) == 1 and z1 == z2 or abs(
                x1 - x2) == 1 and y1 == y2 and z1 == z2:
            surface -= 2

    return surface


def part2(data: list[Coord]) -> int:

    def bfs(start: Coord) -> set[Coord]:
        # before we do anything, we check if 'start' is part of an internal structure already
        if start in air:
            return

        fringe = deque([start])
        visited = set()
        while fringe:
            curr = fringe.popleft()
            if curr in visited or curr in air:
                continue

            visited.add(curr)
            cx, cy, cz = curr
            for x, y, z in [(0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0)]:
                # if one neighbour reaches the padded fringe -> we're not part of an internal structure
                if not (0 < cx + x < n) or not (0 < cy + y < n) or not (0 < cz + z < n):
                    return

                if grid[cx + x][cy + y][cz + z] == '.':
                    fringe.append((cx + x, cy + y, cz + z))

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
        if grid[x][y][z] == '.':
            bfs((x, y, z))

    return part1(data) - part1(air)


if __name__ == '__main__':
    start = timestamp_nano()

    with open('18/input.txt') as in_file:
        data = get_data(in_file.read())

    print(f'part1: {part1(data)}')
    print(f'part2: {part2(data)}')

    print_elapsed(start)
