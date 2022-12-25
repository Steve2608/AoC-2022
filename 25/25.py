from timing_util import Timing


def get_data(content: str) -> list[list[str]]:
    return content.splitlines()


def snafu_2_int(snafu: str) -> int:
    lookup = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    dec = 0
    for digit in snafu:
        dec = dec * 5 + lookup[digit]
    return dec


def int_2_snafu(dec: int) -> str:
    def int_2_snafu_rec(dec: int, d5: int) -> str:
        if -2 <= dec <= 2:
            return lookup[dec]

        for d in [-2, -1, 0, 1, 2]:
            num = dec - d5 * d
            if abs(num) <= max_snafu_value(d5 // 5):
                return lookup[d] + int_2_snafu_rec(num, d5 // 5)

    def max_snafu_value(d5: int) -> int:
        if d5 == 1:
            return 2
        return d5 * 2 + max_snafu_value(d5 // 5)

    lookup = {2: '2', 1: '1', 0: '0', -1: '-', -2: '='}

    d5 = 1
    while abs(dec) > max_snafu_value(d5):
        d5 *= 5

    return int_2_snafu_rec(dec, d5)


def part1(data: list[str]) -> int:
    return int_2_snafu(sum(map(snafu_2_int, data)))


if __name__ == '__main__':
    with Timing():
        with open('25/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
