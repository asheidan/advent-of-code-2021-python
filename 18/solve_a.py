#!/usr/bin/env python3.10
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import math
import sys
import unittest
from typing import Tuple, Union

from snailfish_numbers import number_from_string, add, reduce, magnitude


def main() -> None:
    numbers = map(number_from_string, sys.stdin.readlines())
    
    result = next(numbers)
    result = reduce(result)

    for i, number in enumerate(numbers):
        print(i, number)

        result = add(result, number)
        print(i, result)

        result = reduce(result)
        print(i, result)

    print(result)
    print(magnitude(result))


if __name__ == "__main__":
    main()