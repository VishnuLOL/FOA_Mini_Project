import matplotlib.pyplot as plt
import numpy as np

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
