#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N_GAMES 2500
// <c>_<c>\n\0
#define LINE_LEN 5

char* read_data(const char* file_name, size_t n_games, size_t line_len) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    char* games = malloc(sizeof(char) * (n_games * 2));
    if (games == NULL) {
        fclose(fp);
        return NULL;
    }

    char* buf = malloc(sizeof(char) * line_len);
    if (buf == NULL) {
        fclose(fp);
        free(games);
        return NULL;
    }

    int i = 0;
    while (fgets(buf, line_len, fp) != NULL) {
        games[i++] = buf[0];
        games[i++] = buf[2];
    }
    fclose(fp);
    free(buf);

    return games;
}

int part1(char* data, size_t n_games) {
    char diff = 'X' - 'A';
    char offset = 'W';

    int score = 0;
    for (int i = 0; i < n_games * 2; i++) {
        char opp = data[i++];
        char you = data[i];

        if (opp + diff == you) {
            score += 3;
        } else if ((opp == 'A' && you == 'Y') || (opp == 'B' && you == 'Z') ||
                   (opp == 'C' && you == 'X')) {
            score += 6;
        }

        score += you - offset;
    }

    return score;
}

int part2(char* data, size_t n_games) {
    int score = 0;
    for (int i = 0; i < n_games * 2; i++) {
        char opp = data[i++];
        char you = data[i];

        if (you == 'X') {  // loss
            if (opp == 'A')
                score += 3;
            else if (opp == 'B')
                score += 1;
            else
                score += 2;
        } else if (you == 'Y') {  // draw
            score += 3 + (opp - 'A' + 1);
        } else {  // win
            score += 6;
            if (opp == 'A')
                score += 2;
            else if (opp == 'B')
                score += 3;
            else
                score += 1;
        }
    }

    return score;
}

unsigned long timestamp_nano() {
    struct timespec time;
    timespec_get(&time, TIME_UTC);
    return time.tv_nsec;
}

int main() {
    unsigned long start = timestamp_nano();

    char* data = read_data("02/input.txt", N_GAMES, LINE_LEN);
    if (data == NULL) exit(EXIT_FAILURE);

    int p1 = part1(data, N_GAMES);
    printf("part1: %d\n", p1);

    int p2 = part2(data, N_GAMES);
    printf("part2: %d\n", p2);

    free(data);

    unsigned long end = timestamp_nano();
    printf("time: %.1f??s\n", (end - start) / 1000.0);

    exit(EXIT_SUCCESS);
}
