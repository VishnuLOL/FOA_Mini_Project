from irl_traffic import get_traffic_data_for_cell
import heapq

# Directions for moving in grid (up, down, left, right, diagonals)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Including diagonals

def heuristic(a, b):
    """
    Heuristic function to calculate the Manhattan distance between two points.
    a and b are tuples (x, y).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

def astar_with_traffic(grid, start, goal, traffic_data):
    """
    A* algorithm considering traffic data for pathfinding.
    
    grid: 2D grid (list of lists) representing the environment
    start: tuple (x, y) representing the starting point
    goal: tuple (x, y) representing the goal point
    traffic_data: dictionary with traffic data for each grid cell
    
    Returns:
        path: List of tuples representing the path from start to goal, or None if no path exists
    """
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), start))  # Push starting point with priority
    
    g_cost = {start: 0}  # Dictionary to store the cost to reach each cell
    f_cost = {start: heuristic(start, goal)}  # Dictionary to store the f-cost (g + h)
    came_from = {}  # Dictionary to reconstruct the path
    
    while open_list:
        current_f, current = heapq.heappop(open_list)
        
        # If we reached the goal, reconstruct the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)  # Add start point to path
            path.reverse()  # Reverse the path to start -> goal
            return path
        
        current_x, current_y = current
        
        for dx, dy in DIRECTIONS:
            neighbor = (current_x + dx, current_y + dy)
            
            # Check if the neighbor is within bounds and is not an obstacle
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != 3:
                
                # Get traffic cost for the neighbor cell
                traffic_cost = get_traffic_data_for_cell(neighbor[0], neighbor[1], traffic_data)  # Numeric traffic cost
                
                # If traffic cost is None, use a default value (e.g., 1)
                if traffic_cost is None:
                    traffic_cost = 1
                
                # Calculate the tentative g-cost to reach the neighbor
                tentative_g_cost = g_cost[current] + traffic_cost
                
                # If this neighbor is not in g_cost or we found a shorter path
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g_cost
                    f_cost[neighbor] = tentative_g_cost + heuristic(neighbor, goal)  # f = g + h
                    heapq.heappush(open_list, (f_cost[neighbor], neighbor))  # Push neighbor to open list

    return None  # Return None if no path is found
