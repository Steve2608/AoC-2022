from collections import defaultdict

from timing_util import timestamp_nano, print_elapsed


def file_system(path: str) -> dict[str, int]:
    sizes = defaultdict(int)
    cwd = ['']

    with open(path) as in_file:
        for line in in_file:
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


if __name__ == '__main__':
    start = timestamp_nano()

    sizes = file_system('07/input.txt')

    p1 = sum(s for s in sizes.values() if s <= 100e3)
    print(f'part1: {p1}')

    min_free = sizes['/'] - (70e6 - 30e6)
    p2 = min(s for s in sizes.values() if s >= min_free)
    print(f'part2: {p2}')

    print_elapsed(start)
