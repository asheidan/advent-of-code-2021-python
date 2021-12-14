#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
"""Perform 40 rounds of insertion.

Since the polymer grows exponentially the naive approach of A can't be used
since it will just take too much time.

Recursive?
"""

import itertools
import math
import sys
from datetime import datetime
from collections import defaultdict
from pprint import pprint
from typing import Dict, Iterable, List, TypeVar, Tuple

T = TypeVar("T")


def progress(iterable: Iterable[T]) -> Iterable[T]:
    start = datetime.now()
    for element in iterable:
        print((datetime.now() - start), file=sys.stderr)
        yield element


def c_to_i(char: str) -> int:
    return ord(char) - ord("A")


RULES = {}
COMPUTE_CACHE: Dict[Tuple[str, int], int] = {}


def expand(first: str, second: str, steps: int) -> List[int]:
    key = "".join((first, second))

    if steps > 10 and (key, steps) in COMPUTE_CACHE:
        return COMPUTE_CACHE[(key, steps)]

    element_count = [0] * 26
    inserted_element = RULES[key]
    element_count[c_to_i(inserted_element)] += 1

    if steps == 1:
        # print(" " * (steps - 1), inserted_element)
        return element_count

    left_tree = expand(
        first=first,
        second=inserted_element,
        steps=(steps - 1),
    )

    # print(" " * (steps - 1), inserted_element)

    right_tree = expand(
        first=inserted_element,
        second=second,
        steps=(steps - 1),
    )

    element_count = list(map(sum, zip(element_count, left_tree, right_tree)))

    if steps > 10 :
        COMPUTE_CACHE[(key, steps)] = element_count

    return element_count


def evolve(polymer: Iterable[str], steps: int = 1) -> List[int]:
    result = [0] * 26

    iterator = iter(polymer)
    first = next(iterator)
    result[c_to_i(first)] += 1
    print(first)
    for second in progress(iterator):
        result[c_to_i(second)] += 1

        sub_tree = expand(first, second, steps=steps)
        result = list(map(sum, zip(result, sub_tree)))

        print(second)
        first = second

    return result


def print_element_count(element_count: List[int]) -> None:
    max_width = math.ceil(math.log10(max(element_count)))
    start = ord("A")
    for index, count in enumerate(element_count):
        display = count or " "
        print(f"{chr(start + index): >2} | {display : >{max_width}}")


def main() -> None:
    global RULES

    template, rule_lines = sys.stdin.read().strip().split("\n\n")
    RULES = {
        key: value
        for key, value in map(lambda s: s.split(" -> "), rule_lines.split("\n"))
    }

    print(template)
    polymer = list(template)

    element_count = evolve(polymer=polymer, steps=40)
    print_element_count(element_count)

    max_count = max(element_count)
    min_count = min(filter(None, element_count))

    print(f"{max_count : 5} | {min_count : 5} | {max_count - min_count : 5} | ({len(COMPUTE_CACHE)})")


if __name__ == "__main__":
    main()
