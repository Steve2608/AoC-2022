from timing_util import timestamp_nano, print_elapsed


def part1(data: list[str], instructions: list[tuple[int, int, int]]) -> str:
    containers = data.copy()
    for (cnt, src, dst) in instructions:
        src -= 1
        dst -= 1
        for _ in range(cnt):
            containers[dst] += containers[src][-1]
            containers[src] = containers[src][:-1]

    return ''.join((x[-1] for x in containers))


def part2(data: list[str], instructions: list[tuple[int, int, int]]) -> str:
    containers = data.copy()
    for (cnt, src, dst) in instructions:
        src -= 1
        dst -= 1
        containers[dst] += containers[src][-cnt:]
        containers[src] = containers[src][:-cnt]

    return ''.join((x[-1] for x in containers))


if __name__ == '__main__':
    start = timestamp_nano()

    with open('05/input.txt') as in_file:
        content = in_file.read()

        N_STACKS = 9
        initial, instructions = content.split('\n\n')
        data = ['' for _ in range(N_STACKS)]
        # remove numbered line
        initial = initial.split('\n')[:-1]
        for line in initial[::-1]:
            for i in range(N_STACKS):
                if (char := line[1 + i * 4]) != ' ':
                    data[i] += char

        instructions = [tuple(map(int, line.split(' ')[1::2])) for line in instructions.split('\n')]

    print(f'part1: {part1(data, instructions)}')
    print(f'part2: {part2(data, instructions)}')

    print_elapsed(start)
