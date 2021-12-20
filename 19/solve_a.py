#!/usr/bin/env python3.10
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import sys
from math import cos, sin, pi

import numpy
from matplotlib import pyplot as plot
from tqdm import tqdm


def log_progress(file_name: str, scanner: int, translation, offset) -> None:
    translation_data = ",".join(map(str, itertools.chain(*translation)))
    offset_data = ",".join(map(str, offset))
    with open(file_name, "a") as progress_file:
        progress_file.write("|".join((str(scanner), offset_data, translation_data)))
        progress_file.write("\n")


def iterate_progress_cache(file_name: str):
    print("Read from cache")
    with open(file_name, "r") as cache_file:
        for line in cache_file.readlines():
            scanner_index, offset_data, translation_data = line.strip().split("|")
            offset = numpy.array(offset_data.split(","), numpy.int32)
            translation = numpy.array(translation_data.split(","), numpy.int32).reshape(
                (3, 3)
            )
            print(scanner_index, offset)
            yield (int(scanner_index), offset, translation)

    print("--- Cache done")
    return


def partitioned_product(a_points, b_points):

    a_kth = len(a_points) // 2
    b_kth = len(b_points) // 2

    a_partition_indices = numpy.partition(a_points, a_kth, axis=0)
    b_partition_indices = numpy.partition(b_points, b_kth, axis=0)

    # Front / Back
    a_x_min = a_partition_indices[:a_kth, 0]
    a_x_max = a_partition_indices[(a_kth + 1) :, 0]

    b_x_min = b_partition_indices[:b_kth, 0]
    b_x_max = b_partition_indices[(b_kth + 1) :, 0]

    itertools.product(
        a_points[a_x_max, :],
        b_points[b_x_min, :],
    )
    # a_points[, :]
    # b_points[b_partition_indices[b_kth:, 0], :]
    #for a_point, b_point in itertools.product


def main() -> None:
    scanners_to_place = []
    input_filename = sys.argv[1]
    cache_filename = f"{input_filename}.progress"
    with open(input_filename, "r") as data_file:
        for beacon_data in data_file.read().strip().split("\n\n"):
            scanner_lines = beacon_data.split("\n")
            scanners_to_place.append(
                numpy.array(
                    [[int(v) for v in line.split(",")] for line in scanner_lines[1:]],
                    numpy.int32,
                )
            )

    # Let's use the coordinates for Scanner 0 as our first "truth"
    beacons = scanners_to_place.pop(0)
    universe = [
        # Placed beacons, rotational matrix, offset
        (
            beacons,
            numpy.identity(3, numpy.int32),
            numpy.zeros(3, numpy.int32),
            # numpy.partition(beacons, len(beacons) // 2, axis=0),
        ),
    ]

    for scanner_index, offset, translation in iterate_progress_cache(cache_filename):
        beacons = scanners_to_place.pop(scanner_index)
        beacons = numpy.matmul(beacons, translation) + offset
        universe.append(
            (
                beacons,
                translation,
                offset,
                # numpy.partition(beacons, len(beacons) // 2, axis=0),
            )
        )

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

            description = f"U:{len(universe) : >2} | P:{len(scanners_to_place) : >2} | S:{number + 1 : >2} |"
            # For all possible axis-rotations
            with tqdm(desc=description, total=24) as progress_bar:
                for rotation, facing in itertools.product(rotations, facings):
                    progress_bar.update(1)

                    translation = numpy.matmul(rotation, facing)
                    # print(translation)
                    rotated_beacon_data = numpy.matmul(beacon_data, translation)

                    # For all placed scanners (in reverse to try to optimize)
                    for placed_beacons, _, placed_scanner in universe:

                        # For all possible offsets
                        # TODO: Optimize to not compare all points with all other points
                        for placed_beacon, new_beacon in itertools.product(
                            placed_beacons, rotated_beacon_data
                        ):

                            offset = placed_beacon - new_beacon
                            moved_beacons = rotated_beacon_data + offset

                            common_points_count = len(
                                frozenset(map(tuple, placed_beacons)).intersection(
                                    frozenset(map(tuple, moved_beacons))
                                )
                            )

                            if common_points_count >= 12:
                                progress_bar.close()

                                log_progress(
                                    file_name=cache_filename,
                                    scanner=number,
                                    translation=translation,
                                    offset=offset,
                                )
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

    all_beacons = itertools.chain(
        *(beacon_data for beacon_data, _rotation, _offset in universe)
    )
    unique_beacons = {tuple(beacon) for beacon in all_beacons}
    print(f"----------------------------------- {len(unique_beacons) : >5} beacons")
    scanner_positions = [offset for _, _, offset in universe]

    max_distance = max(numpy.absolute(a - b).sum() for a, b in itertools.product(scanner_positions, scanner_positions))
    print(f"----------------------------------- {max_distance : >5} distance")


    # figure = plot.figure()
    axis = plot.axes(projection="3d")
    for beacons, rotation, offset in universe:
        #print(rotation, offset)
        axis.scatter(beacons[:, 0], beacons[:, 1], beacons[:, 2])
        axis.scatter(offset[0], offset[1], offset[2], c="red")

    plot.show()


if __name__ == "__main__":
    main()
