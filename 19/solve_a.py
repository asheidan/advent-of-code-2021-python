#!/usr/bin/env python3.10
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import os.path
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


def iterate_progress_cache(filename: str):
    print("Read from cache")
    if not os.path.exists(filename):
        return

    with open(filename, "r") as cache_file:
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


def split_partition_indices(points):
    kth = len(points) // 2

    partition_indices = numpy.argpartition(points, kth, axis=0)
    split_indices = []
    for axis in range(3):
        split_indices.append(
            (
                frozenset(partition_indices[:kth, axis]),
                frozenset(partition_indices[(kth + 1) :, axis]),
            )
        )

    return split_indices


def partitioned_product(a_points, b_points, a_split_indices=None, b_split_indices=None):

    if a_split_indices is None:
        a_split_indices = split_partition_indices(a_points)

    if b_split_indices is None:
        b_split_indices = split_partition_indices(b_points)

    for axis in range(3):
        # We don't actually have to compare offsets for all quadrants since the
        # scanners overlap almost the entire facing area
        for backside, quadrant in itertools.product(range(2), range(1)):
            yield from itertools.product(
                a_points[
                    list(
                        a_split_indices[axis][backside]
                        & a_split_indices[(axis + 1) % 3][quadrant // 2]
                        & a_split_indices[(axis + 2) % 3][quadrant % 1]
                    ),
                    :,
                ],
                b_points[
                    list(
                        b_split_indices[axis][(backside + 1) % 2]
                        & b_split_indices[(axis + 1) % 3][quadrant // 2]
                        & b_split_indices[(axis + 2) % 3][quadrant % 1]
                    ),
                    :,
                ],
            )


def main() -> None:
    scanners_to_place = []
    input_filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
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
            split_partition_indices(beacons),
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
                split_partition_indices(beacons),
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
                    for placed_beacons, _, placed_scanner, split_indices in universe:

                        # For all possible offsets
                        for placed_beacon, new_beacon in partitioned_product(
                            placed_beacons, rotated_beacon_data, a_split_indices=split_indices,
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

                                universe.append((moved_beacons, translation, offset, split_partition_indices(moved_beacons)))

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
        else:
            print("COULD NOT PLACE ANY SCANNER?!!")
            return

    all_beacons = itertools.chain(
        *(beacon_data for beacon_data, _rotation, _offset, _split_indices in universe)
    )
    unique_beacons = {tuple(beacon) for beacon in all_beacons}
    print(f"----------------------------------- {len(unique_beacons) : >5} beacons")
    scanner_positions = [offset for _, _, offset, _ in universe]

    max_distance = max(
        numpy.absolute(a - b).sum()
        for a, b in itertools.product(scanner_positions, scanner_positions)
    )
    print(f"----------------------------------- {max_distance : >5} distance")

    # figure = plot.figure()
    #axis = plot.axes(projection="3d")
    #for beacons, rotation, offset, _indices in universe:
    #    # print(rotation, offset)
    #    axis.scatter(beacons[:, 0], beacons[:, 1], beacons[:, 2])
    #    axis.scatter(offset[0], offset[1], offset[2], c="red")
    #plot.show()


if __name__ == "__main__":
    main()
