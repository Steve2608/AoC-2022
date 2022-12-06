from time import perf_counter_ns as timestamp_nano
from ctypes import *


if __name__ == '__main__':
    start = timestamp_nano()

    with open('06/input.txt', 'rb') as in_file:
        c_data = create_string_buffer(in_file.read())
        c_data_len = c_size_t(len(c_data))

    # gcc -Wall -std=c17 -pedantic -O2 -shared 06/06.c -o 06/lib06.so
    lib06 = CDLL("06/lib06.so")

    p1 = lib06.solve(c_data, c_data_len, c_size_t(4), c_int(0))
    print(f'part1: {p1}')

    c_p1 = c_int(p1)
    p2 = lib06.solve(c_data, c_data_len, c_size_t(14), c_p1)
    print(f'part2: {p2}')

    end = timestamp_nano()
    print(f'time: {(end - start) / 1000:.3f}µs')
