#!/usr/bin/env python

import sys


def main() -> None:
    horizontal = 0
    depth = 0
    aim = 0

    for line in sys.stdin:
        direction, value_string = line.split()
        value = int(value_string)

        if direction == "down":
            aim += value

        elif direction == "up":
            aim -= value

        elif direction == "forward":
            horizontal += value

            depth += aim * value

    print(horizontal, depth, aim)

    print(horizontal * depth)


if __name__ == "__main__":
    main()
