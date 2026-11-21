import heapq
from itertools import count
from typing import Dict

from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Calcula a distância Manhattan de cada peça até sua posição objetivo."""

        distance = 0

        goal_positions = {
            tile: index
            for index, tile in enumerate(GOAL_STATE)
        }

        for current_index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            goal_index = goal_positions[tile]

            current_row, current_col = divmod(current_index, 3)
            goal_row, goal_col = divmod(goal_index, 3)

            distance += (
                abs(current_row - goal_row)
                + abs(current_col - goal_col)
            )

        return distance

    def search(self, initial: State) -> SearchResult:
        sequence = count()

        frontier = [
            (initial.cost + self.heuristic(initial), next(sequence), initial)
        ]

        best_cost: Dict[tuple, int] = {
            initial.tiles: initial.cost
        }

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current.cost != best_cost.get(current.tiles):
                continue

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
                previous_cost = best_cost.get(child.tiles)

                if previous_cost is not None and child.cost >= previous_cost:
                    continue

                best_cost[child.tiles] = child.cost

                priority = child.cost + self.heuristic(child)

                heapq.heappush(
                    frontier,
                    (priority, next(sequence), child)
                )

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )