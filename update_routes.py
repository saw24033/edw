"""
Route Data Update Helper for Stepford County Railway
====================================================
This script helps systematically update route information in the JSON file.

ISSUES IDENTIFIED:
1. R081 - Currently shows: Stepford Central → Morganstown → Llyn-by-the-Sea
   Wiki says: Stepford Central → Leighton City → Llyn-by-the-Sea (super fast, skips most stations)

2. R083 - Currently missing some intermediate stations
   Wiki says: Newry → Benton → Morganstown → Leighton Stepford Road → Leighton City → Westercoast → Northshore → Llyn-by-the-Sea

3. R085 - Exists as direct route Benton → Llyn-by-the-Sea but may have incomplete station list
   Wiki says: Benton → Morganstown → [stations] → Llyn-by-the-Sea (6 stations total, ~20 min)

USAGE:
1. Gather correct route information from SCR wiki: https://scr.fandom.com/wiki/List_of_Routes
2. Use update_route() function to fix each route
3. Save updated JSON

"""

import json
from typing import List, Dict


def load_json(filepath='stepford_routes_with_segment_minutes_ai_knowledge_base.json'):
    """Load the current JSON data"""
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(data, filepath='stepford_routes_with_segment_minutes_ai_knowledge_base.json'):
    """Save updated JSON data"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved to {filepath}")


def update_route(data: Dict, route_id: str, **kwargs) -> Dict:
    """
    Update a specific route with new information.

    Args:
        data: Full JSON data structure
        route_id: Route ID (e.g., "R001")
        **kwargs: Fields to update (operator, origin, destination, stations, travel_time, etc.)

    Returns:
        Updated data structure
    """
    if route_id not in data['routes']:
        print(f"❌ Route {route_id} not found")
        return data

    route = data['routes'][route_id]

    # Update fields
    for key, value in kwargs.items():
        if key in route:
            old_value = route[key]
            route[key] = value
            print(f"  Updated {key}: {old_value} → {value}")
        else:
            route[key] = value
            print(f"  Added {key}: {value}")

    # Update stops count if stations list changed
    if 'stations' in kwargs:
        route['stops'] = len(kwargs['stations'])
        print(f"  Updated stops: {route['stops']}")

    print(f"✅ Updated route {route_id}")
    return data


def create_route_template():
    """Template for a new/updated route"""
    return {
        "operator": "Stepford Connect",  # or Metro, Stepford Express, AirLink, Waterline
        "origin": "Start Station",
        "destination": "End Station",
        "route_type": "Service Type",  # e.g., "Express", "Connect", "Local"
        "price": "XXX Points",
        "travel_time": {
            "up": "XX minutes",
            "down": "XX minutes"
        },
        "stops": 0,  # Will be auto-calculated
        "stations": [
            "Station 1",
            "Station 2",
            "Station 3"
        ]
    }


def batch_update_routes(data: Dict, updates: Dict[str, Dict]) -> Dict:
    """
    Update multiple routes at once.

    Args:
        data: Full JSON data
        updates: Dict of {route_id: {field: value, ...}}

    Returns:
        Updated data
    """
    for route_id, fields in updates.items():
        data = update_route(data, route_id, **fields)
    return data


# Known corrections from wiki research
KNOWN_CORRECTIONS = {
    "R081": {
        "stations": [
            "Stepford Central",
            "Leighton City",
            "Llyn-by-the-Sea"
        ],
        "route_type": "Llyn (super fast)",
        "stops": 3,
        "travel_time": {
            "up": "17 minutes",
            "down": "17 minutes"
        },
        "price": "750 Points"
    },
    "R083": {
        "stations": [
            "Newry",
            "Benton",
            "Morganstown",
            "Leighton Stepford Road",
            "Leighton City",
            "Westercoast",
            "Northshore",
            "Llyn-by-the-Sea"
        ],
        "origin": "Newry",
        "destination": "Llyn-by-the-Sea",
        "route_type": "Newry Express",
        "stops": 8,
        "travel_time": {
            "up": "24 minutes",
            "down": "24 minutes"
        },
        "price": "600 Points"
    },
    "R085": {
        "stations": [
            "Benton",
            "Morganstown",
            "Leighton Stepford Road",
            "Leighton City",
            "Northshore",
            "Llyn-by-the-Sea"
        ],
        "route_type": "Benton to Llyn",
        "stops": 6,
        "travel_time": {
            "up": "20 minutes",
            "down": "20 minutes"
        }
    }
}


if __name__ == "__main__":
    # Load current data
    print("Loading JSON data...")
    data = load_json()

    print(f"\n📊 Current state:")
    print(f"Total routes: {len(data['routes'])}")
    print(f"Total stations: {data['metadata']['total_stations']}")

    # Apply known corrections
    print("\n🔧 Applying known corrections...")
    data = batch_update_routes(data, KNOWN_CORRECTIONS)

    # Save backup
    print("\n💾 Saving backup...")
    save_json(data, 'stepford_routes_with_segment_minutes_ai_knowledge_base_backup.json')

    # Save updated version
    print("\n💾 Saving updated version...")
    save_json(data)

    print("\n✅ Done! Review the changes and regenerate CSV with:")
    print("   python3 convert_to_edges.py")
