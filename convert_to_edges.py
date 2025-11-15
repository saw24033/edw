#!/usr/bin/env python3
"""
Convert Stepford County Railway JSON to edge-based CSV format
This creates rail_routes.csv with one row per station-to-station segment
"""

import json
import csv
import re

def parse_travel_time(time_str):
    """Extract minutes from travel time string"""
    if isinstance(time_str, int):
        return time_str
    if isinstance(time_str, str):
        match = re.search(r'(\d+)', time_str)
        if match:
            return int(match.group(1))
    return 0

# Load the network data
with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json', 'r') as f:
    network = json.load(f)

routes = network['routes']

# Build edge list
edges = []
edge_set = set()  # To track unique edges

for route_id, route_data in routes.items():
    operator = route_data.get('operator', 'Unknown')
    line = route_id
    route_type = route_data.get('route_type', 'Regular')
    stations = route_data.get('stations', [])
    travel_time_dict = route_data.get('travel_time', {})

    # Get total travel time
    total_time = parse_travel_time(travel_time_dict.get('up', travel_time_dict.get('down', 0)))

    # Calculate average time per segment if we have total time
    if len(stations) > 1 and total_time > 0:
        avg_time_per_segment = total_time / (len(stations) - 1)
    else:
        avg_time_per_segment = 5  # Default 5 minutes

    # Create edges for consecutive stations on this route
    for i in range(len(stations) - 1):
        from_station = stations[i]
        to_station = stations[i + 1]

        # Create a unique key for this edge (bidirectional)
        edge_key = tuple(sorted([from_station, to_station, operator, line]))

        # Only add if we haven't seen this exact edge before
        if edge_key not in edge_set:
            edge_set.add(edge_key)

            edges.append({
                'operator': operator,
                'line': line,
                'from_station': from_station,
                'to_station': to_station,
                'travel_time_min': round(avg_time_per_segment, 1),
                'service_type': route_type,
                'route_origin': route_data.get('origin', ''),
                'route_destination': route_data.get('destination', '')
            })

# Sort by operator, then line, then from_station
edges.sort(key=lambda x: (x['operator'], x['line'], x['from_station']))

# Write to CSV
with open('rail_routes.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['operator', 'line', 'from_station', 'to_station',
                  'travel_time_min', 'service_type', 'route_origin', 'route_destination']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(edges)

print(f"✅ Created rail_routes.csv with {len(edges)} edges")
print(f"📊 Operators: {len(set(e['operator'] for e in edges))}")
print(f"📊 Lines: {len(set(e['line'] for e in edges))}")
print(f"📊 Stations: {len(set(e['from_station'] for e in edges) | set(e['to_station'] for e in edges))}")
