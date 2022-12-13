from timing_util import print_elapsed, timestamp_nano


def part1(instructions: list[str]) -> int:
    def sig_stren() -> int:
        if (i - 20) % 40 == 0:
            return i * x
        return 0

    i = 1
    x = 1
    signal = 0

    for instr in instructions:
        match instr.split(' '):
            case ['noop']:
                i += 1
            case ['addx', num]:
                i += 1
                signal += sig_stren()
                x += int(num)
                i += 1

        signal += sig_stren()

    return signal


def part2(instructions: list[str], crt_width: int = 40) -> int:
    def shift_i():
        nonlocal i
        i = (i + 1) % crt_width
    
    def append_buf():
        if sprite - 1 <= i <= sprite + 1:
            buf.append('#')
        else:
            buf.append('.')

    i = 0
    sprite = 1
    buf = []
    for instr in instructions:
        append_buf()

        match instr.split(' '):
            case ['noop']:
                shift_i()
            case ['addx', num]:
                shift_i()
                append_buf()

                shift_i()
                sprite += int(num)
    
    for i, step in enumerate(range(crt_width, crt_width*6, crt_width)):
        buf.insert(step + i, '\n')
    
    return ''.join(buf)


if __name__ == '__main__':
    start = timestamp_nano()

    with open('10/input.txt') as in_file:
        data = [line.rstrip() for line in in_file]

    print(f'part1: {part1(data)}')
    print(f'part2:\n{part2(data, crt_width=40)}')

    print_elapsed(start)
