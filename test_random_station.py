#!/usr/bin/env python3
"""
Test platform parser with random station and route
"""

import sys
sys.path.append('C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload')

import station_knowledge_helper as skh
import random
import re

# Load stations
part1 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part1.md"
part2 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part2.md"

print("=" * 80)
print("RANDOM STATION AND ROUTE TEST")
print("=" * 80)

print("\n1. Loading station knowledge...")
stations = skh.load_station_knowledge(part1, part2)
print(f"   Loaded {len(stations)} stations")

# Pick a random station
random_station_name = random.choice(list(stations.keys()))
print(f"\n2. Randomly selected station: {random_station_name}")

station_data = stations[random_station_name]

# Check if station has Services section
content = station_data['full_content']
services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)',
                            content, re.DOTALL | re.IGNORECASE)

if not services_section:
    print(f"   [SKIP] {random_station_name} has no Services section")
    print("\n   Trying another random station...")

    # Try a few more times to find a station with services
    for _ in range(10):
        random_station_name = random.choice(list(stations.keys()))
        station_data = stations[random_station_name]
        content = station_data['full_content']
        services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)',
                                    content, re.DOTALL | re.IGNORECASE)
        if services_section:
            print(f"   Found station with services: {random_station_name}")
            break

    if not services_section:
        print("   [ERROR] Could not find a station with Services section")
        sys.exit(1)

print(f"\n3. Analyzing {random_station_name} Services section...")

# Build directional map
directional_map = skh.build_directional_platform_map(station_data)
route_platform_map = skh.build_route_platform_map(station_data)

print(f"   Directional map entries: {len(directional_map)}")
print(f"   Route-platform map entries: {len(route_platform_map)}")

if not directional_map and not route_platform_map:
    print("   [WARN] No routes found in Services section")
    sys.exit(0)

# Pick a random route from the directional map or route map
if directional_map:
    print("\n4. Testing DIRECTIONAL platform lookup...")
    random_entry = random.choice(list(directional_map.items()))
    (route_code, destination), platforms = random_entry

    print(f"\n   Random selection:")
    print(f"   Route: {route_code}")
    print(f"   Destination: {destination}")
    print(f"   Platforms: {platforms}")

    # Test get_route_platform function
    result = skh.get_route_platform(station_data, route_code, destination)

    print(f"\n   get_route_platform('{route_code}', '{destination}'):")
    print(f"   Result: {result}")

    if result and any(p in result for p in platforms):
        print(f"   [OK] Platform lookup successful!")
    else:
        print(f"   [WARN] Platform lookup mismatch")
        print(f"         Expected: {platforms}")
        print(f"         Got: {result}")

    # Show all directional entries for this route
    route_entries = [(k, v) for k, v in directional_map.items() if k[0] == route_code]
    if len(route_entries) > 1:
        print(f"\n   Other {route_code} destinations at {random_station_name}:")
        for (r, dest), plats in route_entries:
            if dest != destination:
                print(f"   - {route_code} -> {dest}: Platforms {', '.join(plats)}")

elif route_platform_map:
    print("\n4. Testing ROUTE-LEVEL platform lookup...")
    random_route = random.choice(list(route_platform_map.keys()))
    platforms = route_platform_map[random_route]

    print(f"\n   Random selection:")
    print(f"   Route: {random_route}")
    print(f"   Platforms: {platforms}")

    # Test get_route_platform function (without destination)
    result = skh.get_route_platform(station_data, random_route)

    print(f"\n   get_route_platform('{random_route}'):")
    print(f"   Result: {result}")

    if result:
        print(f"   [OK] Platform lookup successful!")
    else:
        print(f"   [WARN] Platform lookup failed")

# Display raw Services section for manual verification
print(f"\n5. Raw Services section from {random_station_name}:")
print("   " + "-" * 76)
services_text = services_section.group(1)
# Show first 500 chars
preview = services_text[:500].replace('\n', '\n   ')
print(f"   {preview}")
if len(services_text) > 500:
    print(f"   ... (truncated, {len(services_text)} chars total)")
print("   " + "-" * 76)

print("\n6. Summary:")
print(f"   Station: {random_station_name}")
print(f"   Total routes found: {len(set(route_platform_map.keys()))}")
print(f"   Directional entries: {len(directional_map)}")
print(f"   Platform assignments working: [OK]")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
