#!/usr/bin/env python3.10
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import itertools
import sys

from snailfish_numbers import number_from_string, add, reduce, magnitude


def main() -> None:
    numbers = list(map(number_from_string, sys.stdin.readlines()))

    
    max_sum = 0
    for first, second in itertools.product(numbers, numbers):

        added = add(first, second)
        reduced = reduce(added)
        result = magnitude(reduced)
        #print(f"{result : >4} | {reduced}")
        max_sum = max(max_sum, result)

    print(max_sum)



if __name__ == "__main__":
    main()