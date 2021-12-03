#!/usr/bin/env python

import sys
from pprint import pprint
from typing import List

# pylint: disable=missing-function-docstring


def list_as_dec(binary_list: List[int]) -> int:
    return int("0b" + "".join(map(str, binary_list)), base=2)


def list_as_str(binary_list: List[int]) -> str:
    return "0b" + "".join(map(str, binary_list))


def common(sum_for_position, linecount) -> int:
    return int(sum_for_position >= (linecount / 2))


def uncommon(sum_for_position, linecount) -> int:
    return int(sum_for_position < (linecount / 2))


def filtered_by_position(rows: List[List[int]], filter_function=common) -> List[int]:
    position = 0
    print(f"----------------------- | rows: {len(rows) : >5}")
    while len(rows) > 1:
        linecount = len(rows)

        sum_for_position = sum(row[position] for row in rows)
        target = filter_function(sum_for_position, linecount)
        rows = [row for row in rows if row[position] == target]
        # pprint(rows)
        print(f"p: {position : >2} | s: {sum_for_position: >5} | t: {target} | rows: {len(rows) : >5}")
        position += 1

    return rows[0]


def main() -> None:
    lines = sys.stdin.readlines()
    matrix = [list(map(int, line.strip())) for line in lines]
    # pprint(matrix)

    rows = matrix

    oxygen_rating = filtered_by_position(rows, common)
    pprint(oxygen_rating)
    pprint(list_as_str(oxygen_rating))
    print(list_as_dec(oxygen_rating))

    scrubber_rating = filtered_by_position(rows, uncommon)
    pprint(scrubber_rating)
    pprint(list_as_str(scrubber_rating))
    print(list_as_dec(scrubber_rating))

    print(list_as_dec(oxygen_rating) * list_as_dec(scrubber_rating))


if __name__ == "__main__":
    main()
