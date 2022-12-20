from collections import defaultdict

from timing_util import Timing


def get_data(content: str) -> dict[str, int]:
    sizes = defaultdict(int)
    cwd = ['']

    for line in content.splitlines():
        match line.removesuffix('\n').split(' '):
            case ['$', 'cd', '/']:
                cwd = ['/']
            case ['$', 'cd', '..']:
                cwd = cwd[:-1]
            case ['$', 'cd', target]:
                cwd.append(target)
            case [num, _] if num.isdigit():
                s = int(num)

                pwd = '/'
                sizes[pwd] += s
                for part in cwd:
                    pwd += part + '/'
                    sizes[pwd] += s

    return sizes


def part1(sizes: dict[str, int]) -> int:
    return sum(s for s in sizes.values() if s <= 100e3)


def part2(sizes: dict[str, int]) -> int:
    min_free = sizes['/'] - (70e6 - 30e6)
    return min(s for s in sizes.values() if s >= min_free)


if __name__ == '__main__':
    with Timing():
        with open('07/input.txt') as in_file:
            sizes = get_data(in_file.read())

        print(f'part1: {part1(sizes)}')
        print(f'part2: {part2(sizes)}')
