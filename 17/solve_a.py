#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import sys

def main() -> None:
    target_bottom = int(sys.argv[1])

    # Only works if target is below submarine
    max_speed = abs(target_bottom) - 1
    print("max speed", max_speed)

    speed = max_speed
    max_height = 0
    while speed:
        max_height += speed
        speed -= 1

    print(max_height)


if __name__ == "__main__":
    main()
