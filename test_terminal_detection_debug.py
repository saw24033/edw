#!/usr/bin/env python3
"""
Debug terminal detection - see what's happening inside the function
"""

import sys
sys.path.insert(0, 'C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload')

import importlib
import station_knowledge_helper as skh
importlib.reload(skh)

# Load stations
part1 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part1.md"
part2 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part2.md"
csv_path = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\rail_routes.csv"

print("=" * 80)
print("DEBUG: TERMINAL DETECTION FOR R045 AT BENTON BRIDGE -> BENTON")
print("=" * 80)

print("\n1. Loading station knowledge...")
stations = skh.load_station_knowledge(part1, part2)
benton_bridge = stations.get("Benton Bridge (Station)")

print("\n2. Testing _get_terminal_for_direction() directly...")
print("   Input:")
print("     route_code = 'R045'")
print("     current_station = 'Benton Bridge (Station)'")
print("     next_station = 'Benton'")

terminal = skh._get_terminal_for_direction(
    'R045',
    'Benton Bridge (Station)',
    'Benton',
    csv_path
)

print(f"\n   Terminal returned: {terminal}")

if terminal:
    print(f"   [OK] Terminal detection found: {terminal}")
else:
    print("   [ERROR] Terminal detection returned None!")

print("\n3. Checking if terminal exists in directional_map...")
directional_map = skh.build_directional_platform_map(benton_bridge)

if terminal:
    key = ('R045', terminal)
    if key in directional_map:
        print(f"   [OK] Found ({key[0]}, {key[1]}) in directional_map")
        print(f"   Platforms: {directional_map[key]}")
    else:
        print(f"   [ERROR] Key {key} NOT found in directional_map")
        print("\n   Available R045 entries in directional_map:")
        for (route, dest), plats in directional_map.items():
            if route == 'R045':
                print(f"     ({route}, {dest}): {plats}")

print("\n4. Testing _load_route_terminals() to see route data...")
routes = skh._load_route_terminals(csv_path)

if 'R045' in routes:
    r045_info = routes['R045']
    print(f"   R045 route info:")
    print(f"     Origin: {r045_info['origin']}")
    print(f"     Destination: {r045_info['destination']}")
    print(f"     Stops: {r045_info['stops']}")

    # Check station positions
    stops = r045_info['stops']
    if 'Benton Bridge (Station)' in stops:
        bb_idx = stops.index('Benton Bridge (Station)')
        print(f"\n   Benton Bridge (Station) is at index {bb_idx}")
    else:
        print(f"\n   [ERROR] 'Benton Bridge (Station)' not found in stops!")
        print(f"   Checking for similar names...")
        for i, stop in enumerate(stops):
            if 'benton bridge' in stop.lower():
                print(f"     Index {i}: {stop}")

    if 'Benton' in stops:
        benton_idx = stops.index('Benton')
        print(f"   Benton is at index {benton_idx}")
    else:
        print(f"   [ERROR] 'Benton' not found in stops!")
        print(f"   Checking for similar names...")
        for i, stop in enumerate(stops):
            if stop.lower() == 'benton' or 'benton' in stop.lower():
                print(f"     Index {i}: {stop}")
else:
    print("   [ERROR] R045 not found in routes!")

print("\n5. Full test with get_route_platform()...")
result = skh.get_route_platform(benton_bridge, 'R045', 'Benton', csv_path=csv_path)
print(f"   Result: {result}")

print("\n" + "=" * 80)
print("DEBUG COMPLETE")
print("=" * 80)
