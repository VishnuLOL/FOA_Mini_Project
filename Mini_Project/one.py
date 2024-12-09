import heapq
import random
import matplotlib.pyplot as plt
import numpy as np



# Directions for moving (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movement directions: up, down, left, right

# Heuristic function for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance: abs(x1 - x2) + abs(y1 - y2)

# A* Algorithm for pathfinding
def astar(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), start))
    
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, goal)}
    came_from = {}

    while open_list:
        current_f, current = heapq.heappop(open_list)
        
        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        current_x, current_y = current
        
        for dx, dy in DIRECTIONS:
            neighbor = (current_x + dx, current_y + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != 3:
                tentative_g_cost = g_cost[current] + 1
                
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g_cost
                    f_cost[neighbor] = tentative_g_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost[neighbor], neighbor))

    return None

# BFS Algorithm for pathfinding
from collections import deque

def bfs(grid, start, goal):
    queue = deque([start])  # Use deque for O(1) pops from front
    visited = set([start])  # Start node is visited
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != 3 and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current
    return None

# DFS Algorithm for pathfinding
def dfs(grid, start, goal):
    stack = [start]
    visited = set([start])  # Start node is visited
    came_from = {start: None}

    while stack:
        current = stack.pop()
        
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != 3 and neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                came_from[neighbor] = current
    return None



def generate_map(rows, cols, probabilities=None):
    """
    Generate a grid map with specific probabilities for different cell types.
    Args:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        probabilities (dict): Probabilities for each cell type.

    Returns:
        list of lists: Generated grid map.
    """
    if probabilities is None:
        # Default probabilities for less obstruction and heavy traffic
        probabilities = {0: 0.85, 1: 0.1, 2: 0.04, 3: 0.01}

    grid = []
    cell_types = list(probabilities.keys())
    weights = list(probabilities.values())

    for _ in range(rows):
        grid.append([random.choices(cell_types, weights)[0] for _ in range(cols)])

    return grid



def display_path(grid, path, title="Path Visualization"):
    """
    Visualize the path on a white background grid with centered blue dots.
    Args:
        grid (list of lists): The grid with costs or obstacles.
        path (list of tuples): The path to visualize.
        title (str): The title of the plot.
    """
    # Convert grid to numpy array for easier handling
    grid_array = np.array(grid)

    # Create a custom color map for a white background
    colors = {
        0: "white",  # Free cell
        1: "lightgray",  # Light traffic
        2: "gray",  # Heavy traffic
        3: "black"  # Obstruction
    }

    # Build a grid of colors
    color_grid = np.empty(grid_array.shape, dtype="object")
    for key, color in colors.items():
        color_grid[grid_array == key] = color

    # Create the figure and axes
    fig, ax = plt.subplots()
    for (i, row) in enumerate(color_grid):
        for (j, cell_color) in enumerate(row):
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=cell_color))

    # Overlay the path as blue dots at the center of each cell
    if path:
        x_coords = [p[1] + 0.5 for p in path]  # Center x-coordinates
        y_coords = [p[0] + 0.5 for p in path]  # Center y-coordinates
        ax.scatter(x_coords, y_coords, c='blue', s=50, zorder=5)  # Blue dots

    # Configure gridlines and labels
    ax.set_xlim(0, grid_array.shape[1])
    ax.set_ylim(grid_array.shape[0], 0)
    ax.set_xticks(np.arange(0, grid_array.shape[1], 1))
    ax.set_yticks(np.arange(0, grid_array.shape[0], 1))
    ax.grid(color="black", linestyle='-', linewidth=0.5)

    # Remove tick labels for a cleaner look
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # Add the title
    ax.set_title(title)

    # Display the plot
    plt.show()




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
