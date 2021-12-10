#!/usr/bin/env python3

import sys
from typing import List


def validate_line(line: str) -> int:
    """Return score/error code for line.
    """
    stack: List[str] = []
    valid_openings = "([{<"

    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    C = {k: v for k, v in ["()", "[]", "{}", "<>"]}

    for c in line.strip():
        if c in valid_openings:
            stack.append(c)

            continue

        if stack and c == C[stack.pop()]:

            continue

        return scores[c]

    return 0


def main() -> None:
    print(sum(map(validate_line, sys.stdin)))


if __name__ == "__main__":
    main()
