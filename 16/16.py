import itertools as it
import re
from collections import deque

from timing_util import print_elapsed, timestamp_nano

MAXIMUM_PATHS_ONLY: bool = True


def get_data(content: str) -> dict[str, tuple[int, list[str]]]:
    connections = {}
    for line in content.splitlines():
        match = re.search(r'Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)', line)
        connections[match.group(1)] = (int(match.group(2)), match.group(3).split(', '))
    return connections


def dfs(adjacent, start, time):

    def dfs_rec(curr, duration):
        modified = False
        for adj, dur in adjacent[curr].items():
            if duration + dur + 1 <= time and adj not in visited:
                modified = True
                visited.add(adj)
                stack.append(adj)

                yield from dfs_rec(adj, duration + dur + 1)

                stack.pop()
                visited.discard(adj)

        if not modified or not MAXIMUM_PATHS_ONLY:
            yield stack

    stack = deque()
    visited = {start}
    curr = start
    yield from dfs_rec(curr, 0)


def search(adjacent: dict[str, list[str]], flows: dict[str, int], start: str, time: int) -> dict[tuple[str, ...], int]:
    targets = list(adjacent)
    targets.remove(start)

    paths = {}
    for p in dfs(adjacent, start, time):
        time_left = time

        curr = start
        passive = 0
        gain = 0
        for adj in p:
            duration = adjacent[curr][adj]

            # opening valve costs 1 time
            time_left -= (duration + 1)

            # add gain including opening time-step for opening said valve
            gain += passive * (duration + 1)

            # open valve
            passive += flows[adj]
            curr = adj

        paths[tuple(p)] = gain + passive * time_left

    return paths


def shortest_path(data, flows, start):
    waypoints = {start: None}

    for k in data:
        visited = set()
        distances = {k: 0}
        fringe = deque([k])

        while fringe:
            curr = fringe.popleft()
            visited.add(curr)

            dist = distances[curr]
            for adj in data[curr][1]:
                if adj not in visited:
                    fringe.append(adj)
                    distances[adj] = dist + 1

        waypoints[k] = {}
        for a, b in distances.items():
            if a in flows and a != k:
                waypoints[k][a] = b

    return waypoints


def part1(data: dict[str, tuple[int, list[str]]], start: str = 'AA', time: int = 30) -> int:
    flows = {k: v[0] for k, v in data.items() if v[0] > 0}
    flows[start] = 0
    adjacent = shortest_path(data, flows, start)
    paths = search(adjacent, flows, start, time)

    return max(paths.values())


def part2(data: dict[str, tuple[int, list[str]]], start: str = 'AA', time: int = 26) -> int:
    flows = {k: v[0] for k, v in data.items() if v[0] > 0}
    flows[start] = 0
    adjacent = shortest_path(data, flows, start)
    paths = search(adjacent, flows, start, time)

    m = 0
    # takes a while
    for (p1, x), (p2, y) in it.combinations(paths.items(), r=2):
        if x + y >= m and all(p not in p1 for p in p2):
            m = x + y

    return m


if __name__ == '__main__':
    start = timestamp_nano()

    with open('16/input.txt') as in_file:
        data = get_data(in_file.read())

    print(f'part1: {part1(data)}')
    print(f'part2: {part2(data)}')

    print_elapsed(start)
