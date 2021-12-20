#!/usr/bin/env python3.10
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import sys
from math import cos, sin, pi

import numpy
from matplotlib import pyplot as plot


def main() -> None:
    scanners_to_place = []
    for beacon_data in sys.stdin.read().strip().split("\n\n"):
        scanner_lines = beacon_data.split("\n")
        scanners_to_place.append(
            numpy.array(
                [[int(v) for v in line.split(",")] for line in scanner_lines[1:]],
                numpy.int32,
            )
        )

    # Let's use the coordinates for Scanner 0 as our first "truth"
    universe = [
        # Placed beacons, rotational matrix, offset
        (scanners_to_place.pop(0), numpy.identity(3, numpy.int32), numpy.zeros(3, numpy.int32)),
    ]
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

    while scanners_to_place:

        for number, beacon_data in enumerate(scanners_to_place):
            print(f"Trying to place scanner: {number + 1 : >2} ({len(universe)}|{len(scanners_to_place)})")
            # print(scanner)

            # For all possible axis-rotations
            for rotation_progress, (rotation, facing) in enumerate(itertools.product(rotations, facings)):
                print(f"\r{rotation_progress : >2} / 24", file=sys.stderr, end="")

                translation = numpy.matmul(rotation, facing)
                # print(translation)
                rotated_beacon_data = numpy.matmul(beacon_data, translation)

                # For all placed scanners (in reverse to try to optimize)
                for placed_beacons, _, placed_scanner in reversed(universe):

                    # For all possible offsets
                    # TODO: Optimize to not compare all points with all other points
                    for placed_beacon, new_beacon in itertools.product(
                        placed_beacons, rotated_beacon_data
                    ):

                        offset = placed_beacon - new_beacon
                        moved_beacons = rotated_beacon_data + offset

                        common_points_count = 0
                        for a, b in itertools.product(placed_beacons, moved_beacons):
                            if (a == b).all():
                                common_points_count += 1

                        if common_points_count >= 12:
                            print("   Placed scanner:", offset, common_points_count)

                            universe.append((moved_beacons, translation, offset))

                            scanners_to_place.pop(number)

                            break  # For offset points
                    else:
                        continue
                    break  # For all placed scanners
                else:
                    continue
                break  # For rotations
            else:
                continue
            break  # For scanners to place

    # figure = plot.figure()
    axis = plot.axes(projection="3d")
    for beacons, rotation, offset in universe:
        print(rotation, offset)
        axis.scatter(beacons[:, 0], beacons[:, 1], beacons[:, 2])
        axis.scatter(offset[0], offset[1], offset[2], c="red")

    plot.show()


    return


if __name__ == "__main__":
    main()
