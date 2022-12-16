import itertools as it
import re
from collections import deque

from timing_util import print_elapsed, timestamp_nano

LEAVES_ONLY: bool = True


def get_data(content: str) -> dict[str, tuple[int, list[str]]]:
    connections = {}
    for line in content.splitlines():
        match = re.search(r'Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)', line)
        connections[match.group(1)] = (int(match.group(2)), match.group(3).split(', '))
    return connections


def iter_paths(adjacent, start, time):

    # DFS because we don't need partial-paths
    def paths(curr, duration):
        is_leaf = True
        for neigh, dur in adjacent[curr].items():
            if duration + dur + 1 <= time and neigh not in visited:
                visited.add(neigh)
                path.append(neigh)

                # opening valve takes one time-step
                yield from paths(neigh, duration + dur + 1)

                path.pop()
                visited.discard(neigh)

                is_leaf = False

        if is_leaf or not LEAVES_ONLY:
            yield path

    path = deque()
    visited = {start}
    yield from paths(start, 0)


def gains(adjacent: dict[str, list[str]], flows: dict[str, int], start: str, time: int) -> dict[tuple[str, ...], int]:
    targets = list(adjacent)
    targets.remove(start)

    paths = {}
    for path in iter_paths(adjacent, start, time):
        time_left = time

        curr = start
        already_open = 0
        gain = 0
        for node in path:
            # opening valve costs 1 time
            duration = adjacent[curr][node] + 1

            time_left -= duration

            # add gain including opening time-step for opening said valve
            gain += already_open * duration

            # open valve
            already_open += flows[node]
            curr = node

        # persistent immutable key
        paths[tuple(path)] = gain + already_open * time_left

    return paths


def adjacency_matrix(data, flows, start):
    nodes = {start: None}

    # BFS for shortest paths
    for node in data:
        visited = set()
        distances = {node: 0}
        fringe = deque([node])

        while fringe:
            curr = fringe.popleft()
            visited.add(curr)

            dist = distances[curr]
            for neigh in data[curr][1]:
                if neigh not in visited:
                    fringe.append(neigh)
                    distances[neigh] = dist + 1

        nodes[node] = {}
        for a, b in distances.items():
            if a in flows and a != node:
                nodes[node][a] = b

    return nodes


def part1(data: dict[str, tuple[int, list[str]]], start: str = 'AA', time: int = 30) -> int:
    flows = {k: v[0] for k, v in data.items() if v[0] > 0}
    flows[start] = 0
    adjacent = adjacency_matrix(data, flows, start)
    gain_for_path = gains(adjacent, flows, start, time)

    return max(gain_for_path.values())


def part2(data: dict[str, tuple[int, list[str]]], start: str = 'AA', time: int = 26) -> int:
    flows = {k: v[0] for k, v in data.items() if v[0] > 0}
    flows[start] = 0
    adjacent = adjacency_matrix(data, flows, start)
    gain_for_path = gains(adjacent, flows, start, time)

    m = 0
    # takes a while
    for (p1, x), (p2, y) in it.combinations(gain_for_path.items(), r=2):
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
