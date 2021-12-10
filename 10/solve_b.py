#!/usr/bin/env python3

import sys
from typing import List
from functools import reduce
from pprint import pprint


def validate_line(line: str) -> int:
    """Return score/error code for line.
    """
    stack: List[str] = []
    valid_openings = "([{<"

    scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    C = {k: v for k, v in ["()", "[]", "{}", "<>"]}

    for c in line.strip():
        if c in valid_openings:
            stack.append(c)

            continue

        if stack and c == C[stack.pop()]:

            continue

        return 0

    return reduce((lambda acc, e: acc * 5 + scores[C[e]]), reversed(stack), 0)


def main() -> None:
    scores = sorted(filter(None, map(validate_line, sys.stdin)))
    print(scores[len(scores) // 2])


if __name__ == "__main__":
    main()
