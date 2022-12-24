from collections import defaultdict
from queue import PriorityQueue

from timing_util import Timing


def get_data(content: str) -> list[list[str]]:
    return [list(line) for line in content.splitlines()]


def setup_blizzards(data: list[list[str]]) -> dict[tuple[int, int], list[str]]:
    blizzards = defaultdict(list)
    for ud, row in enumerate(data[1:-1], 1):
        for lr, space in enumerate(row[1:-1], 1):
            if space != '.':
                blizzards[(ud, lr)].append(space)

    return blizzards


def move_blizzards(data: list[list[str]], blizzards: dict[tuple[int, int], list[str]]):
    blizzards_new = defaultdict(list)
    max_ud = len(data) - 1
    max_lr = len(data[0]) - 1
    for (ud, lr), spaces in blizzards.items():
        for space in spaces:
            match space:
                case '>':
                    ud_, lr_ = ud, lr + 1
                    if lr_ >= max_lr:
                        lr_ = 1
                case '<':
                    ud_, lr_ = ud, lr - 1
                    if lr_ <= 0:
                        lr_ = max_lr - 1
                case '^':
                    ud_, lr_ = ud - 1, lr
                    if ud_ == 0:
                        ud_ = max_ud - 1
                case 'v':
                    ud_, lr_ = ud + 1, lr
                    if ud_ >= max_ud:
                        ud_ = 1

            blizzards_new[(ud_, lr_)].append(space)

    return blizzards_new


def manhattan_dist(curr: tuple[int, int], other: tuple[int, int]) -> int:
    return abs(other[0] - curr[0]) + abs(other[1] - curr[1])


def solve(data: list[list[str]]) -> int:
    def bfs(src: tuple[int, int], dst: tuple[int, int], time: int = 0) -> tuple[int, dict[tuple[int, int], list[str]]]:
        edges = {src, dst}

        fringe = PriorityQueue()
        fringe.put((manhattan_dist(src, dst) + time, (time, src)))
        visited = set()
        while fringe:
            # discard heuristic
            _, state = fringe.get()

            if state in visited:
                continue
            visited.add(state)

            time, curr = state
            if curr == dst:
                return time

            time += 1
            if time < len(blizzards_at_time):
                blizzards = blizzards_at_time[time]
            else:
                blizzards = move_blizzards(data, blizzards_at_time[-1])
                blizzards_at_time.append(blizzards)

            # do nothing, right, left, up, down
            neighbors = [(curr[0], curr[1]), (curr[0], curr[1] + 1), (curr[0], curr[1] - 1),
                         (curr[0] + 1, curr[1]), (curr[0] - 1, curr[1])]
            for nghbr in neighbors:
                if ((1 <= nghbr[0] <= max_ud and 1 <= nghbr[1] <= max_lr) or nghbr in edges) and nghbr not in blizzards:
                    # as heuristic put in best-case scenario:
                    # in time (spent so far) + distance(neigh, end) we will have made it to the end
                    # guaranteed to be optimal and fewer suboptimal nodes will be expanded
                    fringe.put((time + manhattan_dist(nghbr, dst), (time, nghbr)))

        return -1

    start = (0, 1)
    max_ud = len(data) - 2
    max_lr = len(data[0]) - 2
    end = (max_ud + 1, max_lr)

    # save blizzards at timestamp
    blizzards_at_time = [setup_blizzards(data)]

    # go to end: start -> end (time=373)
    time1 = bfs(start, end, time=0)
    yield time1

    # go back to start to pick up snacks: end -> start (time=373+333)
    time2 = bfs(end, start, time=time1)
    # go back to end: start -> end (time=373+333+291)
    time3 = bfs(start, end, time=time2)

    yield time3


if __name__ == '__main__':
    with Timing():
        with open('24/input.txt') as in_file:
            data = get_data(in_file.read())

        for i, px in enumerate(solve(data), 1):
            print(f'part{i}: {px}')
