# dumb-fuzzer

Mutation-based Dumb Fuzzer — General-purpose Binary Fuzzer

## Overview

A Mutation-based Dumb Fuzzer designed to automatically discover vulnerabilities in binary programs.
It performs mutations on seed files or random byte data, and detects abnormal termination (Crash) of the target program.

## Features

- **Dual Fuzzing Mode**: Seed file-based mode / Random data-based mode
- **4 Mutation Operators**
  - Byte Flip: Replaces bytes at random positions with random values
  - Byte Insert: Inserts random bytes at random positions
  - Byte Delete: Deletes bytes at random positions
  - Byte Duplicate: Duplicates a random block and inserts it
- **Adjustable Mutation Rate**: 0.1% ~ 20%
- **Crash Detection**: SIGSEGV / SIGABRT / SIGBUS / SIGILL / SIGFPE
- **Auto Logging**: Saves the crash-triggering input to `crash/` folder with a timestamp
- **Continuous Operation**: Stable long-term fuzzing with exception handling and timeout (1s)

## Usage

```bash
python3 dumb_fuzzer.py
```

Enter the following when prompted:

```
Target binary path: ./target
Use seed files? (y/n): y
Seed folder path: ./seeds
Seed file extension (press Enter for all):
Mutation rate (1: 0.1%, 2: 1%, 3: 5%, 4: 10%, 5: 20%): 2
```

## Example Output

```
[*] Fuzzing started | Target: ./target
[*] Running... 50 iterations
[!!!] CRASH DETECTED | Signal=SIGSEGV | Saved=./crash/bug_1234567890.crash
```

## Directory Structure

```
dumb-fuzzer/
├── dumb_fuzzer.py   # Main fuzzer code
├── crash/           # Crash inputs saved here (auto-created)
└── tmp/             # Temporary files (auto-created)
```

## Requirements

- Python 3.6+
- Linux / WSL
