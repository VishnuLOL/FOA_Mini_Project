import random
import numpy as np
import matplotlib.pyplot as plt
from algos import astar, bfs, dfs
from map_generator import generate_map
from visualization import display_path

def main():
    rows, cols = 10, 10
    grid = generate_map(rows, cols)
    start = (0, 0)
    goal = (9, 9)

    algorithm=input("Enter algorithm (astar/dfs/bfs) : ")

    if algorithm.lower() == 'astar':
        path = astar(grid, start, goal)
    elif algorithm.lower() == 'bfs':
        path = bfs(grid, start, goal)
    elif algorithm.lower() == 'dfs':
        path = dfs(grid, start, goal)

    if path:
        print(f"Path found using {algorithm}: {path}")
        display_path(grid, path, title=f"{algorithm.upper()} Path")
    else:
        print(f"No path found using {algorithm}.")

if __name__ == "__main__":
    main()
