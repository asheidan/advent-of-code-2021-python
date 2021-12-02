#!/usr/bin/env python3

import sys


def main() -> None:
    numbers = [int(l.strip()) for l in sys.stdin.readlines()]
    # print(repr(numbers))

    pairs = list(zip(numbers[:-1], numbers[1:], range(len(numbers) - 1)))
    # print(pairs)

    # for a, b, i in pairs:
    #     print("%5d | %5d %5d | %d" % (i, a, b, int(a < b)))

    result = [1 for a, b, _ in pairs if a < b]
    # print(result)

    print(sum(result))


if __name__ == "__main__":
    main()
