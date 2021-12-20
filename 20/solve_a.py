#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
"""Image enhancement.

Assuming square images.
Fake unlimited canvas by assuming it's enough to pad quite a lot and wrap around
"""

import sys
import unittest


def image_region(image: str, image_width: int, x: int, y: int) -> int:

    result = 0

    # NOTE: We are dealing with an image containing newlines.
    #       That's why each line is image_width + 1.

    image_size = range(image_width)

    # First row
    for row in range(y - 1, y + 2):
        for column in range(x - 1, x + 2):
            result <<= 1
            result += int(
                (row in image_size)
                and (column in image_size)
                and (image[(image_width + 1) * row + column] == "#")
            )

    return result


def enhance(image: str, algorithm: str) -> str:
    image_width = image.find("\n")

    new_image = "\n".join(
        "".join(
            algorithm[image_region(image, image_width, x, y)]
            for x in range(-1, image_width + 1)
        )
        for y in range(-1, round(len(image) / (image_width + 1)) + 1)
    )

    return new_image


def main() -> None:
    algorithm, image = sys.stdin.read().strip().split("\n\n")
    print(image)
    algorithm = algorithm.replace("\n", "")
    print(repr(algorithm))

    for round in range(1, 1 + 1):
        image = enhance(image, algorithm)
        print(f"--- {round} ---")
        if len(image) < 100:
            print(image)

    print(image.count("#"))



if __name__ == "__main__":
    main()


class TestImageRegion(unittest.TestCase):
    def test_middle_picture_all_dark(self):
        # Given
        image = "...\n" * 3
        image_width = 3

        # When
        result = image_region(image, image_width, x=1, y=1)

        # Then
        self.assertEqual(0, result)

    def test_middle_picture_single_light_sohuld_be_1(self):
        # Given
        image = "...\n" "...\n" "..#"
        image_width = 3

        # When
        result = image_region(image, image_width, x=1, y=1)

        # Then
        self.assertEqual(1, result)

    def test_middle_picture_single_center_light_should_be_16(self):
        # Given
        image = "...\n" ".#.\n" "..."
        image_width = 3

        # When
        result = image_region(image, image_width, x=1, y=1)

        # Then
        self.assertEqual(16, result)

    def test_right_of_picture_single_center_light_should_be_16(self):
        # Given
        image = "...\n" "..#\n" "..."
        image_width = 3

        # When
        result = image_region(image, image_width, x=2, y=1)

        # Then
        self.assertEqual(16, result)

    def test_left_of_picture_single_center_light_should_be_16(self):
        # Given
        image = "...\n" "#..\n" "..."
        image_width = 3

        # When
        result = image_region(image, image_width, x=0, y=1)

        # Then
        self.assertEqual(16, result)

    def test_above_picture_single_center_light_should_be_16(self):
        # Given
        image = "#..\n" "...\n" "..."
        image_width = 3

        # When
        result = image_region(image, image_width, x=0, y=0)

        # Then
        self.assertEqual(16, result)

    def test_below_picture_single_center_light_should_be_16(self):
        # Given
        image = "...\n" "...\n" "..#"
        image_width = 3

        # When
        result = image_region(image, image_width, x=2, y=2)

        # Then
        self.assertEqual(16, result)
