import folium
from irl_traffic import get_traffic_data
from grid_with_traffic import adjust_grid_with_traffic
from astar_with_traffic import astar_with_traffic as astar

def plot_route_on_map(start, goal, path):
    """
    Plot the start, goal, and path on a map using folium.
    """
    # Create a map centered at the starting point
    map_ = folium.Map(location=start, zoom_start=13)

    # Add markers for start and goal points
    folium.Marker(start, popup="Start", icon=folium.Icon(color='green')).add_to(map_)
    folium.Marker(goal, popup="Goal", icon=folium.Icon(color='red')).add_to(map_)
    
    # Add the route as a polyline
    path_coords = [start] + path + [goal]
    folium.PolyLine(path_coords, color='blue', weight=4, opacity=0.7).add_to(map_)
    
    # Save map to an HTML file
    map_.save("route_map.html")
    print("Map saved as 'route_map.html'. Open this file in your browser.")

def main():
    # Set the start and goal locations (latitude, longitude)
    start = (9.093898, 76.491927)  # Example starting coordinates
    goal = (9.172815, 76.497715)   # Example goal coordinates
    
    # Create a grid (you can adjust this grid size based on your needs)
    grid = [[0 for _ in range(10)] for _ in range(10)]
    
    # Get real-time traffic data for the start and goal (or adjust for the entire area)
    traffic_data = get_traffic_data("9.093898,76.491927", "9.172815,76.497715")
    print(traffic_data)
    # Handle case where traffic data is None
    if not traffic_data:
        print("Failed to retrieve traffic data. Exiting.")
        return
    
    # Adjust the grid based on the traffic data
    grid = adjust_grid_with_traffic(grid, traffic_data)
    
    # Use A* algorithm to find the path, passing the traffic data as well
    path = astar(grid, start, goal, traffic_data)  # Include traffic_data
    
    if path:
        print("Path found:", path)
        # Plot the route on a map
        plot_route_on_map(start, goal, path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
