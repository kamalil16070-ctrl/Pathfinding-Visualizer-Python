# main.py
import pygame
import sys
import time
from typing import Tuple, Optional, List
from utils.grid import Grid, Pos
from algorithms import bfs, dfs, astar, greedy

# CONFIG
ROWS = 30
COLS = 30
CELL_SIZE = 20  # pixels
MARGIN = 2
WINDOW_W = COLS * CELL_SIZE + 300  # extra for sidebar
WINDOW_H = ROWS * CELL_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREY = (200, 200, 200)
WALL_COLOR = (30, 30, 60)
START_COLOR = (40, 200, 40)
TARGET_COLOR = (200, 40, 40)
VISITED_COLOR = (100, 180, 255)
FRONTIER_COLOR = (255, 200, 80)
PATH_COLOR = (255, 240, 100)
BG = (245, 245, 245)
TEXT_COLOR = (30, 30, 30)

# Helpers
def grid_to_rect(r: int, c: int) -> pygame.Rect:
    x = c * CELL_SIZE
    y = r * CELL_SIZE
    return pygame.Rect(x, y, CELL_SIZE - 1, CELL_SIZE - 1)

def draw_text(surface, text, pos, font, color=TEXT_COLOR):
    surface.blit(font.render(text, True, color), pos)

def run_algorithm_and_animate(screen, clock, grid: Grid, start: Pos, target: Pos, algorithm_name: str, font):
    alg_map = {
        "BFS": bfs.bfs,
        "DFS": dfs.dfs,
        "A*": astar.astar,
        "Greedy": greedy.greedy_best_first
    }
    alg = alg_map.get(algorithm_name)
    if alg is None:
        return

    visited, path = alg(grid, start, target)
    # animate visited
    for i, node in enumerate(visited):
        r, c = node
        pygame.draw.rect(screen, VISITED_COLOR, grid_to_rect(r, c))
        pygame.display.flip()
        clock.tick(240)  # speed of visiting (you can throttle)
    # animate path
    if path:
        for node in path:
            r, c = node
            pygame.draw.rect(screen, PATH_COLOR, grid_to_rect(r, c))
            pygame.display.flip()
            clock.tick(240)
    else:
        # flash message for no path
        draw_text(screen, "No path found", (COLS * CELL_SIZE + 20, 200), font, (180, 30, 30))
        pygame.display.flip()
        pygame.time.delay(700)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Pathfinding Visualizer (Pygame)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    big_font = pygame.font.SysFont("Arial", 20, bold=True)

    grid = Grid(ROWS, COLS)
    start: Optional[Pos] = None
    target: Optional[Pos] = None
    drawing = False  # left mouse drag for walls
    erasing = False  # right mouse to erase
    mode = "wall"  # or 'set_start' or 'set_target'
    current_algorithm = "BFS"

    running = True
    while running:
        screen.fill(BG)
        # draw grid cells
        for r in range(ROWS):
            for c in range(COLS):
                rect = grid_to_rect(r, c)
                pos = (r, c)
                if pos in grid.walls:
                    color = WALL_COLOR
                elif start is not None and pos == start:
                    color = START_COLOR
                elif target is not None and pos == target:
                    color = TARGET_COLOR
                else:
                    color = WHITE
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GREY, rect, 1)

        # sidebar
        sidebar_x = COLS * CELL_SIZE + 10
        draw_text(screen, "Controls:", (sidebar_x, 10), big_font)
        draw_text(screen, "Left drag: draw walls", (sidebar_x, 40), font)
        draw_text(screen, "Right click drag: erase walls", (sidebar_x, 60), font)
        draw_text(screen, "S: set Start (press S then click cell)", (sidebar_x, 90), font)
        draw_text(screen, "T: set Target (press T then click cell)", (sidebar_x, 110), font)
        draw_text(screen, "C: clear walls", (sidebar_x, 140), font)
        draw_text(screen, "R: reset (clear start/target/walls)", (sidebar_x, 160), font)
        draw_text(screen, "1: BFS  2: DFS  3: A*  4: Greedy", (sidebar_x, 190), font)
        draw_text(screen, f"Algorithm: {current_algorithm}", (sidebar_x, 230), font)
        draw_text(screen, "Space: Run algorithm", (sidebar_x, 260), font)
        draw_text(screen, "Esc: Quit", (sidebar_x, 290), font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx < COLS * CELL_SIZE and my < ROWS * CELL_SIZE:
                    cell_r = my // CELL_SIZE
                    cell_c = mx // CELL_SIZE
                    pos = (cell_r, cell_c)
                    if event.button == 1:  # left click
                        if mode == "set_start":
                            start = pos
                            mode = "wall"
                        elif mode == "set_target":
                            target = pos
                            mode = "wall"
                        else:
                            drawing = True
                            # toggle wall on click
                            if pos in grid.walls:
                                grid.walls.remove(pos)
                            else:
                                # avoid making start/target walls
                                if pos != start and pos != target:
                                    grid.walls.add(pos)
                    elif event.button == 3:  # right click -> erase
                        erasing = True
                        if pos in grid.walls:
                            grid.walls.remove(pos)

            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if mx < COLS * CELL_SIZE and my < ROWS * CELL_SIZE:
                    cell_r = my // CELL_SIZE
                    cell_c = mx // CELL_SIZE
                    pos = (cell_r, cell_c)
                    if drawing:
                        if pos != start and pos != target:
                            grid.walls.add(pos)
                    if erasing:
                        if pos in grid.walls:
                            grid.walls.remove(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                if event.button == 3:
                    erasing = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    mode = "set_start"
                elif event.key == pygame.K_t:
                    mode = "set_target"
                elif event.key == pygame.K_c:
                    grid.walls.clear()
                elif event.key == pygame.K_r:
                    grid.walls.clear()
                    start = None
                    target = None
                elif event.key == pygame.K_1:
                    current_algorithm = "BFS"
                elif event.key == pygame.K_2:
                    current_algorithm = "DFS"
                elif event.key == pygame.K_3:
                    current_algorithm = "A*"
                elif event.key == pygame.K_4:
                    current_algorithm = "Greedy"
                elif event.key == pygame.K_SPACE:
                    if start is None or target is None:
                        # message: need start & target
                        draw_text(screen, "Place start (S) and target (T) first", (sidebar_x, 320), font, (180, 30, 30))
                        pygame.display.flip()
                        pygame.time.delay(700)
                    else:
                        # run selected algorithm and animate
                        run_algorithm_and_animate(screen, clock, grid, start, target, current_algorithm, font)

        # small indicator of current mode
        draw_text(screen, f"Mode: {mode}", (sidebar_x, 340), font)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
