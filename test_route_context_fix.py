#!/usr/bin/env python3
"""
Test get_route_context() with terminal detection fix
Mimics the Custom GPT call that was returning None
"""

import sys
sys.path.insert(0, 'C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload')

import importlib
import station_knowledge_helper as skh
importlib.reload(skh)

# Load stations
part1 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part1.md"
part2 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part2.md"

print("=" * 80)
print("TEST: get_route_context() WITH TERMINAL DETECTION FIX")
print("=" * 80)

print("\n1. Loading station knowledge...")
stations = skh.load_station_knowledge(part1, part2)
print(f"   Loaded {len(stations)} stations")

print("\n2. Testing get_route_context() - Mimicking Custom GPT call...")
print("   Query: Benton Bridge -> Benton on R045 (Stepford Connect)")

# This is exactly what the Custom GPT was calling
origin = skh.get_route_context(
    "Benton Bridge",
    "Stepford Connect",
    stations,
    route_code="R045",
    next_station="Benton"
)

print(f"\n   Result: {origin}")

if origin is None:
    print("\n   [FAIL] Still returning None!")
    print("   This means the fix didn't work or station name mismatch")
elif 'departure_platforms' in origin and origin['departure_platforms']:
    print(f"\n   [PASS] Platform data returned: {origin['departure_platforms']}")
    if "toward" in origin['departure_platforms']:
        print(f"   [PASS] Direction indicator present!")
else:
    print(f"\n   [WARN] Context returned but no platform data")

print("\n3. Testing with correct station name (Benton Bridge (Station))...")
origin_fixed = skh.get_route_context(
    "Benton Bridge (Station)",
    "Stepford Connect",
    stations,
    route_code="R045",
    next_station="Benton"
)

print(f"\n   Result: {origin_fixed}")

if origin_fixed and 'departure_platforms' in origin_fixed and origin_fixed['departure_platforms']:
    print(f"\n   [PASS] Platform data: {origin_fixed['departure_platforms']}")
    if "toward" in origin_fixed['departure_platforms']:
        print(f"   [PASS] Direction indicator: YES")

print("\n4. Comparing both results...")
print(f"   'Benton Bridge': {origin is not None}")
print(f"   'Benton Bridge (Station)': {origin_fixed is not None}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
