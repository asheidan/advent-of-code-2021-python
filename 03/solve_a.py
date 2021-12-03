#!/usr/bin/env python

import sys
from pprint import pprint
from typing import List

def list_as_dec(binary_list: List[int]) -> int:
    return int("0b" + "".join(map(str, binary_list)), base=2)


def main() -> None:
    lines = sys.stdin.readlines()
    line_count = len(lines)
    matrix = [list(map(int, line.strip())) for line in lines]
    # pprint(matrix)

    sums = [sum(column) for column in zip(*matrix)]
    pprint(sums)
    averages = [int(n > (line_count / 2)) for n in sums]
    pprint(averages)

    gamma_rate = list_as_dec(averages)
    pprint(gamma_rate)
    sigma_rate = list_as_dec(int(not n) for n in averages)
    pprint(sigma_rate)

    print(gamma_rate * sigma_rate)


if __name__ == "__main__":
    main()
