from timing_util import Timing


def get_data(content: str) -> list[int]:
    return list(map(int, content.splitlines()))


def solve(data: list[int], encryption_key: int = None, n_mixing: int = 1) -> int:
    i_zero = data.index(0)
    n = len(data)

    if encryption_key:
        data = [x * encryption_key for x in data]

    # numbers are not unique -> generate unique key
    data = list(enumerate(data))
    ring = data.copy()
    for _ in range(n_mixing):
        for key_num in data:
            i = ring.index(key_num)
            i += ring.pop(i)[1]

            # python negative indexing works in [-n, n)
            if not (-n <= i < n):
                # otherwise wrap around the n-1 long list
                i %= n - 1

            ring.insert(i, key_num)

    i_zero = ring.index((i_zero, 0))
    return sum([ring[(i_zero + i) % n][1] for i in [1000, 2000, 3000]])


if __name__ == '__main__':
    with Timing():
        with open('20/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {solve(data)}')
        print(f'part2: {solve(data, encryption_key=811589153, n_mixing=10)}')
