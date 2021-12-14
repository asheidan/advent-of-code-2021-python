#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
"""Perform 10 rounds of insertion."""

import sys
from collections import defaultdict


def main() -> None:
    template, rule_lines = sys.stdin.read().strip().split("\n\n")
    rules = {
        key: value
        for key, value in map(lambda s: s.split(" -> "), rule_lines.split("\n"))
    }

    print(template)
    polymer = list(template)

    for _round in range(10):
        insertions = [
            (i, rules["".join(polymer[i : i + 2])]) for i in range(len(polymer) - 1)
        ]
        insertions.reverse()
        # print(insertions)

        for index, element in insertions:
            polymer.insert(index + 1, element)

        # print("".join(polymer))
    
    element_count = defaultdict(int)
    for element in polymer:
        element_count[element] += 1

    max_count = max(element_count.values())
    min_count = min(element_count.values())

    print(f"{max_count : 5} | {min_count : 5} | {max_count - min_count : 5}")


if __name__ == "__main__":
    main()
