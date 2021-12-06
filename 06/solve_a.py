#!/usr/bin/env python3

import math
import sys
import unittest
from typing import List
from typing import Tuple


Generation = List[int]
"""One position for each timer value, counter for number of fish with that timer value.
"""


def generation_from_string(string: str) -> Generation:
    """Return a Generation parsed from string."""
    generation = [0] * 9

    timers = [int(s) for s in string.strip().split(",") if s]
    # print(timers)
    for timer in timers:
        generation[timer] += 1

    return generation


def next_generation(generation: Generation) -> Generation:
    """Return the next generation given the parent generation."""
    # Shift timers and make sure theres always 9 elements
    birther_count, *new_generation = generation + [0]

    new_generation[6] += birther_count  # Reset timers of birthers
    new_generation[8] += birther_count  # Birth new fish

    return new_generation


def print_table_row(days: int, generation: Generation, output=sys.stdout) -> None:
    if not output.isatty():
        print(" ".join(map(str, generation)), file=output)

        return

    column_width = max(2, math.ceil(math.log10(max(generation))))

    timers = ", ".join(f"{count : >{column_width}}" for count in generation)
    school_size = sum(generation)

    print(f"{days : >3} | {timers} | {school_size : >{column_width + 1}} | {school_size : E}", file=output)


def main() -> None:
    generation = generation_from_string(sys.stdin.read())
    print_table_row(0, generation)
    for count in range(1, 256 + 1):
        generation = next_generation(generation)
        print_table_row(count, generation)


if __name__ == "__main__":
    main()


class TestGenerationFromString(unittest.TestCase):
    def test_empty_string_should_result_in_empty_generation(self):
        # Given
        string = ""

        # When
        result = generation_from_string(string)

        # Then
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(expected, result)

    def test_single_number_should_be_reflected_in_generation(self):
        # Given
        string = "8"

        # When
        result = generation_from_string(string)

        # Then
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.assertEqual(expected, result)

    def test_should_handle_example_input_correctly(self):
        # Given
        string = "3,4,3,1,2"

        # When
        result = generation_from_string(string)

        # Then
        expected = [0, 1, 1, 2, 1, 0, 0, 0, 0]
        self.assertEqual(expected, result)
