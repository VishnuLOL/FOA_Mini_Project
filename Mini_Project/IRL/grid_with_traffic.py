from irl_traffic import get_traffic_data_for_cell

def adjust_grid_with_traffic(grid, traffic_data):
    """
    Adjust grid weights based on real-time traffic data.
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # Assuming traffic_data provides congestion information for each road
            congestion_level = get_traffic_data_for_cell(i, j, traffic_data)  # Custom function to map traffic data to grid cell
            
            # Adjust grid weight based on congestion level
            if congestion_level == "Light":
                grid[i][j] = 1  # Low cost
            elif congestion_level == "Moderate":
                grid[i][j] = 2  # Medium cost
            elif congestion_level == "Heavy":
                grid[i][j] = 5  # High cost
    return grid
