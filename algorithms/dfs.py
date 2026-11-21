from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        best_depth = {initial.tiles: initial.cost}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            current = frontier.pop()

            if current.cost != best_depth.get(current.tiles):
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.path()) - 1,
                )

            current_depth = current.cost - initial.cost

            if current_depth >= self.depth_limit:
                continue

            nodes_expanded += 1

            children = current.neighbors()
            nodes_generated += len(children)

            for child in children:
                child_depth = child.cost - initial.cost

                if child_depth > self.depth_limit:
                    continue

                previous_depth = best_depth.get(child.tiles)

                if previous_depth is not None and child.cost >= previous_depth:
                    continue

                best_depth[child.tiles] = child.cost
                frontier.append(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )