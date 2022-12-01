#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_LEN 100
#define N_ELVES 3
#define LAST_INDEX N_ELVES - 1

struct solution {
    int p1;
    int p2;
};

void insertion_sort(int* data, int value) {
    if (value <= data[LAST_INDEX]) return;

    data[LAST_INDEX] = value;

    for (int i = LAST_INDEX - 1; i >= 0; i--) {
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

    for (int i = 0; i < N_ELVES; i++) {
        data[i] = 0;
    }
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
            insertion_sort(data, curr_elf);
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

int main() {
    struct solution* sol = solve("01/input.txt");
    if (sol == NULL) exit(EXIT_FAILURE);

    printf("Part1: %d\n", sol->p1);
    printf("Part2: %d\n", sol->p2);

    free(sol);

    exit(EXIT_SUCCESS);
}
