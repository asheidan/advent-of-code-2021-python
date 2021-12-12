#!/usr/bin/env python3
# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring
import sys
from collections import defaultdict
from pprint import pprint
from typing import Dict, List

Graph = Dict[str, List[str]]


def is_big_cave(name: str) -> bool:
    return name.upper() == name


def explore(
    node_name: str, graph: Graph, visited_nodes: frozenset = frozenset(), level: int = 0,
) -> int:
    print(f"{'  ' * level} {node_name}")

    if node_name == "end":
        return 1

    if not is_big_cave(node_name):
        visited_nodes = visited_nodes | frozenset((node_name,))

    # pprint(visited_nodes)

    return sum(
        explore(destination, graph=graph, visited_nodes=visited_nodes, level=level + 1)
        for destination in graph[node_name]
        if destination not in visited_nodes
    )


def main() -> None:
    graph = defaultdict(list)

    for line in sys.stdin:
        start, end = line.strip().split("-")
        graph[start].append(end)
        graph[end].append(start)

    pprint(graph)
    print(explore("start", graph=graph))


if __name__ == "__main__":
    main()
