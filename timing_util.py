from time import perf_counter_ns as timestamp_nano

def print_elapsed(start):
    end = timestamp_nano()

    diff = (end - start)
    if diff < 1e3:
        print(f'time: {diff:.3f}ns')
    elif diff < 1e6:
        print(f'time: {diff / 1e3:.3f}µs')
    elif diff < 1e9:
        print(f'time: {diff / 1e6:.3f}ms')
    else:
        print(f'time: {diff / 1e9:.3f}s')
