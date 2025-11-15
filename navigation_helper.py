"""
Stepford County Railway Navigation Helper
==========================================
This code is designed to run inside a GPT with Code Interpreter enabled.
It provides navigation functions for the Stepford County Railway network.

IMPORTANT: This file is for REFERENCE. The GPT will write and execute
similar code when passengers ask for journey planning.
"""

import json
from typing import List, Dict, Tuple, Optional

# Load the network data
with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json', 'r') as f:
    network = json.load(f)

stations = network['stations']
routes = network['routes']
station_index = network['station_index']
connections = network.get('connections', {})
interchanges = network.get('interchanges', {})


def find_direct_routes(origin: str, destination: str) -> List[Dict]:
    """
    Find all routes that directly connect origin to destination.

    Args:
        origin: Starting station name
        destination: Ending station name

    Returns:
        List of route dictionaries with journey details
    """
    direct_routes = []

    # Get all routes serving the origin station
    if origin not in station_index:
        return []

    origin_routes = station_index[origin]['routes']

    # Check each route to see if it also serves the destination
    for route_id in origin_routes:
        route = routes[route_id]

        # Check if both stations are on this route
        if origin in route['stations'] and destination in route['stations']:
            origin_idx = route['stations'].index(origin)
            dest_idx = route['stations'].index(destination)

            # Make sure they're in the right order (origin before destination)
            if origin_idx < dest_idx:
                # Calculate number of stops between stations
                stops_between = dest_idx - origin_idx

                direct_routes.append({
                    'route_id': route_id,
                    'operator': route['operator'],
                    'route_type': route.get('route_type', 'Regular'),
                    'origin': origin,
                    'destination': destination,
                    'stations': route['stations'][origin_idx:dest_idx + 1],
                    'stops': stops_between,
                    'travel_time': route.get('travel_time', {}),
                    'price': route.get('price', 'Standard fare'),
                    'full_route_origin': route['origin'],
                    'full_route_destination': route['destination']
                })

    return direct_routes


def find_one_interchange_routes(origin: str, destination: str) -> List[Dict]:
    """
    Find routes requiring exactly one interchange.

    Args:
        origin: Starting station name
        destination: Ending station name

    Returns:
        List of journey dictionaries with two-leg routes
    """
    interchange_routes = []

    if origin not in station_index or destination not in station_index:
        return []

    # Get all possible interchange stations from the origin
    origin_interchanges = station_index[origin].get('interchanges', [])

    # For each possible interchange station
    for interchange in origin_interchanges:
        # Find routes from origin to interchange
        leg1_routes = find_direct_routes(origin, interchange)

        # Find routes from interchange to destination
        leg2_routes = find_direct_routes(interchange, destination)

        # Combine them
        for leg1 in leg1_routes:
            for leg2 in leg2_routes:
                # Make sure we're not using the same route twice
                if leg1['route_id'] != leg2['route_id']:
                    interchange_routes.append({
                        'type': 'one_interchange',
                        'interchange_at': interchange,
                        'leg1': leg1,
                        'leg2': leg2,
                        'total_stops': leg1['stops'] + leg2['stops'],
                        'route_ids': [leg1['route_id'], leg2['route_id']]
                    })

    return interchange_routes


def parse_travel_time(time_str: str) -> int:
    """
    Convert travel time string to minutes.

    Args:
        time_str: String like "18 minutes" or "25 mins"

    Returns:
        Integer minutes
    """
    if isinstance(time_str, int):
        return time_str

    if isinstance(time_str, str):
        # Extract number from string
        import re
        match = re.search(r'(\d+)', time_str)
        if match:
            return int(match.group(1))

    return 0


def calculate_journey_time(journey: Dict) -> int:
    """
    Calculate total journey time including interchange penalties.

    Args:
        journey: Journey dictionary

    Returns:
        Total time in minutes
    """
    if 'leg1' in journey:
        # Multi-leg journey
        leg1_time = journey['leg1'].get('travel_time', {})
        leg2_time = journey['leg2'].get('travel_time', {})

        # Try to get 'up' direction time, fallback to parsing the dict
        time1 = parse_travel_time(leg1_time.get('up', leg1_time.get('down', 0)))
        time2 = parse_travel_time(leg2_time.get('up', leg2_time.get('down', 0)))

        # Add 4 minutes for interchange
        interchange_penalty = 4

        return time1 + time2 + interchange_penalty
    else:
        # Direct journey
        travel_time = journey.get('travel_time', {})
        return parse_travel_time(travel_time.get('up', travel_time.get('down', 0)))


def find_all_routes(origin: str, destination: str) -> Dict:
    """
    Find all possible routes between two stations.

    Args:
        origin: Starting station name
        destination: Ending station name

    Returns:
        Dictionary with direct and interchange routes, sorted by preference
    """
    # Find direct routes
    direct = find_direct_routes(origin, destination)

    # Find one-interchange routes
    one_change = find_one_interchange_routes(origin, destination)

    # Sort direct routes by travel time
    direct_sorted = sorted(direct, key=lambda x: calculate_journey_time(x))

    # Sort interchange routes by total time
    interchange_sorted = sorted(one_change, key=lambda x: calculate_journey_time(x))

    return {
        'direct_routes': direct_sorted,
        'one_interchange_routes': interchange_sorted,
        'has_direct': len(direct) > 0,
        'total_options': len(direct) + len(one_change)
    }


def get_station_info(station_name: str) -> Optional[Dict]:
    """
    Get comprehensive information about a station.

    Args:
        station_name: Name of the station

    Returns:
        Dictionary with station information
    """
    if station_name not in station_index:
        return None

    station_data = station_index[station_name]

    return {
        'name': station_name,
        'total_routes': len(station_data['routes']),
        'routes': station_data['routes'],
        'interchanges': station_data.get('interchanges', []),
        'total_connections': station_data.get('connections', 0),
        'is_major_hub': len(station_data['routes']) > 10
    }


def search_station_name(query: str) -> List[str]:
    """
    Search for stations matching a query (fuzzy search).

    Args:
        query: Search string

    Returns:
        List of matching station names
    """
    query_lower = query.lower()

    # Exact match
    exact_matches = [s for s in stations if s.lower() == query_lower]
    if exact_matches:
        return exact_matches

    # Contains match
    contains_matches = [s for s in stations if query_lower in s.lower()]
    if contains_matches:
        return contains_matches

    # Word-based match
    query_words = query_lower.split()
    word_matches = []
    for station in stations:
        station_lower = station.lower()
        if all(word in station_lower for word in query_words):
            word_matches.append(station)

    return word_matches


def format_route_display(route: Dict, route_number: int = 1) -> str:
    """
    Format a route for display to passengers.

    Args:
        route: Route dictionary
        route_number: Option number for display

    Returns:
        Formatted string
    """
    if 'leg1' in route:
        # Interchange route
        leg1 = route['leg1']
        leg2 = route['leg2']
        total_time = calculate_journey_time(route)

        output = f"**Option {route_number} - Via {route['interchange_at']}**\n"
        output += f"🚆 {leg1['route_type']} ({leg1['route_id']}) → Change at {route['interchange_at']} → "
        output += f"{leg2['route_type']} ({leg2['route_id']})\n"
        output += f"- Total travel time: ~{total_time} minutes (including 4 min interchange)\n"
        output += f"- Total stops: {route['total_stops']}\n"
        output += f"- Operators: {leg1['operator']}, {leg2['operator']}\n"

        return output
    else:
        # Direct route
        travel_time = calculate_journey_time(route)

        output = f"**Option {route_number} - Direct Route**\n"
        output += f"🚆 {route['route_type']} Service\n"
        output += f"- Route: {route['route_id']}\n"
        output += f"- Operator: {route['operator']}\n"
        output += f"- Travel time: {travel_time} minutes\n"
        output += f"- Stops: {route['stops']}\n"
        output += f"- Price: {route['price']}\n"
        output += f"- Stations: {' → '.join(route['stations'])}\n"

        return output


# Example usage
if __name__ == "__main__":
    # Example 1: Find direct routes
    print("Example 1: Direct routes from Stepford Central to Airport Terminal 1")
    print("=" * 70)
    results = find_all_routes("Stepford Central", "Airport Terminal 1")

    if results['has_direct']:
        print(f"Found {len(results['direct_routes'])} direct route(s):\n")
        for i, route in enumerate(results['direct_routes'], 1):
            print(format_route_display(route, i))

    # Example 2: Station information
    print("\n" + "=" * 70)
    print("Example 2: Station information for Benton")
    print("=" * 70)
    info = get_station_info("Benton")
    if info:
        print(f"Station: {info['name']}")
        print(f"Total routes: {info['total_routes']}")
        print(f"Major hub: {'Yes' if info['is_major_hub'] else 'No'}")
        print(f"Connections: {info['total_connections']}")

    # Example 3: Search for stations
    print("\n" + "=" * 70)
    print("Example 3: Search for stations containing 'airport'")
    print("=" * 70)
    matches = search_station_name("airport")
    print(f"Found {len(matches)} station(s):")
    for station in matches:
        print(f"  - {station}")
