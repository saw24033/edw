#!/usr/bin/env python3
"""
Test script to show different corridor query behaviors
"""

from route_corridor_calculator import RouteCorridorCalculator
import json

calc = RouteCorridorCalculator()

# Load route data
with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("QUESTION: What stations are between St Helens Bridge and Leighton Stepford Road?")
print("=" * 80)
print()

start = 'St Helens Bridge'
end = 'Leighton Stepford Road'

# METHOD 1: Show ALL stations from ALL paths (comprehensive)
print("METHOD 1: Show ALL stations from ALL possible paths")
print("-" * 80)

all_stations = set()
paths_by_type = {
    'via_hampton': [],
    'via_morganstown': [],
    'direct': []
}

for route_code, route_data in data['routes'].items():
    stations = route_data.get('stations', [])
    try:
        s_idx = stations.index(start)
        e_idx = stations.index(end)

        if s_idx < e_idx:
            segment = stations[s_idx:e_idx+1]
            all_stations.update(segment)

            # Categorize the path
            if 'Hampton Hargate' in segment:
                paths_by_type['via_hampton'].append((route_code, segment))
            elif 'Morganstown' in segment:
                paths_by_type['via_morganstown'].append((route_code, segment))
            elif len(segment) == 3 and 'Benton' in segment:
                paths_by_type['direct'].append((route_code, segment))
    except ValueError:
        pass

print(f"Total unique stations across ALL paths: {len(all_stations)}")
print(f"Stations: {', '.join(sorted(all_stations))}")
print()

# METHOD 2: Show paths grouped by corridor type
print("METHOD 2: Show paths grouped by corridor type")
print("-" * 80)

print(f"\nVia Hampton Hargate corridor ({len(paths_by_type['via_hampton'])} services):")
for route, path in paths_by_type['via_hampton'][:3]:
    print(f"  {route}: {' → '.join(path)}")

print(f"\nVia Morganstown (divergent) ({len(paths_by_type['via_morganstown'])} services):")
for route, path in paths_by_type['via_morganstown']:
    print(f"  {route}: {' → '.join(path)}")

print(f"\nDirect via Benton ({len(paths_by_type['direct'])} services):")
for route, path in paths_by_type['direct']:
    print(f"  {route}: {' → '.join(path)}")

print()

# METHOD 3: Longest path (what current calculator uses for express services)
print("METHOD 3: Longest path (current default for express services)")
print("-" * 80)

# Find longest path
all_paths = {}
for route_code, route_data in data['routes'].items():
    stations = route_data.get('stations', [])
    try:
        s_idx = stations.index(start)
        e_idx = stations.index(end)

        if s_idx < e_idx:
            segment = tuple(stations[s_idx:e_idx+1])
            if segment not in all_paths:
                all_paths[segment] = []
            all_paths[segment].append(route_code)
    except ValueError:
        pass

longest_path = max(all_paths.keys(), key=len)
print(f"Longest path ({len(longest_path)} stations):")
print(f"  {' → '.join(longest_path)}")
print(f"  Used by: {', '.join(all_paths[longest_path])}")

print()
print("=" * 80)
print("CURRENT CALCULATOR BEHAVIOR:")
print("=" * 80)
print()
print("For ROUTE-SPECIFIC queries (e.g., 'What does R080 skip?'):")
print("  → Uses the path that route ACTUALLY takes (detects divergent routes)")
print()
print("For GENERIC queries (e.g., 'What's between A and B?'):")
print("  → Would need a NEW function to handle this properly")
print("  → Options:")
print("     A) Show ALL stations from ALL paths (Method 1)")
print("     B) Show paths grouped by corridor (Method 2)")
print("     C) Show only longest path (Method 3 - current default)")
print()
