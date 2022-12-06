from time import perf_counter_ns as timestamp_nano


def solve(data: str, n_distinct: int, offset: int = 0) -> int:
    for i in range(offset + n_distinct, len(data)):
        if (len(set(data[i - n_distinct:i])) == n_distinct):
            return i
    return -1


if __name__ == '__main__':
    start = timestamp_nano()

    with open('06/input.txt') as in_file:
        data = in_file.read()

    p1 = solve(data, 4)
    print(f'part1: {p1}')
    print(f'part2: {solve(data, 14, p1 - 4)}')

    end = timestamp_nano()
    print(f'time: {(end - start) / 1000:.3f}µs')
