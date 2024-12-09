import random

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
