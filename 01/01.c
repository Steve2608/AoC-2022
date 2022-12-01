#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_LEN 10

struct solution {
    int p1;
    int p2;
};

struct solution* solve(const char* file_name) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    int elf_1 = -1;
    int elf_2 = -1;
    int elf_3 = -1;
    int curr_elf = 0;

    char line[LINE_LEN];
    while (fgets(line, sizeof(line), fp)) {
        // empty line
        if (line[0] == '\n') {
            if (curr_elf > elf_1) {
                elf_3 = elf_2;
                elf_2 = elf_1;
                elf_1 = curr_elf;
            } else if (curr_elf > elf_2) {
                elf_3 = elf_2;
                elf_2 = curr_elf;
            } else if (curr_elf > elf_3) {
                elf_3 = curr_elf;
            }
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

    struct solution* sol = malloc(sizeof(struct solution));
    sol->p1 = elf_1;
    sol->p2 = elf_1 + elf_2 + elf_3;
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
