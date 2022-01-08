#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import sys

from instructions import chunked_evaluation, python_from_instructions


def main() -> None:
    python_strings = python_from_instructions(sys.stdin.readlines())
    python_chunks = [eval("lambda i0, z:" + lambda_code) for lambda_code in python_strings]

    print(chunked_evaluation(python_chunks, iteration_order=list(range(9, 0, -1)), position=0))


if __name__ == "__main__":
    main()
