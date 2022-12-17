import itertools as it
from copy import deepcopy

from timing_util import print_elapsed, timestamp_nano

MAX_ROCK_HEIGHT = 4
ROCKS = [['....', '....', '....', '####'], ['....', '.#..', '###.', '.#..'], ['....', '..#.', '..#.', '###.'],
         ['#...', '#...', '#...', '#...'], ['....', '....', '##..', '##..']]
WIDTH = 7


def print_chambers(chambers: list[list[str]]):
    print('\n'.join(''.join(line) for line in chambers), end='\n\n')


def segment(rock: str | None = None) -> list[list[str]]:
    seg = [list('.' * WIDTH) for _ in range(4)]
    if rock:
        for i, layer in enumerate(rock[::-1]):
            for j, r in enumerate(layer, 2):
                seg[len(seg) - 1 - i][j] = r
    return seg


def has_collision(field: list[list[str]], rock: list[list[str]]) -> bool:
    for f, r in zip(field, rock):
        if any(f_i == r_i == '#' for f_i, r_i in zip(f, r)):
            return True
    return False


def set_rock(field: list[list[str]], rock: list[list[str]]):
    # 'logical or' with rocks
    for f, r in zip(field, rock):
        for i, r_i in enumerate(r):
            if r_i == '#':
                f[i] = r_i


def can_shift_left(field: list[list[str]], rock: list[list[str]]) -> bool:
    # collision against left wall
    if not all(l[0] == '.' for l in rock):
        return False

    for f, r in zip(field, rock):
        for i, r_i in enumerate(r[1:], 1):
            if r_i == '#' and f[i - 1] == '#':
                return False
    return True


def can_shift_right(field: list[list[str]], rock: list[list[str]]) -> bool:
    # collision against right wall
    if not all(l[-1] == '.' for l in rock):
        return False

    for f, r in zip(field, rock):
        for i, r_i in enumerate(r[:-1]):
            if r_i == '#' and f[i + 1] == '#':
                return False
    return True


def solve(data: str, n_steps: int) -> int:

    def step_rock():
        i_rock, rock = next(rocks)
        seg = segment(rock)

        # executes at least MAX_ROCK_HEIGHT + 1 times
        for depth in it.count():
            grid = chamber[depth:depth + MAX_ROCK_HEIGHT]
            prev = deepcopy(seg)

            if has_collision(grid, seg):
                depth -= 1
                set_rock(chamber[depth:depth + MAX_ROCK_HEIGHT], prev)
                return i_rock, i_direction

            i_direction, direction = next(directions)
            if direction == '>':
                if can_shift_right(grid, seg):
                    for l in seg:
                        l.insert(0, l.pop())
            else:
                if can_shift_left(grid, seg):
                    for l in seg:
                        l.append(l.pop(0))

    def step_chamber():
        nonlocal chamber, height
        for d in range(buf_len):
            if any(c == '#' for c in chamber[d]):
                # restore buffer on top
                for depth in range(buf_len - d):
                    chamber.insert(0, list('.' * WIDTH))

                for col in range(WIDTH):
                    col_heights[col] += buf_len - d
                    for depth in range(buf_len - d, col_heights[col]):
                        if chamber[depth][col] == '#':
                            col_heights[col] = depth
                            break

                height += buf_len - d

                # keep only the necessary bit in memory
                chamber = chamber[:max(col_heights) + 1]
                return

    # infinite iterators
    directions = ((i % len(data), d) for i, d in enumerate(it.cycle(data)))
    rocks = ((i % len(ROCKS), r) for i, r in enumerate(it.cycle(ROCKS)))

    # setup
    chamber = segment() + [list('.' * WIDTH), list('.' * WIDTH), list('.') * WIDTH, list('#' * WIDTH)]
    buf_len = len(chamber) - 1

    col_heights = [len(chamber)] * WIDTH
    height = 0
    step = 0
    # checking for periods
    states = {}
    while step < n_steps:
        i_rock, i_direction = step_rock()
        step_chamber()

        # part2
        if states is not None:
            state = i_rock, i_direction, tuple(col_heights)
            if state in states:
                last_step, last_height = states[state]
                n_periods = ((n_steps - step) - 1) // (step - last_step)

                height += (height - last_height) * n_periods
                step += (step - last_step) * n_periods

                # invalidate states
                states = None
            else:
                states[state] = step, height

        step += 1

    return height


if __name__ == '__main__':
    start = timestamp_nano()

    with open('17/input.txt') as in_file:
        data = in_file.read()

    print(f'part1: {solve(data, n_steps=2022)}')
    print(f'part2: {solve(data, n_steps=1_000_000_000_000)}')

    print_elapsed(start)
