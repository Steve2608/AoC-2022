import re

from timing_util import Timing


def print_grid(grid: list[list[str]]):
    print('\n'.join(''.join(line) for line in grid), end='\n\n')


def get_data(content: str) -> tuple[list[list[str]], tuple[int, str], int]:
    grid, walks = content.split('\n\n')
    
    # parsing last number
    for i in range(1, len(walks)):
        try:
            last = int(walks[-i:])
        except ValueError:
            break

    grid = list(list(line) for line in grid.splitlines())
    row_len = max(len(row) for row in grid)
    for row in grid:
        if len(row) != row_len:
            row.extend(list(' ' * (row_len - len(row))))

    walks = [(int(amount), direction) for amount, direction in re.findall(r'(\d+)([RL])', walks)]
    
    return grid, walks, last


def score(curr: tuple[int, int], facing: int, directions: str) -> int:
    ud, lr = curr
    return 1000 * (ud + 1) + 4 * (lr + 1) + facing


def turn(facing: int, rotation: str, directions: str) -> int:
    if rotation == 'L':
        return (facing - 1) % len(directions)
    else:
        return (facing + 1) % len(directions)


def find_start(grid):
    return 0, grid[0].index('.')

def part1(data: tuple[list[list[str]], tuple[int, str], int]) -> int:
    def walk(curr: tuple[int, int]) -> tuple[int, int]:
        ud, lr = curr
        match directions[facing]:
            case 'L':
                for _ in range(amount):
                    lr_ = lr
                    while grid[ud][(lr_ - 1) % LR] == ' ':
                        lr_ = (lr_ - 1) % LR
                    if grid[ud][(lr_ - 1) % LR] == '#':
                        break
                    lr = (lr_ - 1) % LR
            case 'R':
                for _ in range(amount):
                    lr_ = lr
                    while grid[ud][(lr_ + 1) % LR] == ' ':
                        lr_ = (lr_ + 1) % LR
                    if grid[ud][(lr_ + 1) % LR] == '#':
                        break
                    lr = (lr_ + 1) % LR
            case 'U':
                for _ in range(amount):
                    _ud = ud
                    while grid[(_ud - 1) % UD][lr] == ' ':
                        _ud = (_ud - 1) % UD
                    if grid[(_ud - 1) % UD][lr] == '#':
                        break
                    ud = (_ud - 1) % UD
            case 'D':
                for _ in range(amount):
                    _ud = ud
                    while grid[(_ud + 1) % UD][lr] == ' ':
                        _ud = (_ud + 1) % UD
                    if grid[(_ud + 1) % UD][lr] == '#':
                        break
                    ud = (_ud + 1) % UD
        
        return ud, lr

    grid, walks, last = data
    UD = len(grid)
    LR = len(grid[0])

    curr = find_start(grid)
    directions = 'RDLU'
    facing = 0
    for amount, rotation in walks:
        curr = walk(curr)
        facing = turn(facing, rotation, directions)

    amount = last
    curr = walk(curr)
    return score(curr, facing, directions)

# cube layout is
# .12
# .3.
# 45.
# 6..
faces = dict(enumerate([(0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (3, 0)], 1))
# from (face, facing) -> (face, facing)
connections = {
    (1, 0): (2, 0), (1, 1): (3, 1), (1, 2): (4, 0), (1, 3): (6, 0),
    (2, 0): (5, 2), (2, 1): (3, 2), (2, 2): (1, 2), (2, 3): (6, 3),
    (3, 0): (2, 3), (3, 1): (5, 1), (3, 2): (4, 1), (3, 3): (1, 3),
    (4, 0): (5, 0), (4, 1): (6, 1), (4, 2): (1, 0), (4, 3): (3, 0),
    (5, 0): (2, 2), (5, 1): (6, 2), (5, 2): (4, 2), (5, 3): (3, 3),
    (6, 0): (5, 3), (6, 1): (2, 1), (6, 2): (1, 1), (6, 3): (4, 3)
}
LEN = 50


def part2(data: tuple[list[list[str]], tuple[int, str], int]) -> int:
    def get_cube_face(ud, lr):
        for i, (x, y) in faces.items():
            if x*LEN <= ud < (x+1) * LEN and y*LEN <= lr < (y + 1) * LEN:
                return i, (ud - x * LEN, lr - y * LEN)

    def get_global_coord(ud, lr, face):
        x, y = faces[face]
        return x * LEN + ud, y * LEN + lr

    def new_coordinates(ud, lr, facing, facing_new):
        match directions[facing]:
            case 'R':
                other = ud
            case 'D':
                other = LEN - 1 - lr
            case 'L':
                other = LEN - 1 - ud
            case 'U':
                other = lr

        match directions[facing_new]:
            case 'R':
                return (other, 0)
            case 'D':
                return (0, LEN - 1 - other)
            case 'L':
                return (LEN - 1 - other, LEN - 1)
            case 'U':
                return (LEN - 1, other)

    def walk(curr: tuple[int, int]) -> tuple[int, int]:
        def wrap_cube():
            # which face are we on
            face_id, (face_ud, face_lr) = get_cube_face(ud, lr)
            
            # get new face
            new_face, new_facing = connections[(face_id, facing)]
            
            # get new local coordinates
            new_ud, new_lr = new_coordinates(face_ud, face_lr, facing, new_facing)
            
            # map to global coordinates
            return new_facing, get_global_coord(new_ud, new_lr, new_face)

        nonlocal facing
        # global ud/lr
        ud, lr = curr

        for _ in range(amount):
            match directions[facing]:
                case 'L':
                    if grid[ud][(lr - 1) % LR] == ' ' or lr == 0:
                        new_facing, (ud_, lr_) = wrap_cube()
                        
                        # if we hit a wall, just stay where we are
                        if grid[ud_][lr_] == '#':
                            break

                        ud, lr, facing = ud_, lr_, new_facing
                    elif grid[ud][(lr - 1) % LR] == '#':
                        break
                    else:
                        lr = (lr - 1) % LR
                case 'R':
                    if grid[ud][(lr + 1) % LR] == ' ' or lr == LR - 1:
                        new_facing, (ud_, lr_) = wrap_cube()
                        
                        # if we hit a wall, just stay where we are
                        if grid[ud_][lr_] == '#':
                            break

                        ud, lr, facing = ud_, lr_, new_facing
                    elif grid[ud][(lr + 1) % LR] == '#':
                        break
                    else:
                        lr = (lr + 1) % LR
                case 'U':
                    if grid[(ud - 1) % UD][lr] == ' ' or ud == 0:
                        new_facing, (ud_, lr_) = wrap_cube()
                        
                        # if we hit a wall, just stay where we are
                        if grid[ud_][lr_] == '#':
                            break

                        ud, lr, facing = ud_, lr_, new_facing
                    elif grid[(ud - 1) % UD][lr] == '#':
                        break
                    else:
                        ud = (ud - 1) % UD
                case 'D':
                    if grid[(ud + 1) % UD][lr] == ' ' or ud == UD - 1:
                        new_facing, (ud_, lr_) = wrap_cube()
                        
                        # if we hit a wall, just stay where we are
                        if grid[ud_][lr_] == '#':
                            break

                        ud, lr, facing = ud_, lr_, new_facing
                    elif grid[(ud + 1) % UD][lr] == '#':
                        break
                    else:
                        ud = (ud + 1) % UD
        return ud, lr

    grid, walks, last = data
    UD = len(grid)
    LR = len(grid[0])

    curr = find_start(grid)
    directions = 'RDLU'
    facing = 0

    for amount, rotation in walks:
        curr = walk(curr)
        facing = turn(facing, rotation, directions)

    amount = last
    curr = walk(curr)
    return score(curr, facing, directions)


if __name__ == '__main__':
    with Timing():
        with open('22/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data)}')
