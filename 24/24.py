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
    for (ud, lr), spaces in blizzards.items():
        for space in spaces:
            match space:
                case '>':
                    ud_, lr_ = ud, lr + 1
                    if lr_ == len(data[0]) - 1:
                        lr_ = 1
                case '<':
                    ud_, lr_ = ud, lr - 1
                    if lr_ == 0:
                        lr_ = len(data[0]) - 2
                case '^':
                    ud_, lr_ = ud - 1, lr
                    if ud_ == 0:
                        ud_ = len(data) - 2
                case 'v':
                    ud_, lr_ = ud + 1, lr
                    if ud_ == len(data) - 1:
                        ud_ = 1

            blizzards_new[(ud_, lr_)].append(space)

    return blizzards_new


def distance(curr: tuple[int, int], other: tuple[int, int]) -> int:
    return abs(other[0] - curr[0]) + abs(other[1] - curr[1])


def quickest_path(data: list[list[str]], src: tuple[int, int], dst: tuple[int, int], blizzards: dict[tuple[int, int], list[str]]) -> tuple[int, dict[tuple[int, int], list[str]]]:
    fringe = PriorityQueue()
    fringe.put((distance(src, dst), 0, src, blizzards))
    visited = set()
    while fringe:
        _, time, curr, blizzards = fringe.get()

        if (curr, time) in visited:
            continue
        visited.add((curr, time))

        if curr == dst:
            return time, blizzards

        blizzards_next = move_blizzards(data, blizzards)
        neighbors = [(curr[0], curr[1]), (curr[0], curr[1] + 1), (curr[0], curr[1] - 1),
                     (curr[0] + 1, curr[1]), (curr[0] - 1, curr[1])]
        time += 1
        for neigh in filter(lambda neigh: neigh not in blizzards_next, neighbors):
            ud, lr = neigh
            # never just camp in start
            if (1 <= ud <= len(data) - 2 and 1 <= lr <= len(data[0]) - 2) or neigh in {src, dst}:
                # as heuristic put in best-case scenario:
                # in time (spent so far) + distance(neigh, end) we will have made it to the end
                # guaranteed to be optimal but fewer suboptimal nodes will be expanded
                fringe.put((time + distance(neigh, dst), time, neigh, blizzards_next))

    return -1, None


def solve(data: list[list[str]]) -> int:
    start = (0, 1)
    end = (len(data) - 1, len(data[0]) - 2)
    blizzards = setup_blizzards(data)

    # go to end: start -> end (time=373)
    time1, blizzards = quickest_path(data, start, end, blizzards)
    yield time1

    # go back to start to pick up snacks: end -> start (time=333)
    time2, blizzards = quickest_path(data, end, start, blizzards)
    # go back to end: start -> end (time=291)
    time3, blizzards = quickest_path(data, start, end, blizzards)

    yield time1 + time2 + time3


if __name__ == '__main__':
    with Timing():
        with open('24/input.txt') as in_file:
            data = get_data(in_file.read())

        for i, px in enumerate(solve(data), 1):
            print(f'part{i}: {px}')
