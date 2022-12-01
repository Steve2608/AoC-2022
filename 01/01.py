if __name__ == '__main__':
    with open('01/input.txt') as in_file:
        data = sorted(
            [sum(map(int, elf.split('\n'))) for elf in in_file.read().split('\n\n')],
            reverse=True
        )[:3]

    print(f'part1: {data[0]}')
    print(f'part2: {sum(data)}')
