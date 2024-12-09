import heapq

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
