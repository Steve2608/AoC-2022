#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define LINE_LEN 100
#define N_ELVES 3

struct solution {
    int p1;
    int p2;
};

void insertion_sort(int* data, size_t len, int value) {
    if (value <= data[len - 1]) return;

    data[len - 1] = value;
    for (int i = len - 2; i >= 0; i--) {
        if (data[i] < data[i + 1]) {
            value = data[i];
            data[i] = data[i + 1];
            data[i + 1] = value;
        }
    }
}

int* init_array(size_t len) {
    int* data = malloc(sizeof(int) * N_ELVES);
    if (data == NULL) return NULL;

    memset(data, 0, sizeof(int) * len);
    return data;
}

struct solution* solve(const char* file_name) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    int* data = init_array(N_ELVES);
    if (data == NULL) {
        fclose(fp);
        return NULL;
    }

    size_t buf_size = sizeof(char) * LINE_LEN;
    char* line = malloc(buf_size);
    if (line == NULL) {
        fclose(fp);
        free(data);
        return NULL;
    }

    int curr_elf = 0;
    while (fgets(line, buf_size, fp)) {
        // empty line
        if (line[0] == '\n') {
            insertion_sort(data, N_ELVES, curr_elf);
            curr_elf = 0;
        } else {
            int val = atoi(line);
            if (val <= 0) {
                perror("Invalid value encountered");
            } else {
                curr_elf += val;
            }
        }
    }
    fclose(fp);
    free(line);

    struct solution* sol = malloc(sizeof(struct solution));
    if (sol == NULL) {
        free(data);
        return NULL;
    }
    sol->p1 = data[0];
    sol->p2 = sol->p1;
    for (int i = 1; i < N_ELVES; i++) {
        sol->p2 += data[i];
    }
    free(data);

    return sol;
}

unsigned long timestamp_nano() {
    struct timespec time;
    timespec_get(&time, TIME_UTC);
    return time.tv_nsec;
}

int main() {
    unsigned long start = timestamp_nano();

    struct solution* sol = solve("01/input.txt");
    if (sol == NULL) exit(EXIT_FAILURE);

    printf("part1: %d\n", sol->p1);
    printf("part2: %d\n", sol->p2);

    free(sol);

    unsigned long end = timestamp_nano();
    printf("time: %.1fµs\n", (end - start) / 1000.0);

    exit(EXIT_SUCCESS);
}
