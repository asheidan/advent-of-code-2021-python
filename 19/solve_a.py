#!/usr/bin/env python3.10
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import sys
from math import cos, sin, pi

import numpy
from matplotlib import pyplot as plot


def main() -> None:
    scanner_pings = []
    for scanner in sys.stdin.read().strip().split("\n\n"):
        scanner_lines = scanner.split("\n")
        scanner_pings.append(
            numpy.array(
                [[int(v) for v in line.split(",")] for line in scanner_lines[1:]],
                numpy.int32,
            )
        )

    # Let's use the coordinates for Scanner 0 as our "truth"
    universe = scanner_pings.pop(0)
    print(universe)

    rotations = [
        numpy.array(
            [  # All of these
                [1, 0, 0],
                [0, int(round(cos(alpha))), int(round(sin(alpha)))],
                [0, int(round(-sin(alpha))), int(round(cos(alpha)))],
            ],
            numpy.int32,
        )
        for alpha in [0, pi / 2, pi, 3 * pi / 2]
    ]

    # Either
    facings = list(
        itertools.chain(
            (  # All of these
                numpy.array(
                    [
                        [cos(beta), 0, -sin(beta)],
                        [0, 1, 0],
                        [sin(beta), 0, cos(beta)],
                    ],
                    numpy.int32,
                )
                for beta in [0, pi / 2, pi, 3 * pi / 2]
            ),
            (  # Or 2 of these
                numpy.array(
                    [
                        [cos(theta), sin(theta), 0],
                        [-sin(theta), cos(theta), 0],
                        [0, 0, 1],
                    ],
                    numpy.int32,
                )
                for theta in [pi / 2, 3 * pi / 2]
            ),
        )
    )

    # figure = plot.figure()
    # axis = plot.axes(projection="3d")
    # axis.scatter(universe[:, 0], universe[:, 1], universe[:, 2])
    # axis.scatter(0, 0, 0, c="red")
    # plot.show()

    for number, scanner in enumerate(scanner_pings):
        print(f"Trying to place scanner: {number + 1}")
        # print(scanner)

        # TODO: For all possible axis-rotations
        for rotation, facing in itertools.product(rotations, facings):

            translation = numpy.matmul(rotation, facing)
            print(translation)
            rotated_scanner = numpy.matmul(scanner, translation)

            # For all possible offsets
            # TODO: Optimize to not compare all points with all other points
            for placed_beacon, new_beacon in itertools.product(
                universe, rotated_scanner
            ):

                offset = placed_beacon - new_beacon
                moved_beacons = rotated_scanner + offset

                common_points_count = 0
                for a, b in itertools.product(universe, moved_beacons):
                    if (a == b).all():
                        common_points_count += 1

                if common_points_count >= 12:
                    print("   Placed scanner:", offset, (common_points_count,))

                    break  # For offset points
                    break  # For rotations
                    break  # For all scanners

        return


if __name__ == "__main__":
    main()
