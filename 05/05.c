#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_HEIGHT (N_STACKS * (N_HEADER_LINES - 1))
#define N_STACKS 9
#define N_INSTRUCTIONS 501
#define N_OPERANDS_INSTRUCTION 3
#define N_HEADER_LINES 9
#define N_BYTES_HEADER_LINE 36

typedef signed char byte;

struct cargo {
    char* crates;
    byte* heights;
    byte* instructions;

    int n_stacks;
    int max_height;
    int n_instructions;
    int n_operands_instruction;
};

void free_cargo(struct cargo* c) {
    if (c == NULL) return;
    free(c->instructions);
    free(c->heights);
    free(c->crates);
    free(c);
}

struct cargo* copy_cargo(struct cargo* orig) {
    if (orig == NULL) return NULL;

    struct cargo* copy = malloc(sizeof(struct cargo));
    if (copy == NULL) return NULL;
    copy->n_stacks = orig->n_stacks;
    copy->max_height = orig->max_height;
    copy->n_instructions = orig->n_instructions;
    copy->n_operands_instruction = orig->n_operands_instruction;

    // big 1D array
    copy->crates = malloc(sizeof(char) * (orig->n_stacks * orig->max_height));
    if (copy->crates == NULL) {
        free_cargo(copy);
        return NULL;
    }
    memcpy(copy->crates, orig->crates, sizeof(char) * (orig->n_stacks * orig->max_height));

    copy->heights = malloc(sizeof(byte) * orig->n_stacks);
    if (copy->heights == NULL) {
        free_cargo(copy);
        return NULL;
    }
    memcpy(copy->heights, orig->heights, sizeof(byte) * orig->n_stacks);

    copy->instructions = malloc(sizeof(byte) * (orig->n_instructions * orig->n_operands_instruction));
    if (copy->instructions == NULL) {
        free_cargo(copy);
        return NULL;
    }
    memcpy(copy->instructions, orig->instructions,
           sizeof(byte) * (orig->n_instructions * orig->n_operands_instruction));

    return copy;
}

void print_cargo(struct cargo* c) {
    if (c == NULL) return;

    char* stack = malloc(sizeof(char) * (c->max_height + 1));
    if (stack == NULL) return;

    for (int i = 0; i < c->n_stacks; i++) {
        int j;
        for (j = 0; j < c->heights[i]; j++) {
            stack[j] = c->crates[i * c->max_height + j];
        }
        stack[j] = '\0';
        printf("%d [%hhd]: %s\n", i, c->heights[i], stack);
    }
    printf("\n");
    free(stack);
}

struct cargo* init_cargo(size_t n_stacks, size_t max_height, size_t n_instructions, size_t n_operands_instruction) {
    struct cargo* c = malloc(sizeof(struct cargo));
    if (c == NULL) return NULL;
    c->n_stacks = n_stacks;
    c->max_height = max_height;
    c->n_instructions = n_instructions;
    c->n_operands_instruction = n_operands_instruction;

    // big 1D array
    c->crates = malloc(sizeof(char) * (n_stacks * max_height));
    if (c->crates == NULL) {
        free_cargo(c);
        return NULL;
    }

    c->heights = calloc(n_stacks, sizeof(byte));
    if (c->heights == NULL) {
        free_cargo(c);
        return NULL;
    }

    c->instructions = malloc(sizeof(byte) * (n_instructions * n_operands_instruction));
    if (c->instructions == NULL) {
        free_cargo(c);
        return NULL;
    }

    return c;
}

struct cargo* parse(const char* file_name, size_t n_stacks, size_t max_height, size_t n_instructions,
                    size_t n_operands_instruction, size_t n_header_lines, size_t n_bytes_header_line) {
    FILE* fp = fopen(file_name, "r");
    if (fp == NULL) {
        perror(file_name);
        return NULL;
    }

    struct cargo* c = init_cargo(n_stacks, max_height, n_instructions, n_operands_instruction);
    if (c == NULL) {
        fclose(fp);
        return NULL;
    }

    // n_header_lines lines, each with n_bytes_header_line
    // 1 line with just newline
    // space for '\0'
    int buf_size = ((n_header_lines * n_bytes_header_line) + 1 + 1);
    char* buf = malloc(sizeof(char) * buf_size);
    if (buf == NULL) {
        free_cargo(c);
        fclose(fp);
        return NULL;
    }

    // read buf_size - 1 bytes -> space for '\0'
    if (fread(buf, sizeof(char), buf_size - 1, fp) != buf_size - 1) {
        perror("Invalid header");
        free_cargo(c);
        fclose(fp);
        return NULL;
    }

    // - '\0' - '\n' - enumeration line
    for (int i = buf_size - 1 - 1 - n_bytes_header_line; i > 0; i -= n_bytes_header_line) {
        int offset = (i - n_bytes_header_line) + 1;
        for (int j = 0; j < n_stacks; j++) {
            char crate = buf[offset + j * 4];

            if (crate != ' ') {
                // set crate
                c->crates[j * c->max_height + c->heights[j]] = crate;
                c->heights[j]++;
            }
        }
    }
    // we don't need the header any more
    free(buf);

    byte cnt, src, dst;
    for (int i = 0, offset = 0; i < n_instructions; i++, offset += c->n_operands_instruction) {
        if (fscanf(fp, "move %hhd from %hhd to %hhd\n", &cnt, &src, &dst) != c->n_operands_instruction) {
            perror("Invalid instruction encountered");
            free_cargo(c);
            fclose(fp);
            return NULL;
        }
        c->instructions[offset] = cnt;
        // correct for index=0 offset
        c->instructions[offset + 1] = src - 1;
        c->instructions[offset + 2] = dst - 1;
    }
    fclose(fp);

    return c;
}

char* part1(struct cargo* orig) {
    struct cargo* copy = copy_cargo(orig);
    if (copy == NULL) return NULL;

    // room for '\0'
    char* result = malloc(sizeof(char) * (copy->n_stacks + 1));
    if (result == NULL) {
        free_cargo(copy);
        return NULL;
    }
    result[copy->n_stacks] = '\0';

    for (int i = 0, offset = 0; i < copy->n_instructions; i++, offset += copy->n_operands_instruction) {
        byte cnt = copy->instructions[offset];
        byte src = copy->instructions[offset + 1];
        byte dst = copy->instructions[offset + 2];

        for (int j = 0; j < cnt; j++) {
            // get crate
            copy->heights[src]--;
            char crate = copy->crates[src * copy->max_height + copy->heights[src]];
            copy->crates[src * copy->max_height + copy->heights[src]] = '\0';

            // set crate
            copy->crates[dst * copy->max_height + copy->heights[dst]] = crate;
            copy->heights[dst]++;
        }
    }
    for (int i = 0; i < copy->n_stacks; i++) {
        result[i] = copy->crates[i * copy->max_height + copy->heights[i] - 1];
    }
    free_cargo(copy);

    return result;
}

char* part2(struct cargo* orig) {
    struct cargo* copy = copy_cargo(orig);
    if (copy == NULL) return NULL;

    // room for '\0'
    char* result = malloc(sizeof(char) * (copy->n_stacks + 1));
    if (result == NULL) {
        free_cargo(copy);
        return NULL;
    }
    result[copy->n_stacks] = '\0';

    for (int i = 0, offset = 0; i < copy->n_instructions; i++, offset += copy->n_operands_instruction) {
        byte cnt = copy->instructions[offset];
        byte src = copy->instructions[offset + 1];
        byte dst = copy->instructions[offset + 2];

        copy->heights[src] -= cnt;
        memcpy(&copy->crates[dst * copy->max_height + copy->heights[dst]],
               &copy->crates[src * copy->max_height + copy->heights[src]], sizeof(byte) * cnt);
        copy->heights[dst] += cnt;
    }
    for (int i = 0; i < copy->n_stacks; i++) {
        result[i] = copy->crates[i * copy->max_height + copy->heights[i] - 1];
    }
    free_cargo(copy);

    return result;
}

unsigned long timestamp_nano() {
    struct timespec time;
    timespec_get(&time, TIME_UTC);
    return time.tv_nsec;
}

int main() {
    unsigned long start = timestamp_nano();

    struct cargo* c = parse("05/input.txt", N_STACKS, MAX_HEIGHT, N_INSTRUCTIONS, N_OPERANDS_INSTRUCTION,
                            N_HEADER_LINES, N_BYTES_HEADER_LINE);
    if (c == NULL) exit(EXIT_FAILURE);

    char* p1 = part1(c);
    if (p1 == NULL) {
        free_cargo(c);
        exit(EXIT_FAILURE);
    }
    printf("part1: %s\n", p1);
    free(p1);

    char* p2 = part2(c);
    if (p2 == NULL) {
        free_cargo(c);
        exit(EXIT_FAILURE);
    }
    printf("part2: %s\n", p2);
    free(p2);

    free_cargo(c);

    unsigned long end = timestamp_nano();
    printf("time: %.1fµs\n", (end - start) / 1000.0);

    exit(EXIT_SUCCESS);
}