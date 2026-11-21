from collections import deque

from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        visited = {initial.tiles}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            current = frontier.popleft()

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.path()) - 1,
                )

            nodes_expanded += 1

            children = current.neighbors()
            nodes_generated += len(children)

            for child in children:
                if child.tiles not in visited:
                    visited.add(child.tiles)
                    frontier.append(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )