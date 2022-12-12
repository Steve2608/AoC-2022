import dataclasses
import math
import re
from copy import deepcopy
from dataclasses import dataclass
from collections import deque
from time import perf_counter_ns as timestamp_nano


@dataclass
class Monkey:
    items: dataclasses.field(default_factory=deque)
    operation: str
    operand: int
    div_by: int
    true_target: int
    false_target: int

    def __call__(self):
        worry = self.items.popleft()

        match [self.operation, self.operand]:
            case ['+', num]:
                return worry + num
            case ['*', -1]:
                return worry * worry
            case ['*', num]:
                return worry * num 


def parse_monkeys(path: str):
    with open(path) as in_file:
        content = in_file.read()

    monkeys = []
    for block in content.split('\n\n'):
        # Monkey 0:
        #   Starting items: 71, 86
        #   Operation: new = old * 13
        #   Test: divisible by 19
        #     If true: throw to monkey 6
        #     If false: throw to monkey 7
        match = re.search(r'''Monkey \d+:
  Starting items: (?P<item>\d+)(?P<items>(?:, \d+)*)
  Operation: new = old (?P<operation>\+|\*) (?P<operand>\d+|old)
  Test: divisible by (?P<divisible>\d+)
    If true: throw to monkey (?P<true>\d+)
    If false: throw to monkey (?P<false>\d+)''', block, re.MULTILINE)
        items = [match.group('item')] + list(filter(bool, match.group('items').split(', ')))
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
            while monkey.items:
                worry = monkey() // worry_decay
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
            while monkey.items:
                worry = monkey() % lcm
                if worry % monkey.div_by == 0:
                    monkeys[monkey.true_target].items.append(worry)
                else:
                    monkeys[monkey.false_target].items.append(worry)
                
    return math.prod(sorted(inter_count)[-2:])


if __name__ == '__main__':
    start = timestamp_nano()

    monkeys = parse_monkeys('11/input.txt')

    print(f'part1: {part1(deepcopy(monkeys), 20, worry_decay=3)}')
    print(f'part2: {part2(deepcopy(monkeys), 10_000)}')

    end = timestamp_nano()
    print(f'time: {(end - start) / 1e6:.3f}ms')
