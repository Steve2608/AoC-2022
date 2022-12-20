from timing_util import print_elapsed, timestamp_nano


def get_data(content: str) -> list[int]:
    return list(map(int, content.splitlines()))


def solve(data: list[int], encryption_key: int = None, n_mixing: int = 1) -> int:
    if encryption_key:
        data = [x * encryption_key for x in data]

    i_zero = data.index(0)
    n = len(data)

    # numbers are not unique -> generate unique key
    data = list(enumerate(data))
    copy = data.copy()
    for _ in range(n_mixing):
        for key_num in data:
            i = copy.index(key_num)
            target = i + copy.pop(i)[1]
            if -n <= target < n:
                copy.insert(target, key_num)
            else:
                copy.insert(target % (n - 1), key_num)

    i_zero = copy.index((i_zero, 0))
    return sum([copy[(i_zero + i) % n][1] for i in [1000, 2000, 3000]])


if __name__ == '__main__':
    start = timestamp_nano()

    with open('20/input.txt') as in_file:
        data = get_data(in_file.read())

    print(f'part1: {solve(data)}')
    print(f'part2: {solve(data, encryption_key=811589153, n_mixing=10)}')

    print_elapsed(start)
