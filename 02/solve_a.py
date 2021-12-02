#!/usr/bin/env python

import sys
from pprint import pprint

position = {
    "forward": 0,
    "down": 0,
    "up": 0,
}

for line in sys.stdin:
    direction, value = line.split()

    position[direction] += int(value)

pprint(position)

print(position["forward"], position["down"] - position["up"])
print(position["forward"] * (position["down"] - position["up"]))
