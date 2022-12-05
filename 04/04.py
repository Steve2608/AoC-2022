import re
from time import perf_counter_ns as timestamp_nano


def part1(data: list[tuple[int, ...]]) -> int:
    return sum(
        (start1 <= start2 <= end2 <= end1) or (start2 <= start1 <= end1 <= end2)
        for start1, end1, start2, end2 in data
    )


def part2(data: list[tuple[int, ...]]) -> int:
    return sum(
        (start1 <= start2 <= end1) or (start2 <= start1 <= end2)
        for start1, end1, start2, end2 in data
    )


if __name__ == '__main__':
    start = timestamp_nano()

    with open('04/input.txt') as in_file:
        data = [tuple(map(int, (re.search(r'(\d+)-(\d+),(\d+)-(\d+)', line).groups()))) for line in in_file]

    print(f'part1: {part1(data)}')
    print(f'part2: {part2(data)}')

    end = timestamp_nano()
    print(f'{(end - start) / 1000:.3f}µs')
