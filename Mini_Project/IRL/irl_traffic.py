import requests
from datetime import datetime

def get_traffic_data(start, end):
    """
    Fetch traffic-aware route information from HERE API with real-time traffic data.

    Args:
        start (str): Starting location in "latitude,longitude" format.
        end (str): Ending location in "latitude,longitude" format.
    
    Returns:
        dict: A dictionary containing traffic data for grid-based analysis.
    """
    base_url = "https://router.hereapi.com/v8/routes"
    
    # Define query parameters
    params = {
        "apikey": "HI1yJbeC1WE_6S6-m3r091A9fk5PZXG0m0MLDraXczE",  # Replace with your HERE API key
        "transportMode": "car",
        "origin": start,
        "destination": end,
        "return": "summary,travelSummary",
        "departureTime": datetime.now().replace(microsecond=0).isoformat()
    }
    
    # Make API request to get the route summary
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        
        if "routes" in data and data["routes"]:
            route_summary = data["routes"][0]["sections"][0]["summary"]
            distance = route_summary["length"] / 1000  # Convert to kilometers
            duration = route_summary["baseDuration"] / 60  # Convert to minutes
            duration_in_traffic = route_summary["duration"] / 60  # Convert to minutes
            
            print(f"Distance: {distance} km")
            print(f"Duration without traffic: {duration} minutes")
            print(f"Duration with traffic: {duration_in_traffic} minutes")
            
            # Fetch traffic flow data for grid cells from HERE Traffic API
            traffic_data = get_real_time_traffic_data(start, end)
            
            return traffic_data
        else:
            print("No routes found.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_real_time_traffic_data(start, end):
    """
    Fetch real-time traffic flow data from the HERE Traffic API for grid-based analysis.
    
    Args:
        start (str): Starting location in "latitude,longitude" format.
        end (str): Ending location in "latitude,longitude" format.
    
    Returns:
        dict: A dictionary containing real-time traffic flow data for grid cells.
    """
    traffic_base_url = "https://traffic.ls.hereapi.com/traffic/6.2/flow.json"
    
    # Define query parameters for traffic flow
    params = {
        "apikey": "HI1yJbeC1WE_6S6-m3r091A9fk5PZXG0m0MLDraXczE",  # Replace with your HERE API key
        "bbox": f"{start},{end}",  # Bounding box for the traffic data
        "incl": "traffic,all"  # Include all traffic data
    }
    
    # Make API request to get traffic flow data
    response = requests.get(traffic_base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Parse the traffic flow data and map it to grid cells
        traffic_data = {}
        for flow in data.get('TRAFFIC', {}).get('flow', []):
            lat, lon = flow['location']['lat'], flow['location']['lng']
            # Convert latitude, longitude to grid cell (simple approach, could be more refined)
            grid_cell = (int(lat * 10), int(lon * 10))  # Example grid mapping
            traffic_condition = flow['condition']
            
            if traffic_condition == "LOW":
                traffic_data[grid_cell] = 1  # Light traffic
            elif traffic_condition == "MEDIUM":
                traffic_data[grid_cell] = 2  # Moderate traffic
            elif traffic_condition == "HIGH":
                traffic_data[grid_cell] = 5  # Heavy traffic
            else:
                traffic_data[grid_cell] = 0  # No traffic
        
        return traffic_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_traffic_data_for_cell(x, y, traffic_data):
    """
    Get the traffic condition for a specific grid cell based on the traffic data.

    Args:
        x (int): Row index of the grid cell.
        y (int): Column index of the grid cell.
        traffic_data (dict): Dictionary or any data structure holding traffic information.
    
    Returns:
        int: Traffic cost for the given grid cell.
    """
    # Check if the cell has specific traffic data and return the corresponding value
    if (x, y) in traffic_data:
        return traffic_data[(x, y)]
    else:
        # Default to "No traffic" if no data is available for this cell
        return 0


# Example Usage
# Coordinates for the locations (start, end)
start_coordinates = "9.093898,76.491927"  # Replace with actual lat,long of starting point
end_coordinates = "9.172815,76.497715"    # Replace with actual lat,long of destination

traffic_data = get_traffic_data(start_coordinates, end_coordinates)

# Analyze specific grid cell traffic
if traffic_data:
    cell_x, cell_y = 0, 1  # Example grid cell coordinates
    traffic_cost = get_traffic_data_for_cell(cell_x, cell_y, traffic_data)
    print(f"Traffic cost for cell ({cell_x}, {cell_y}): {traffic_cost}")
