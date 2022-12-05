from time import perf_counter_ns as timestamp_nano


if __name__ == '__main__':
    start = timestamp_nano()
    
    with open('01/input.txt') as in_file:
        data = sorted(
            [sum(map(int, elf.split('\n'))) for elf in in_file.read().split('\n\n')],
            reverse=True
        )[:3]

    print(f'part1: {data[0]}')
    print(f'part2: {sum(data)}')
    
    end = timestamp_nano()
    print(f'time: {(end - start) / 1000:.3f}µs')
 