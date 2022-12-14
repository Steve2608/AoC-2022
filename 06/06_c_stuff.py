from ctypes import *

from timing_util import Timing

if __name__ == '__main__':
    with Timing():
        with open('06/input.txt', 'rb') as in_file:
            c_data = create_string_buffer(in_file.read())
            c_data_len = c_size_t(len(c_data))

        # create a shared object first
        # gcc -Wall -std=c17 -pedantic -O2 -shared 06/06.c -o 06/lib06.so
        # load shared object
        lib06 = CDLL("06/lib06.so")

        # get the function from the shared object
        solve = lib06.solve

        # explicitly (!) set the return-type
        solve.restype = c_int

        p1 = solve(c_data, c_data_len, c_size_t(4), c_int(0))
        print(f'part1: {p1}')

        c_p1 = c_int(p1)
        p2 = solve(c_data, c_data_len, c_size_t(14), c_p1)
        print(f'part2: {p2}')
