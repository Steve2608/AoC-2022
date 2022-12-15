from timing_util import print_elapsed, timestamp_nano


def get_data(content: str) -> list[list[int]]:
    return [list(map(int, elf.split('\n'))) for elf in content.split('\n\n')]


def part12(data: list[list[int]]) -> tuple[int, int]:
    res = sorted([sum(elf) for elf in data], reverse=True)[:3]
    return res[0], sum(res)


if __name__ == '__main__':
    start = timestamp_nano()

    with open('01/input.txt') as in_file:
        data = get_data(in_file.read())

    p1, p2 = part12(data)
    print(f'part1: {p1}')
    print(f'part2: {p2}')

    print_elapsed(start)
