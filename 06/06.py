from time import perf_counter_ns as timestamp_nano


def solve(data: str, n_distinct: int) -> int:
    for i in range(n_distinct, len(data)):
        if (len(set(data[i - n_distinct:i])) == n_distinct):
            return i
    return -1


if __name__ == '__main__':
    start = timestamp_nano()

    with open('06/input.txt') as in_file:
        data = in_file.read()

    print(f'part1: {solve(data, 4)}')
    print(f'part2: {solve(data, 14)}')

    end = timestamp_nano()
    print(f'time: {(end - start) / 1000:.3f}µs')
