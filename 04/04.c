#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N_PAIRS 1000

struct solution {
    int p1;
    int p2;
};

struct solution* solve(const char* file_name, size_t n_pairs) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    // values range from 0-99
    short start1, end1, start2, end2;
    int part1 = 0, part2 = 0;
    for (int i = 0; i < n_pairs; i++) {
        // matching one line exactly
        if (fscanf(fp, "%hi-%hi,%hi-%hi\n", &start1, &end1, &start2, &end2) != 4) {
            perror("Invalid line encountered");
            fclose(fp);
            return NULL;
        }

        if ((start1 <= start2 && end2 <= end1) || (start2 <= start1 && end1 <= end2)) part1++;
        if ((start1 <= start2 && start2 <= end1) || (start2 <= start1 && start1 <= end2)) part2++;

    }
    fclose(fp);

    struct solution* sol = malloc(sizeof(struct solution));
    if (sol == NULL) return NULL;
    sol->p1 = part1;
    sol->p2 = part2;
    return sol;
}

unsigned long timestamp_nano() {
    struct timespec time;
    timespec_get(&time, TIME_UTC);
    return time.tv_nsec;
}

int main() {
    unsigned long start = timestamp_nano();

    struct solution* sol = solve("04/input.txt", N_PAIRS);
    if (sol == NULL) exit(EXIT_FAILURE);

    printf("part1: %d\n", sol->p1);
    printf("part2: %d\n", sol->p2);

    free(sol);

    unsigned long end = timestamp_nano();
    printf("time: %.1fµs\n", (end - start) / 1000.0);

    exit(EXIT_SUCCESS);
}