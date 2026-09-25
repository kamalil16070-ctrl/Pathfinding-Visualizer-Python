# algorithms/bfs.py
from collections import deque
from typing import List, Tuple, Optional
from utils.grid import Grid, Pos

def bfs(grid: Grid, start: Pos, goal: Pos) -> Tuple[List[Pos], Optional[List[Pos]]]:
    """
    Returns (visited_order, path) where visited_order is list of nodes in order visited,
    path is list from start->goal (or None if no path).
    """
    if start == goal:
        return [start], [start]

    frontier = deque([start])
    came_from = {start: None}
    visited_order = []

    while frontier:
        current = frontier.popleft()
        visited_order.append(current)

        if current == goal:
            # reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return visited_order, path

        for neighbor in grid.neighbors(current, allow_diagonal=False):
            if neighbor not in came_from:
                came_from[neighbor] = current
                frontier.append(neighbor)

    return visited_order, None
