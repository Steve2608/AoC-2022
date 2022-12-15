from collections import deque
from typing import TypeAlias

from timing_util import print_elapsed, timestamp_nano

Coord: TypeAlias = tuple[float, float]


def get_data(content: str) -> tuple[list[list[str]], Coord, list[Coord], Coord]:
    grid = [list(line) for line in content.splitlines()]

    s, end = None, None
    strt = []
    for i, row in enumerate(grid):
        for j, letter in enumerate(row):
            match letter:
                case 'E':
                    end = i, j
                case 'S':
                    s = i, j
                case 'a':
                    if not (
                        i > 0 and height(grid, (i - 1, j)) != 1 and
                        i < len(grid) - 1 and height(grid, (i + 1, j)) != 1 and
                        j > 0 and height(grid, (i, j - 1)) and
                        j > len(grid[i]) - 1 and height(grid, (i, j + 1)) != 1
                    ):
                        strt.append((i, j))

    return grid, s, strt, end


def height(grid: list[list[str]], idx: Coord) -> int:
    match grid[idx[0]][idx[1]]:
        case 'S':
            return 0
        case 'E':
            return 26
        case letter:
            return ord(letter) - ord('a')


def bfs(
    grid: list[list[str]],
    visited: set[Coord],
    distances: dict[Coord, int],
    fringe: deque[Coord]
):
    while fringe:
        curr = fringe.popleft()
        if curr in visited:
            continue
        
        visited.add(curr)
        dist = distances[curr] + 1

        max_height = height(grid, curr) + 1
        curr_x, curr_y = curr
        if curr_y > 0:
            left = curr_x, curr_y - 1
            if height(grid, left) <= max_height and left not in visited:
                fringe.append(left)
                distances[left] = dist
        
        if curr_y < len(grid[curr_x]) - 1:
            right = curr_x, curr_y + 1
            if height(grid, right) <= max_height and right not in visited:
                fringe.append(right)
                distances[right] = dist
        
        if curr_x > 0:
            up = curr_x - 1, curr_y
            if height(grid, up) <= max_height and up not in visited:
                fringe.append(up)
                distances[up] = dist
        
        if curr_x < len(grid) - 1:
            down = curr_x + 1, curr_y
            if height(grid, down) <= max_height and down not in visited:
                fringe.append(down)
                distances[down] = dist


def part1(grid: list[list[str]], start: Coord, end: Coord) -> int | None:
    visited = set()
    distances = {start: 0}
    fringe = deque([start])

    bfs(grid, visited, distances, fringe)

    return distances.get(end, None)


def part2(grid: list[list[str]], strt: list[Coord], end: Coord, best) -> int:
    return min(best, min(filter(bool, (part1(grid, start, end) for start in strt))))


if __name__ == '__main__':
    start = timestamp_nano()

    with open('12/input.txt') as in_file:
        grid, s, strt, end = get_data(in_file.read())

    p1 = part1(grid, s, end)
    print(f'part1: {p1}')
    print(f'part2: {part2(grid, strt, end, p1)}')

    print_elapsed(start)
