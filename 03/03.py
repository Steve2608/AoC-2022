from timing_util import Timing


def get_data(content: str) -> list[str]:
    return content.splitlines()


def score(char: str) -> int:
    if (o := ord(char)) <= ord('Z'):
        return 27 + (o - ord('A'))
    else:
        return 1 + (o - ord('a'))


def part1(data: list[str]) -> int:
    s = 0
    for line in data:
        middle = len(line) // 2
        char = (set(line[:middle]) & set(line[middle:])).pop()

        s += score(char)
    return s


def part2(data: list[str]) -> int:
    s = 0
    for i in range(len(data) // 3):
        group = data[i * 3:(i + 1) * 3]
        common_badge = (set(group[0]) & set(group[1]) & set(group[2])).pop()

        s += score(common_badge)
    return s


if __name__ == '__main__':
    with Timing():
        with open('03/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data)}')
