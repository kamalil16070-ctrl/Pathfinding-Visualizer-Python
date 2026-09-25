# algorithms/dfs.py
from typing import List, Tuple, Optional
from utils.grid import Grid, Pos

def dfs(grid: Grid, start: Pos, goal: Pos) -> Tuple[List[Pos], Optional[List[Pos]]]:
    """
    Iterative DFS (stack). Returns visited order and path if found.
    """
    if start == goal:
        return [start], [start]

    stack = [start]
    came_from = {start: None}
    visited_order = []

    while stack:
        current = stack.pop()
        if current in visited_order:
            continue
        visited_order.append(current)

        if current == goal:
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
                stack.append(neighbor)

    return visited_order, None
