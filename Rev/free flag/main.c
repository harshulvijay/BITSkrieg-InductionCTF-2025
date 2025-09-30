#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int FLAG_PART1_LEN = 13;
const int FLAG_PART2_LEN = 16;
const int FLAG_PART3_LEN = 17;

const char FLAG_PART1[FLAG_PART1_LEN + 1] = {
    '\x0c', '\x2b', '\x21', '\x30', '\x26', '\x31', '\x2c',
    '\x2a', '\x2b', '\x06', '\x11', '\x03', '\x3e'};
const char FLAG_PART2[FLAG_PART2_LEN + 1] = {
    '\x6c', '\x2e', '\x35', '\x5d', '\x31', '\x74', '\x31', '\x70',
    '\x77', '\x35', '\x66', '\x2f', '\x6c', '\x65', '\x5d', '\xfe'};
const char FLAG_PART3[FLAG_PART3_LEN + 1] = {
    '\x5b', '\x98', '\x89', '\x96', '\x5b', '\x90', '\x5d', '\x89', '\x5b',
    '\x5f', '\x89', '\x90', '\x9c', '\x5d', '\x5d', '\xa7', '\x2a'};

char *process_flag_part1() {
  char *part1_processed = calloc(FLAG_PART1_LEN, sizeof(char));

  for (int i = 0; i < FLAG_PART1_LEN; i++) {
    part1_processed[i] = (long long int)FLAG_PART1[i] ^ 69;
  }

  return part1_processed;
}

char *process_flag_part2() {
  char *part1_processed = calloc(FLAG_PART2_LEN, sizeof(char));

  for (int i = 0; i < FLAG_PART2_LEN; i++) {
    part1_processed[i] = (long long int)FLAG_PART2[i] + 2;
  }

  return part1_processed;
}

char *process_flag_part3() {
  char *part3_processed = calloc(FLAG_PART3_LEN, sizeof(char));

  for (int i = 0; i < FLAG_PART3_LEN; i++) {
    part3_processed[i] = (long long int)FLAG_PART3[i] - 42;
  }

  return part3_processed;
}

void getFlag() {
  char FLAG[FLAG_PART1_LEN + FLAG_PART2_LEN + FLAG_PART3_LEN + 1] = {0};

  strncat(FLAG, process_flag_part1(), FLAG_PART1_LEN);
  strncat(FLAG, process_flag_part2(), FLAG_PART2_LEN);
  strncat(FLAG, process_flag_part3(), FLAG_PART3_LEN);

  printf("%s", FLAG);
}

int main() {
  printf("claim your free flag!\n");

  return 0;
}
