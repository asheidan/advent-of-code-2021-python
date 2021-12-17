#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import sys

TARGET = (
    (20, 30),
    (-10, -5),
)


def main() -> None:
    target_x = range(TARGET[0][0], TARGET[0][1] + 1)
    target_y = range(TARGET[1][0], TARGET[1][1] + 1)

    # Only works if target is below submarine
    max_speed_y = abs(target_y.start) - 1
    max_speed_x = target_x.stop - 1
    # print("max speed y:", max_speed_y)

    speeds_x = range(1, max_speed_x + 1)
    speeds_y = range(-(max_speed_y + 1), max_speed_y + 1)

    target_speed_count = 0
    for start_speed in itertools.product(speeds_x, speeds_y):
        speed_x, speed_y = start_speed
        pos_x, pos_y = (0, 0)
        while pos_x < target_x.stop and pos_y >= target_y.start:
            pos_x += speed_x
            pos_y += speed_y

            if pos_x in target_x and pos_y in target_y:
                # print(start_speed)
                target_speed_count += 1

                break

            speed_y -= 1

            if speed_x:
                speed_x -= 1

            elif pos_x < TARGET[0][0]:

                break

    print(target_speed_count)

if __name__ == "__main__":
    main()
