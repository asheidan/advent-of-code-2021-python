#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
import sys
from collections import defaultdict
from pprint import pprint
from typing import Dict, List, Hashable, Iterable

Graph = Dict[str, List[str]]


def is_big_cave(name: str) -> bool:
    return name.upper() == name


class SpecialSet:
    """This allows a single element to exist twice."""

    def __init__(self, elements: Iterable = (), has_double_element: bool = False):
        self.has_double_element = has_double_element
        self.elements = frozenset(elements)

    def __contains__(self, element: Hashable) -> bool:
        return self.has_double_element and (element in self.elements)

    def add(self, element: Hashable) -> "SpecialSet":
        """Return a new immutable copy with the element added."""
        return SpecialSet(
            elements=(self.elements | frozenset((element,))),
            has_double_element=self.has_double_element or (element in self.elements),
        )

    def __str__(self) -> str:
        return f"{self.elements}[{self.has_double_element}]"


def explore(
    node_name: str,
    graph: Graph,
    visited_nodes: SpecialSet = SpecialSet(),
    level: int = 0,
) -> int:
    print(f"{'  ' * level} {node_name}")

    if node_name == "end":
        return 1

    if not is_big_cave(node_name):
        visited_nodes = visited_nodes.add(node_name)

    # print(f"{str(visited_nodes) : >100}")

    return sum(
        explore(
            node_name=destination,
            graph=graph,
            visited_nodes=visited_nodes,
            level=level + 1,
        )
        for destination in graph[node_name]
        if destination != "start" and destination not in visited_nodes
    )


def main() -> None:
    graph = defaultdict(list)

    for line in sys.stdin:
        start, end = line.strip().split("-")
        graph[start].append(end)
        graph[end].append(start)

    pprint(graph)
    print(explore("start", graph=graph), file=sys.stderr)


if __name__ == "__main__":
    main()
