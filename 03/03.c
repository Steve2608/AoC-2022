#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N_ELVES_PER_GROUP 3
// 26 lowercase + 26 uppercase + '\0'
#define ITEM_LENGTH (26 + 26 + 1)
#define N_GROUPS 100

struct solution {
    int p1;
    int p2;
};

char** init_rucksacks(size_t group_size, size_t item_size) {
    char** items = malloc(sizeof(char*) * group_size);
    if (items == NULL) return NULL;

    for (int i = 0; i < group_size; i++) {
        items[i] = malloc(sizeof(char) * item_size);
        if (items[i] == NULL) {
            for (int j = i; j >= 0; j--) free(items[j]);
            free(items);
            return NULL;
        }
    }
    return items;
}

int score(char c) {
    if (c <= 'Z') return c - 'A' + 27;
    return c - 'a' + 1;
}

int part1(char* items, int len) {
    int half = len / 2;
    for (int i = 0; i < half; i++) {
        char c = items[i];
        for (int j = half; j < len; j++) {
            if (c == items[j]) {
                return score(c);
            }
        }
    }
    return -1;
}

int index_of(char needle, char* haystack, int size) {
    for (int i = 0; i < size; i++) {
        if (needle == haystack[i]) return i;
    }
    return -1;
}

int part2(char** items, int* sizes, size_t group_size) {
    for (int i = 0; i < sizes[0]; i++) {
        char needle = items[0][i];
        
        int found = 1;
        for (int j = 1; j < group_size; j++) {
            if (index_of(needle, items[j], sizes[j]) < 0) {
                found = 0;
                break;
            }
        }
        if (found) {
            return score(needle);
        }
    }
    return -1;
}

struct solution* solve(const char* file_name, size_t n_groups, size_t group_size, size_t item_size) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    int* sizes = malloc(sizeof(int) * group_size);
    if (sizes == NULL) {
        fclose(fp);
        return NULL;
    }
    char** items = init_rucksacks(group_size, item_size);
    if (items == NULL) {
        free(sizes);
        fclose(fp);
        return NULL;
    }

    int p1 = 0, p2 = 0;
    for (int i = 0; i < n_groups; i++) {
        for (int j = 0; j < group_size; j++) {
            // error encountered in line
            if (fgets(items[j], item_size, fp) == NULL) {
                fclose(fp);
                free(sizes);
                for (i = 0; i < group_size; i++) free(items[i]);
                free(items);
                perror("Invalid line encountered");
                return NULL;
            }
            sizes[j] = strlen(items[j]);
            // calculate part 1 line-by-line
            p1 += part1(items[j], sizes[j]);
        }
        // batch for part 2
        p2 += part2(items, sizes, group_size);
    }
    fclose(fp);
    free(sizes);
    for (int i = 0; i < group_size; i++) free(items[i]);
    free(items);

    struct solution* sol = malloc(sizeof(struct solution));
    if (sol == NULL) return NULL;
    sol->p1 = p1;
    sol->p2 = p2;

    return sol;
}

unsigned long timestamp_nano() {
    struct timespec time;
    timespec_get(&time, TIME_UTC);
    return time.tv_nsec;
}

int main() {
    unsigned long start = timestamp_nano();

    struct solution* sol = solve("03/input.txt", N_GROUPS, N_ELVES_PER_GROUP, ITEM_LENGTH); 
    if (sol == NULL) exit(EXIT_FAILURE);

    printf("part1: %d\n", sol->p1);
    printf("part2: %d\n", sol->p2);

    free(sol);
    
    unsigned long end = timestamp_nano();
    printf("time: %.1fµs\n", (end - start) / 1000.0);

    exit(EXIT_SUCCESS);
}
