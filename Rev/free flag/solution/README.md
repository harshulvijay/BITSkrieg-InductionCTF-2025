# [rev] free flag &mdash; Write Up

When we open the binary in IDA (or Ghidra), we see a function named `getFlag()`.

## Tracing the control flow

`getFlag()` calls three functions - `process_flag_part1`, `process_flag_part2` and `process_flag_part3`.

`process_flag_part1` XORs each element in a hardcoded array `FLAG_PART1` with 0x45.

`process_flag_part2` adds 2 to each element in a hardcoded array `FLAG_PART2`.

`process_flag_part3` subtracts 42 from each element in a hardcoded array `FLAG_PART3`.

## Getting the flag

If we extract the three arrays and apply the operations in the correct order, we will get the flag `InductionCTF{n07_3v3ry7h1ng_1n_l1f3_15_fr33}`.
