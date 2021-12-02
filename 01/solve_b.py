#!/usr/bin/env python3

import sys


def main() -> None:
    numbers = [int(line.strip()) for line in sys.stdin.readlines()]

    # When comparing two consecutive sliding windows it is enough to compare
    # the unique elements between the windows
    pairs = list(zip(numbers[:-3], numbers[3:]))
    result = sum(1 for a, b in pairs if a < b)

    print(result)


if __name__ == "__main__":
    main()
