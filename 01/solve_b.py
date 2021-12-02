#!/usr/bin/env python3

import sys


def main() -> None:
    numbers = [int(l.strip()) for l in sys.stdin.readlines()]
    # print(repr(numbers))

    windows = list(zip(numbers[:-2], numbers[1:-1], numbers[2:]))
    # print(windows)

    # for window in windows:
    #     print("%-15s | %d" % (window, sum(window)))

    sums = [sum(window) for window in windows]
    pairs = list(zip(sums[:-1], sums[1:]))
    result = [1 for a, b in pairs if a < b]

    print(sum(result))


if __name__ == "__main__":
    main()
