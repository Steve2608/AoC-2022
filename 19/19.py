import math
import multiprocessing as mp
import re
from collections import deque
from functools import partial
from typing import TypeAlias

from timing_util import Timing

Costs: TypeAlias = tuple[int, int, int, int, int, int]
Blueprint: TypeAlias = tuple[int, Costs]


def get_data(content: str) -> list[Blueprint]:
    data = []
    for line in content.splitlines():
        m = re.search(
            r'Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.',
            line)
        r = map(int, m.groups())
        _id, ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = r
        data.append((_id, (ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian)))
    return data


def solve(costs: Costs, time: int) -> int:
    cost_o, cost_c, cost_ob_o, cost_ob_c, cost_g_o, cost_g_ob = costs
    max_cost_ore = max([cost_o, cost_c, cost_ob_o, cost_g_o])

    fringe = deque([((0, 0, 0, 0), (1, 0, 0, 0), time)])
    visited = set()
    best_geodes = 0
    while fringe:
        (o, c, ob, g), (bot_o, bot_c, bot_ob, bot_g), time = fringe.popleft()
        # reduce search-depth by one
        # no matter what action is taken by at time==1 it does not change the number of geodes in time==0
        if time == 1:
            best_geodes = max(g + bot_g, best_geodes)
            continue

        # throw away surplus resources that cannot be spent in time
        if o > (spendable_o := time * max_cost_ore - bot_o * (time - 1)):
            o = spendable_o
        if c > (spendable_c := time * cost_ob_c - bot_c * (time - 1)):
            c = spendable_c
        if ob > (spendable_ob := time * cost_g_ob - bot_ob * (time - 1)):
            ob = spendable_ob

        if (state := ((o, c, ob, g), (bot_o, bot_c, bot_ob, bot_g))) in visited:
            continue
        visited.add(state)

        time -= 1
        # do nothing
        fringe.append(((o + bot_o, c + bot_c, ob + bot_ob, g + bot_g), (bot_o, bot_c, bot_ob, bot_g), time))

        # buy ore, clay, obsidian, geode bot but never beyond a point where it cannot be spent
        if o >= cost_o and bot_o < max_cost_ore:
            fringe.append(
                ((o + bot_o - cost_o, c + bot_c, ob + bot_ob, g + bot_g), (bot_o + 1, bot_c, bot_ob, bot_g), time))
        if o >= cost_c and bot_c < cost_ob_c:
            fringe.append(
                ((o + bot_o - cost_c, c + bot_c, ob + bot_ob, g + bot_g), (bot_o, bot_c + 1, bot_ob, bot_g), time))
        if o >= cost_ob_o and c >= cost_ob_c and bot_ob < cost_g_ob:
            fringe.append(((o + bot_o - cost_ob_o, c + bot_c - cost_ob_c, ob + bot_ob, g + bot_g),
                           (bot_o, bot_c, bot_ob + 1, bot_g), time))
        if o >= cost_g_o and ob >= cost_g_ob:
            fringe.append(((o + bot_o - cost_g_o, c + bot_c, ob + bot_ob - cost_g_ob, g + bot_g), (bot_o, bot_c, bot_ob,
                                                                                                   bot_g + 1), time))
    return best_geodes


def part1(data: list[Blueprint]) -> int:
    func = partial(solve, time=24)
    with mp.Pool(processes=int(mp.cpu_count() * (2/3))) as pool:
        geodes = pool.map(func, [costs for _, costs in data])

    return sum(_id * g for (_id, _), g in zip(data, geodes))


def part2(data: list[Blueprint]) -> int:
    func = partial(solve, time=32)
    with mp.Pool(processes=min(3, int(mp.cpu_count() * 1/2))) as pool:
        geodes = pool.map(func, [costs for _, costs in data[:3]])

    return math.prod(geodes)


if __name__ == '__main__':
    with Timing():
        with open('19/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data)}')
