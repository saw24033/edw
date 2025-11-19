#!/usr/bin/env python3
"""
Test terminal detection for Benton Bridge -> Benton (intermediate stop)
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
print("TESTING TERMINAL DETECTION FOR INTERMEDIATE STOPS")
print("=" * 80)

print("\n1. Loading station knowledge...")
stations = skh.load_station_knowledge(part1, part2)
print(f"   Loaded {len(stations)} stations")

print("\n2. Getting Benton Bridge station data...")
benton_bridge = stations.get("Benton Bridge (Station)")
if not benton_bridge:
    print("   [ERROR] Benton Bridge (Station) not found!")
    sys.exit(1)

print(f"   Found: {benton_bridge['name']}")

print("\n3. Building directional platform map...")
directional_map = skh.build_directional_platform_map(benton_bridge)
print(f"   Directional entries: {len(directional_map)}")

# Show all R045 entries
r045_entries = {k: v for k, v in directional_map.items() if k[0] == 'R045'}
print(f"\n4. R045 directional entries at Benton Bridge:")
for (route, dest), plats in r045_entries.items():
    print(f"   {route} -> {dest}: Platform {', '.join(plats)}")

print("\n5. Testing INTERMEDIATE STATION lookup (R045 -> Benton)...")
print("   Query: get_route_platform(benton_bridge, 'R045', 'Benton')")

result = skh.get_route_platform(benton_bridge, 'R045', 'Benton', csv_path=csv_path)

print(f"\n   Result: {result}")

if result and "Platform" in result:
    print(f"   [OK] Terminal detection successful!")
    if "toward" in result:
        print(f"   [OK] Direction indicated: {result}")
else:
    print(f"   [WARN] Platform lookup returned: {result}")

print("\n6. Testing TERMINAL STATION lookup (R045 -> Leighton City)...")
print("   Query: get_route_platform(benton_bridge, 'R045', 'Leighton City')")

result_terminal = skh.get_route_platform(benton_bridge, 'R045', 'Leighton City', csv_path=csv_path)
print(f"\n   Result: {result_terminal}")

if result_terminal and "Platform" in result_terminal:
    print(f"   [OK] Terminal lookup successful!")

print("\n7. Testing route-level fallback (R045 without destination)...")
result_fallback = skh.get_route_platform(benton_bridge, 'R045', csv_path=csv_path)
print(f"   Result: {result_fallback}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
