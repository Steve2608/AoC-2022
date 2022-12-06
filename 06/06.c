#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define FILE_SIZE 4096

char* read_data(const char* file_name, size_t file_size) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) return NULL;

    char* data = malloc(sizeof(char) * file_size);
    if (data == NULL) {
        fclose(fp);
        return NULL;
    }

    if (fread(data, sizeof(char), file_size, fp) != file_size - 1) {
        free(data);
        fclose(fp);
        return NULL;
    }
    fclose(fp);

    return data;
}

int solve(char* data, size_t data_len, size_t n_distinct) {
    for (int i = n_distinct; i < data_len;) {
        int j, k, start = i - n_distinct;

        for (j = start; j < i; j++) {
            for (k = i - 1; k >= start; k--) {
                if (j != k && data[j] == data[k]) {
                    goto not_header;
                }
            }
        }
        // no duplicate in last n_distinct characeters
        return i;

    not_header:
        // duplicate found, just continue

        // shift sliding window past current duplicate
        i += abs(j - k);
    }
    return -1;
}

unsigned long timestamp_nano() {
    struct timespec time;
    timespec_get(&time, TIME_UTC);
    return time.tv_nsec;
}

int main() {
    unsigned long start = timestamp_nano();

    char* data = read_data("06/input.txt", FILE_SIZE);

    int p1 = solve(data, FILE_SIZE - 1, 4);
    printf("part1: %d\n", p1);

    int p2 = solve(data, FILE_SIZE - 1, 14);
    printf("part2: %d\n", p2);

    free(data);

    unsigned long end = timestamp_nano();
    printf("time: %.1fµs\n", (end - start) / 1000.0);

    exit(EXIT_SUCCESS);
}
