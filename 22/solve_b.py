#!/usr/bin/env python3

import math
import sys
import itertools
import unittest
from dataclasses import dataclass
from typing import Iterator, Tuple, Optional, Iterable

try:
    from matplotlib import pyplot
except ImportError:
    pyplot = None


@dataclass(frozen=True)
class Dimension:
    start: int
    stop: int

    def cut(self, other: "Dimension") -> Iterable["Dimension"]:
        if self.start < other.start:
            if self.stop < other.start:
                return (self,)

            elif self.stop <= other.stop:
                return (Dimension(self.start, other.start - 1),
                        Dimension(other.start, self.stop))

            else:  # Other contained by self
                return (
                    Dimension(self.start, other.start - 1),
                    other,
                    Dimension(other.stop + 1, self.stop),
                )

        elif self.start >= other.start:
            if self.start > other.stop:
                return (self,)

            elif self.stop <= other.stop:  # Covered by other
                return (self,)

            elif self.stop > other.stop:
                return (Dimension(self.start, other.stop),
                        Dimension(other.stop + 1, self.stop))

    def __str__(self) -> str:
        return f"{self.start}..{self.stop}"

    def __len__(self) -> int:
        return self.stop - (self.start - 1)  # Inclusive range

    def __contains__(self, other) -> bool:
        if isinstance(other, Dimension):

            return (self.start <= other.start) and (self.stop >= other.stop)

        return (self.start <= other) and (self.stop >= other)

    def touches(self, other) -> bool:
        return (
            (self.start >= other.start and self.start <= other.stop)
            or (self.stop >= other.start and self.stop <= other.stop)
            or (other.start >= self.start and other.start <= self.stop))



@dataclass(frozen=True)
class Position:
    x: int
    y: int
    z: int

    def distance_cubed(self) -> int:
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y, self.z - other.z)


class Cuboid:
    x: Optional[Dimension]
    y: Optional[Dimension]
    z: Optional[Dimension]

    def __init__(self, x: Dimension, y: Dimension, z: Dimension) -> None:
        self.x: Dimension = x
        self.y: Dimension = y
        self.z: Dimension = z

        self.sphere_size_cubed = math.ceil(len(x) ** 2 + len(y) ** 2 + len(z) ** 2 / 2)
        self.center = Position(
            x.start + len(x) // 2,
            y.start + len(y) // 2,
            z.start + len(z) // 2,
        )

    def subtract(self, other: "Cuboid") -> Optional[Iterable["Cuboid"]]:
        #if (self.center - other.center).distance_cubed() > (
        #    self.sphere_size_cubed + other.sphere_size_cubed
        #):
        #    return (self,)

        if not self.touches(other):
            return [self,]

        x_dimension = self.x.cut(other.x)
        #print(x_dimension, self.x)
        y_dimension = self.y.cut(other.y)
        #print(y_dimension, self.y)
        z_dimension = self.z.cut(other.z)
        #print(z_dimension, self.z)

        new_cubes = [
            Cuboid(*dimension)
            for dimension in itertools.product(x_dimension, y_dimension, z_dimension)
        ]
        new_cubes = [cube for cube in new_cubes if cube not in other]

        return new_cubes

    def touches(self, other) -> bool:

        return self.x.touches(other.x) and self.y.touches(other.y) and self.z.touches(other.z)

    @property
    def dimensions(self):
        return (self.x, self.y, self.z)

    @property
    def volume(self) -> int:
        return len(self.x) * len(self.y) * len(self.z)

    def __contains__(self, other: "Cuboid") -> bool:
        return other.x in self.x and other.y in self.y and other.z in self.z

    def __repr__(self) -> str:
        return f"<x:{self.x},y:{self.y},z:{self.z}>"

    def __format__(self, format_str: str) -> str:

        return f"{repr(self) :{format_str.strip()}}"

    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)


def plot_cubes(cubes: Iterable) -> None:
    if pyplot is None:
        return

    figure = pyplot.figure()
    axis = pyplot.axes(projection="3d")

    position_vectors = [
        [axis.start for axis in (cube.x, cube.y, cube.z)] for cube in cubes
    ]
    size_vectors = [
        [abs(axis.stop - axis.start) for axis in (cube.x, cube.y, cube.z)]
        for cube in cubes
    ]

    for pos, size in zip(position_vectors, size_vectors):
        axis.bar3d(*pos, *size)

    pyplot.show()


def main() -> None:
    from pprint import pprint

    cubes = []
    for line in sys.stdin.readlines():
        operation, coordinates = line.strip().split(" ")
        operation_cubes = [Cuboid(
            *(
                Dimension(*(int(v) for v in axis_range[2:].split("..")))
                for axis_range in coordinates.split(",")
            )
        )]

        if operation == "on":
            for cube in cubes:
                operation_cubes = list(
                    itertools.chain(
                        *filter(None, (operation_cube.subtract(cube) for operation_cube in operation_cubes))
                    )
                )

                overlapping = [(a, b) for a, b in itertools.combinations(operation_cubes, 2) if a.touches(b)]
                if any(a in b for a, b in itertools.product(operation_cubes, cubes)):
                    print("-----------Broken cut algorithm")
                    break

                if overlapping:
                    pprint(overlapping)
                    break

            print(f"adding {len(operation_cubes)}")
            cubes.extend(operation_cubes)

        else:
            cubes = list(
                itertools.chain(
                    *filter(None, (cube.subtract(operation_cubes[0]) for cube in cubes))
                )
            )

        # Overlap?
        overlapping = [(a, b) for a, b in itertools.combinations(cubes, 2) if a.touches(b)]
        print(f"{operation : >3} | {len(cubes) : >6} | {len(overlapping)} | {sum(c.volume for c in cubes) : >18}")
        if overlapping:
            plot_cubes(itertools.chain(*overlapping))
            pprint(overlapping)
            break

        plot_cubes(cubes)
        # Consolidation?



if __name__ == "__main__":
    main()


class TestDimensionCut(unittest.TestCase): # {{{
    def test_other_after_self_should_return_self(self):
        # Given
        dimension = Dimension(0, 3)
        other = Dimension(10, 25)

        # When
        result = dimension.cut(other)

        # Then
        expected = (Dimension(0, 3),)
        self.assertEqual(expected, result)

    def test_other_before_self_should_return_self(self):
        # Given
        dimension = Dimension(0, 3)
        other = Dimension(-4, -1)

        # When
        result = dimension.cut(other)

        # Then
        expected = (Dimension(0, 3),)
        self.assertEqual(expected, result)

    def test_other_covers_end_of_self_should_return_beginning_and_end(self):
        # Given
        dimension = Dimension(0, 5)
        other = Dimension(4, 6)

        # When
        result = dimension.cut(other)

        # Then
        expected = (Dimension(0, 3), Dimension(4, 5))
        self.assertEqual(expected, result)

    def test_other_cuts_middle_of_self_should_return_three_dimensions(self):
        # Given
        dimension = Dimension(0, 6)
        other = Dimension(3, 4)

        # When
        result = dimension.cut(other)

        # Then
        expected = (Dimension(0, 2), Dimension(3, 4), Dimension(5, 6))
        self.assertEqual(expected, result)

    def test_other_covers_beginning_of_self_should_return_beginning_and_end(self):
        # Given
        dimension = Dimension(0, 6)
        other = Dimension(-3, 3)

        # When
        result = dimension.cut(other)

        # Then
        expected = (Dimension(0, 3), Dimension(4, 6))
        self.assertEqual(expected, result)

    def test_other_covers_self_should_return_self(self):
        # Given
        dimension = Dimension(0, 3)
        other = Dimension(0, 3)

        # When
        result = dimension.cut(other)

        # Then
        expected = (Dimension(0, 3),)
        self.assertEqual(expected, result)

# }}}

class TestCuboidSubtract(unittest.TestCase):  # {{{

    def test_no_overlap_should_not_change_self(self):
        # Given
        cube = Cuboid(Dimension(0, 1), Dimension(0, 1), Dimension(0, 1))
        other = Cuboid(Dimension(2, 3), Dimension(2, 3), Dimension(2, 3))

        # When
        result = cube.subtract(other)

        # Then
        expected = [
            Cuboid(Dimension(0, 1), Dimension(0, 1), Dimension(0, 1)),
        ]
        self.assertEqual(expected, result)

    def test_total_overlap_should_return_empty(self):
        # Given
        cube = Cuboid(Dimension(0, 1), Dimension(0, 1), Dimension(0, 1))
        other = Cuboid(Dimension(0, 1), Dimension(0, 1), Dimension(0, 1))

        # When
        result = cube.subtract(other)

        # Then
        expected = []
        self.assertEqual(expected, result)

    def test_half_overlap_should_return_half_self(self):
        # Given
        cube = Cuboid(Dimension(0, 1), Dimension(0, 1), Dimension(0, 1))
        other = Cuboid(Dimension(0, 0), Dimension(0, 1), Dimension(0, 1))

        # When
        result = cube.subtract(other)

        # Then
        expected = [
            Cuboid(Dimension(1, 1), Dimension(0, 1), Dimension(0, 1)),
        ]
        self.assertEqual(expected, result)

    def test_quarter_overlap_should_return_three_quarters_self(self):
        # Given
        cube = Cuboid(Dimension(0, 1), Dimension(0, 1), Dimension(0, 1))
        other = Cuboid(Dimension(0, 0), Dimension(0, 0), Dimension(0, 1))

        # When
        result = cube.subtract(other)

        # Then
        expected = [
            Cuboid(Dimension(0, 0), Dimension(1, 1), Dimension(0, 1)),
            Cuboid(Dimension(1, 1), Dimension(0, 0), Dimension(0, 1)),
            Cuboid(Dimension(1, 1), Dimension(1, 1), Dimension(0, 1)),
        ]
        self.assertEqual(expected, result)

    def test_quadrant_overlap_should_return_seven_quarters_self(self):
        # Given
        cube = Cuboid(Dimension(0, 1), Dimension(0, 1), Dimension(0, 1))
        other = Cuboid(Dimension(0, 0), Dimension(0, 0), Dimension(0, 0))

        # When
        result = cube.subtract(other)

        # Then
        expected = [
            Cuboid(Dimension(0, 0), Dimension(0, 0), Dimension(1, 1)),
            Cuboid(Dimension(0, 0), Dimension(1, 1), Dimension(0, 0)),
            Cuboid(Dimension(0, 0), Dimension(1, 1), Dimension(1, 1)),
            Cuboid(Dimension(1, 1), Dimension(0, 0), Dimension(0, 0)),
            Cuboid(Dimension(1, 1), Dimension(0, 0), Dimension(1, 1)),
            Cuboid(Dimension(1, 1), Dimension(1, 1), Dimension(0, 0)),
            Cuboid(Dimension(1, 1), Dimension(1, 1), Dimension(1, 1)),
        ]
        self.assertEqual(expected, result)

# }}}
