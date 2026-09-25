# algorithms/astar.py
import heapq
from typing import List, Tuple, Optional, Dict
from utils.grid import Grid, Pos
import math

def manhattan(a: Pos, b: Pos) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid: Grid, start: Pos, goal: Pos) -> Tuple[List[Pos], Optional[List[Pos]]]:
    """
    A* using g + h (manhattan heuristic). Returns visited order and path.
    """
    if start == goal:
        return [start], [start]

    open_heap = []
    heapq.heappush(open_heap, (0 + manhattan(start, goal), 0, start))  # (f, g, pos)
    came_from: Dict[Pos, Pos | None] = {start: None}
    g_score: Dict[Pos, float] = {start: 0}
    visited_order = []
    closed = set()

    while open_heap:
        _, current_g, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        closed.add(current)
        visited_order.append(current)

        if current == goal:
            # reconstruct
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return visited_order, path

        for neighbor in grid.neighbors(current, allow_diagonal=False):
            tentative_g = current_g + grid.cost(current, neighbor)
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_heap, (f, tentative_g, neighbor))

    return visited_order, None
