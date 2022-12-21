from functools import cache

from timing_util import Timing


def get_data(content: str) -> list[str, str]:
    return dict(line.split(': ') for line in content.splitlines())


def part1(data: list[str, str], root: str = 'root') -> int:
    def eval_monkeys(monkey: str) -> int:
        value = data[monkey]
        try:
            return int(value)
        except ValueError:
            left, op, right = value.split()
            match op:
                case '*':
                    return eval_monkeys(left) * eval_monkeys(right)
                case '/':
                    return eval_monkeys(left) // eval_monkeys(right)
                case '+':
                    return eval_monkeys(left) + eval_monkeys(right)
                case '-':
                    return eval_monkeys(left) - eval_monkeys(right)
    
    return eval_monkeys(root)


def part2(data: list[str, str], root: str = 'root') -> int:
    @cache
    def walk_until_humn(monkey: str) -> int | None:
        if monkey == 'humn':
            raise ValueError

        value = data[monkey]
        try:
            return int(value)
        except ValueError:
            left, op, right = value.split()
            match op:
                case '*':
                    return walk_until_humn(left) * walk_until_humn(right)
                case '/':
                    return walk_until_humn(left) // walk_until_humn(right)
                case '+':
                    return walk_until_humn(left) + walk_until_humn(right)
                case '-':
                    return walk_until_humn(left) - walk_until_humn(right)
    
    def solve_monkeys(monkey: str, parent: int = None) -> int:
        if monkey == 'humn':
            return parent

        value = data[monkey]
        try:
            return int(value)
        except ValueError:
            left, op, right = value.split()
            try:
                left_val = walk_until_humn(left)
            except ValueError:
                left_val = None

            try:
                right_val = walk_until_humn(right)
            except ValueError:
                right_val = None                    

            if left_val:
                val, target = left_val, right
            else:
                val, target = right_val, left

            # root has no operation
            if monkey == root:
                return solve_monkeys(target, val)

            match op:
                # + and * are commutative, - and / aren't
                case '+':
                    return solve_monkeys(target, parent - val)
                case '*':
                    return solve_monkeys(target, parent // val)
                
                case '-':
                    if left_val:
                        # something - <humn> = parent
                        return solve_monkeys(target, val - parent)
                    else:
                        # <humn> - something = parent
                        return solve_monkeys(target, parent + val)

                case '/':
                    if left_val:
                        # something / <humn> = parent
                        return solve_monkeys(target, val // parent)
                    else:
                        # <humn> / something = parent
                        return solve_monkeys(target, parent * val)
    
    return solve_monkeys(root, parent=None)


if __name__ == '__main__':
    with Timing():
        with open('21/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data)}')
