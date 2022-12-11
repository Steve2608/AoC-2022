import dataclasses
import math
from copy import deepcopy
from dataclasses import dataclass
from collections import deque


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
        lines = block.split('\n')
        items = lines[1].strip()[len('Starting items: '):].split(', ')
        operation, operand = lines[2].split(' ')[-2:]
        div_by = lines[3].split(' ')[-1]
        true_target = lines[4].split(' ')[-1]
        false_target = lines[5].split(' ')[-1]

        try:
            operand = int(operand)
        except:
            operand = -1

        mon = Monkey(deque(map(int, items)), operation, operand, int(div_by), int(true_target), int(false_target))
        monkeys.append(mon)
    return monkeys


def solve(monkeys: list[Monkey], rounds: int, worry_decay: int = 0):
    if not worry_decay:
        lcm = math.lcm(*[monkey.div_by for monkey in monkeys])

    inter_count = [0] * len(monkeys)

    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            inter_count[i] += len(monkey.items)
            while monkey.items:
                worry = monkey()
                if not worry_decay:
                    worry %= lcm
                else:
                    worry //= worry_decay
                
                if worry % monkey.div_by == 0:
                    monkeys[monkey.true_target].items.append(worry)
                else:
                    monkeys[monkey.false_target].items.append(worry)
                
    return math.prod(sorted(inter_count)[-2:])

if __name__ == '__main__':
    monkeys = parse_monkeys('11/input.txt')

    print(f'part1: {solve(deepcopy(monkeys), rounds=20, worry_decay=3)}')
    print(f'part1: {solve(deepcopy(monkeys), rounds=10_000)}')
