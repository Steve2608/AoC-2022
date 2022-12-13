from timing_util import print_elapsed, timestamp_nano


def part12(instructions, n_knots: int = 9) -> tuple[int, int]:
    def sign(x: int) -> int:
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0

    # +1 for head
    knots = [(0, 0)] * (n_knots + 1)
    visited1 = set([(knots[0])])
    visited2 = set([(knots[0])])

    for direction, amount in instructions:
        for _ in range(amount):
            head_x, head_y = knots[0]
            match direction:
                case 'U':
                    knots[0] = head_x, head_y + 1
                case 'D':
                    knots[0] = head_x, head_y - 1
                case 'L':
                    knots[0] = head_x - 1, head_y
                case 'R':
                    knots[0] = head_x + 1, head_y

            # drag knots behind
            for i in range(1, n_knots + 1):
                diff_x, diff_y = (a - b for a, b in zip(knots[i - 1], knots[i]))

                if abs(diff_x) > 1 or abs(diff_y) > 1:
                    knots[i] = tuple(x + sign(d) for x, d in zip(knots[i], (diff_x, diff_y)))
                else:
                    break

            visited1.add(knots[1])
            visited2.add(knots[-1])
        
    return len(visited1), len(visited2)

if __name__ == '__main__':
    start = timestamp_nano()

    with open('09/input.txt') as in_file:
        data = [(line[0], int(line.removesuffix('\n')[2:])) for line in in_file]

    p1, p2 = part12(data)
    print(f'part1: {p1}')
    print(f'part2: {p2}')

    print_elapsed(start)
