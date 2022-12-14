from typing import TypeAlias
from timing_util import print_elapsed, timestamp_nano

Coord: TypeAlias = tuple[int, int]


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
    grid[spawn_ud][spawn_lr] = '+'

    return grid, (spawn_ud, spawn_lr)


def part1(data: list[list[Coord]]) -> int:
    grid, spawn = init_grid(data)

    n_sand = 0
    while True:
        s_ud, s_lr = spawn
        while s_ud + 1 < len(grid):
            if grid[s_ud + 1][s_lr] == '.':
                s_ud += 1
            elif grid[s_ud + 1][s_lr - 1] == '.':
                s_ud += 1
                s_lr -= 1
            elif grid[s_ud + 1][s_lr + 1] == '.':
                s_ud += 1
                s_lr += 1
            else:
                break

        # fell off the map
        if s_ud >= len(grid) - 1:
            break
        else:
            grid[s_ud][s_lr] = 'O'
            n_sand += 1

    return n_sand


def part2(data: list[list[Coord]]) -> int:
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
    while True:
        s_ud, s_lr = spawn
        while s_ud + 2 < len(grid):
            if grid[s_ud + 1][s_lr] == '.':
                s_ud += 1
            elif grid[s_ud + 1][s_lr - 1] == '.':
                s_ud += 1
                s_lr -= 1
            elif grid[s_ud + 1][s_lr + 1] == '.':
                s_ud += 1
                s_lr += 1
            else:
                break

        grid[s_ud][s_lr] = 'O'
        n_sand += 1

        # filled up all the way to spawn
        if (s_ud, s_lr) == spawn:
            break

    return n_sand


if __name__ == '__main__':
    start = timestamp_nano()

    with open('14/input.txt') as in_file:
        data = [[tuple(map(int, c.split(','))) for c in line.rstrip().split(' -> ')] for line in in_file]

    print(f'part1: {part1(data)}')
    print(f'part2: {part2(data)}')

    print_elapsed(start)
