import dataclasses
import math
import re
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from typing import Iterator

from timing_util import print_elapsed, timestamp_nano


@dataclass(frozen=True, slots=True, repr=False, eq=False, order=False, unsafe_hash=False)
class Monkey:
    items: dataclasses.field(default_factory=deque)
    operation: str
    operand: int
    div_by: int
    true_target: int
    false_target: int

    def __iter__(self) -> Iterator[int]:
        while self.items:
            worry = self.items.popleft()

            match [self.operation, self.operand]:
                case ['+', num]:
                    yield worry + num
                case ['*', -1]:
                    yield worry * worry
                case ['*', num]:
                    yield worry * num


def get_data(content: str) -> list[Monkey]:
    monkeys = []
    for block in content.split('\n\n'):
        # Monkey 0:
        #   Starting items: 71, 86
        #   Operation: new = old * 13
        #   Test: divisible by 19
        #     If true: throw to monkey 6
        #     If false: throw to monkey 7
        match = re.search(r'''Monkey \d+:
  Starting items: (?P<items>(?:\d+(?:, )?)*)
  Operation: new = old (?P<operation>\+|\*) (?P<operand>\d+|old)
  Test: divisible by (?P<divisible>\d+)
    If true: throw to monkey (?P<true>\d+)
    If false: throw to monkey (?P<false>\d+)''', block, re.MULTILINE)
        items = match.group('items').split(', ')
        operation, operand = match.group('operation'), match.group('operand')
        div_by = match.group('divisible')
        true_target = match.group('true')
        false_target = match.group('false')

        try:
            operand = int(operand)
        except:
            operand = -1

        mon = Monkey(deque(map(int, items)), operation, operand, int(div_by), int(true_target), int(false_target))
        monkeys.append(mon)
    return monkeys


def part1(monkeys: list[Monkey], rounds: int, worry_decay: int = 0) -> int:
    inter_count = [0] * len(monkeys)

    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            inter_count[i] += len(monkey.items)
            for worry in monkey:
                worry //= worry_decay
                if worry % monkey.div_by == 0:
                    monkeys[monkey.true_target].items.append(worry)
                else:
                    monkeys[monkey.false_target].items.append(worry)

    return math.prod(sorted(inter_count)[-2:])


def part2(monkeys: list[Monkey], rounds: int) -> int:
    lcm = math.lcm(*[monkey.div_by for monkey in monkeys])
    inter_count = [0] * len(monkeys)

    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            inter_count[i] += len(monkey.items)
            for worry in monkey:
                worry %= lcm
                if worry % monkey.div_by == 0:
                    monkeys[monkey.true_target].items.append(worry)
                else:
                    monkeys[monkey.false_target].items.append(worry)

    return math.prod(sorted(inter_count)[-2:])


if __name__ == '__main__':
    start = timestamp_nano()

    with open('11/input.txt') as in_file:
        monkeys = get_data(in_file.read())

    print(f'part1: {part1(deepcopy(monkeys), 20, worry_decay=3)}')
    print(f'part2: {part2(deepcopy(monkeys), 10_000)}')

    print_elapsed(start)
