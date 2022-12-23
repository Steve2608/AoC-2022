import itertools as it
from collections import defaultdict, deque
from copy import deepcopy

from timing_util import Timing


def print_grid(grid: list[list[str]]):
    print('\n'.join(''.join(line) for line in grid), end='\n\n')


def get_data(content: str) -> list[list[str]]:
    return [list(line) for line in content.splitlines()]


def expand_grid(data: list[list[str]]) -> list[list[str]]:
    for row in data:
        row.insert(0, '.')
        row.append('.')
    data.insert(0, ['.'] * len(data[0]))
    data.append(['.'] * len(data[0]))


def bounding_box(data: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
    min_ud, max_ud = len(data), 0
    min_lr, max_lr = len(data[0]), 0
    for ud, row in enumerate(data):
        for lr, space in enumerate(row):
            if space == '#':
                if ud < min_ud:
                    min_ud = ud
                if ud > max_ud:
                    max_ud = ud

                if lr < min_lr:
                    min_lr = lr
                if lr > max_lr:
                    max_lr = lr

    return (min_ud, max_ud + 1), (min_lr, max_lr + 1)


def contract_grid(data: list[list[str]]):
    (min_ud, max_ud), (min_lr, max_lr) = bounding_box(data)

    grid = [['.'] * (max_lr - min_lr) for _ in range(max_ud - min_ud)]
    for ud, row in enumerate(data):
        for lr, space in enumerate(row):
            if space == '#':
                grid[ud - min_ud][lr - min_lr] = '#'

    return grid


def empty_grid_like(grid: list[list[str]]) -> list[list[str]]:
    return [['.'] * len(grid[0]) for _ in grid]


def score(data: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
    (min_ud, max_ud), (min_lr, max_lr) = bounding_box(data)
    
    s = 0
    for row in data[min_ud:max_ud]:
        for space in row[min_lr:max_lr]:
            if space == '.':
                s += 1
    return s


def part12(data: list[list[str]], n_rounds: int) -> int:
    grid = deepcopy(data)
    proposals = deque(['north', 'south', 'west', 'east'])
    neighbors = [(x, y) for x, y in it.product([-1, 0, 1], [-1, 0, 1]) if x or y]
    i = 0
    while n_rounds is None or i < n_rounds:
        expand_grid(grid)

        movements = []
        for ud, row in enumerate(grid):
            for lr, space in enumerate(row):
                if space == '.':
                    continue

                # all neighbouring fields are clear already, elf stays where it is
                if all(grid[ud + x][lr + y] == '.' for x, y in neighbors):
                    movements.append(((ud, lr), (ud, lr)))
                    continue

                for prop in proposals:
                    match prop:
                        case 'north':
                            row = grid[ud - 1]
                            if row[lr - 1] == '.' and row[lr] == '.' and row[lr + 1] == '.':
                                movements.append(((ud, lr), (ud - 1, lr)))
                                break
                        case 'south':
                            row = grid[ud + 1]
                            if row[lr - 1] == '.' and row[lr] == '.' and row[lr + 1] == '.':
                                movements.append(((ud, lr), (ud + 1, lr)))
                                break
                        case 'west':
                            if grid[ud - 1][lr - 1] == '.' and grid[ud][lr - 1] == '.' and grid[ud + 1][lr - 1] == '.':
                                movements.append(((ud, lr), (ud, lr - 1)))
                                break
                        case 'east':
                            if grid[ud - 1][lr + 1] == '.' and grid[ud][lr + 1] == '.' and grid[ud + 1][lr + 1] == '.':
                                movements.append(((ud, lr), (ud, lr + 1)))
                                break
                else:
                    # could not find a proposal, elf stays where it is
                    movements.append(((ud, lr), (ud, lr)))   

        i += 1
        if all(src == dst for src, dst in movements):
            return i

        next_step = empty_grid_like(grid)
        destinations = defaultdict(int)
        for (_, dst) in movements:
            destinations[dst] += 1

        for (src, dst) in movements:
            if destinations[dst] == 1:
                ud, lr = dst
            else:
                # stay where it was
                ud, lr = src

            next_step[ud][lr] = '#'

        grid = contract_grid(next_step)
        proposals.rotate(-1)

    return score(grid)


if __name__ == '__main__':
    with Timing():
        with open('23/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part12(data, n_rounds=10)}')
        print(f'part2: {part12(data, n_rounds=None)}')
