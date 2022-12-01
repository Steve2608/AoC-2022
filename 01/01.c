#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_LEN 10

int part1(const char* file_name) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return -1;
    }

    int max_elf = -1;
    int curr_elf = 0;

    char line[LINE_LEN];
    while (fgets(line, sizeof(line), fp)) {
        if (line[0] == '\n') {
            if (curr_elf > max_elf) {
                max_elf = curr_elf;
            }
            curr_elf = 0;
        } else {
            curr_elf += atoi(line);
        }
    }
    fclose(fp);

    return max_elf;
}

int part2(const char* file_name) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return -1;
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
            curr_elf += atoi(line);
        }
    }
    fclose(fp);

    return elf_1 + elf_2 + elf_3;
}

int main() {
    int p1 = part1("01/input.txt");
    printf("Part1: %d\n", p1);

    int p2 = part2("01/input.txt");
    printf("Part2: %d\n", p2);
}
