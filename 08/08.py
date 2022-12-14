from timing_util import Timing


def get_data(content: str) -> list[list[int]]:
    return [list(map(int, line)) for line in content.splitlines()]


def part1(grid: list[list[int]]) -> int:
    # no double counting on corners
    circumference = len(grid) * 2 + len(grid[0]) * 2 - 4

    n_visible = circumference
    for i, row in enumerate(grid[1:-1], 1):
        for j, tree in enumerate(row[1:-1], 1):
            n_visible += all(tree > r[j] for r in grid[:i]) or \
                all(tree > r[j] for r in grid[i+1:]) or \
                all(tree > t for t in row[:j]) or \
                all(tree > t for t in row[j+1:])

    return n_visible


def part2(grid: list[list[int]]) -> int:
    scenic_score = 0
    for i, row in enumerate(grid[1:-1], 1):
        for j, tree in enumerate(row[1:-1], 1):
            score_up = 1
            for r in grid[1:i][::-1]:
                if tree <= r[j]:
                    break
                score_up += 1

            score_left = 1
            for t in row[1:j][::-1]:
                if tree <= t:
                    break
                score_left += 1

            score_down = 1
            for r in grid[i + 1:-1]:
                if tree <= r[j]:
                    break
                score_down += 1

            score_right = 1
            for t in row[j + 1:-1]:
                if tree <= t:
                    break
                score_right += 1

            scenic_score = max(scenic_score, score_up * score_left * score_down * score_right)
    return scenic_score


if __name__ == '__main__':
    with Timing():
        with open('08/input.txt') as in_file:
            data = get_data(in_file.read())

        print(f'part1: {part1(data)}')
        print(f'part2: {part2(data)}')
