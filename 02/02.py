from timing_util import timestamp_nano, print_elapsed


def part1(data: list[list[str]]) -> int:
    diff = ord('X') - ord('A')
    wins = {('A', 'Y'), ('B', 'Z'), ('C', 'X')}
    offset = ord('W')

    score = 0
    for opp, you in data:
        if (opp, you) in wins:
            score += 6
        elif ord(opp) + diff == ord(you):
            score += 3

        score += ord(you) - offset
    return score


def part2(data: list[list[str]]) -> int:
    score = 0
    for opp, you in data:
        if you == 'X':  # win
            if opp == 'A':
                score += 3
            elif opp == 'B':
                score += 1
            else:
                score += 2
        elif you == 'Y':  # draw
            score += 3 + (ord(opp) - ord('A') + 1)
        else:  # loss
            score += 6
            if opp == 'A':
                score += 2
            elif opp == 'B':
                score += 3
            else:
                score += 1
    return score


if __name__ == '__main__':
    start = timestamp_nano()

    with open('02/input.txt') as in_file:
        data = [game.rstrip().split(' ') for game in in_file]

    print(f'part1: {part1(data)}')
    print(f'part2: {part2(data)}')

    print_elapsed(start)
