import math
import re
from collections import deque
from typing import TypeAlias

from timing_util import Timing

Blueprint: TypeAlias = tuple[int, tuple[int, int, int, int, int, int]]


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


def solve(cost_o, cost_c, cost_ob_o, cost_ob_c, cost_g_o, cost_g_ob, time: int) -> int:
    max_cost_ore = max([cost_o, cost_c, cost_ob_o, cost_g_o])
    fringe = deque([((0, 0, 0, 0), (1, 0, 0, 0), time)])
    visited = set()
    best_geodes = 0
    while fringe:
        (o, c, ob, g), (bot_o, bot_c, bot_ob, bot_g), time = fringe.popleft()
        if time == 0:
            best_geodes = max(g, best_geodes)
            continue

        # discard surplus resources in production to reduce the number of states
        bot_o = min(bot_o, max_cost_ore)
        bot_c = min(bot_c, cost_ob_c)
        bot_ob = min(bot_ob, cost_g_ob)

        # throw away surplus resources that cannot be spent in time
        o = min(o, time * max_cost_ore - bot_o * (time - 1))
        c = min(c, time * cost_ob_c - bot_c * (time - 1))
        ob = min(ob, time * cost_g_ob - bot_ob * (time - 1))

        if (state := ((o, c, ob, g), (bot_o, bot_c, bot_ob, bot_g))) in visited:
            continue

        visited.add(state)

        time -= 1
        # do nothing
        fringe.append(((o + bot_o, c + bot_c, ob + bot_ob, g + bot_g), (bot_o, bot_c, bot_ob, bot_g), time))

        # buy ore, clay, obsidian, geode bot
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
    return sum(_id * solve(*robot, time=24) for _id, robot in data)


def part2(data: list[Blueprint]) -> int:
    return math.prod(solve(*robot, time=32) for _, robot in data[:3])


if __name__ == '__main__':
    with Timing():
        with open('19/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data)}')
