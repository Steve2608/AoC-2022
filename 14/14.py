from typing import TypeAlias

from timing_util import Timing

Coord: TypeAlias = tuple[int, int]


def get_data(content: str) -> list[list[Coord]]:
    return [[tuple(map(int, c.split(','))) for c in line.rstrip().split(' -> ')] for line in content.splitlines()]


def show_grid(grid: list[list[str]]):
    print('\n'.join(''.join(elem for elem in row) for row in grid))


def init_grid(data: list[list[Coord]]) -> tuple[list[list[str]], Coord]:
    min_lr, max_lr = 1000, 0
    min_ud, max_ud = 0, 0
    for line in data:
        for lr, ud in line:
            min_lr = min(min_lr, lr)
            max_lr = max(max_lr, lr)

            max_ud = max(ud, max_ud)

    grid = [['.' for _ in range(min_lr, max_lr + 3)] for _ in range(min_ud, max_ud + 1)]
    off_lr = min_lr - 1

    for line in data:
        y, x = line[0]
        for lr, ud in line[1:]:
            for i in range(min(x, ud), max(x, ud) + 1):
                for j in range(min(y, lr) - off_lr, max(y, lr) - off_lr + 1):
                    grid[i][j] = '#'
            x, y = ud, lr

    spawn_ud, spawn_lr = 0, 500 - off_lr
    return grid, (spawn_ud, spawn_lr)


def part1(data: list[list[Coord]]) -> int:

    def dfs(ud: int, lr: int) -> bool:
        if ud == len(grid) - 1 and grid[ud][lr] != '#':
            return False

        if grid[ud][lr] != '.':
            return True

        if not dfs(ud + 1, lr) or not dfs(ud + 1, lr - 1) or not dfs(ud + 1, lr + 1):
            return False

        grid[ud][lr] = 'O'
        nonlocal n_sand
        n_sand += 1
        return True

    grid, spawn = init_grid(data)
    n_sand = 0
    dfs(*spawn)
    return n_sand


def part2(data: list[list[Coord]]) -> int:

    def dfs(ud: int, lr: int):
        if ud >= len(grid) - 1 or grid[ud][lr] != '.':
            return

        dfs(ud + 1, lr)
        dfs(ud + 1, lr - 1)
        dfs(ud + 1, lr + 1)

        grid[ud][lr] = 'O'
        nonlocal n_sand
        n_sand += 1

    grid, spawn = init_grid(data)
    # one row at the bottom
    grid.append(['.'] * len(grid[0]))

    offset_left = len(grid) - spawn[1]
    left_buf = ['.'] * offset_left
    offset_right = len(grid) - (len(grid[0]) - spawn[1])
    right_buf = ['.'] * offset_right

    for i in range(len(grid)):
        grid[i] = left_buf + grid[i] + right_buf
    spawn = spawn[0], len(grid)

    # bottomless pit now has a bottom
    grid.append(['#'] * len(grid[0]))

    n_sand = 0
    dfs(*spawn)
    return n_sand


if __name__ == '__main__':
    with Timing():
        with open('14/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data)}')
