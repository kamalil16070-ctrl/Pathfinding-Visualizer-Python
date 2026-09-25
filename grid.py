# utils/grid.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Iterator, Set

Pos = Tuple[int, int]  # (row, col)


@dataclass
class Grid:
    rows: int
    cols: int
    walls: Set[Pos] | None = None
    weights: dict | None = None  # optional: {(r,c): cost}

    def __post_init__(self):
        self.walls = set(self.walls) if self.walls else set()
        self.weights = dict(self.weights) if self.weights else {}

    def in_bounds(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, pos: Pos) -> bool:
        return pos not in self.walls

    def neighbors(self, pos: Pos, allow_diagonal: bool = False) -> List[Pos]:
        (r, c) = pos
        results = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        if allow_diagonal:
            results += [(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
        # filter bounds & passable
        results = [p for p in results if self.in_bounds(p) and self.passable(p)]
        return results

    def cost(self, from_pos: Pos, to_pos: Pos) -> float:
        # default cost = 1; if diagonal movement, cost ~= 1.414
        if to_pos in self.weights:
            return self.weights[to_pos]
        if from_pos[0] != to_pos[0] and from_pos[1] != to_pos[1]:
            return 2 ** 0.5
        return 1.0

    def reset(self):
        self.walls.clear()
        self.weights.clear()


    
    