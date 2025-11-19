#!/usr/bin/env python3
"""
Comprehensive test of terminal detection across multiple scenarios
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
print("COMPREHENSIVE TERMINAL DETECTION TESTS")
print("=" * 80)

stations = skh.load_station_knowledge(part1, part2)

# Test cases: (station_name, route, next_station, expected_result_contains)
test_cases = [
    # Intermediate stops (should use terminal detection)
    ("Benton Bridge (Station)", "R045", "Benton", "Platform 3", "toward Stepford Victoria"),
    ("Benton Bridge (Station)", "R045", "Hampton Hargate", "Platform 2", "toward Leighton"),

    # Terminal stations (should use direct lookup)
    ("Benton Bridge (Station)", "R045", "Leighton City", "Platform 2", None),
    ("Benton Bridge (Station)", "R045", "Stepford Victoria", "Platform 3", None),

    # Route-level fallback (no next_station provided)
    ("Benton Bridge (Station)", "R045", None, "Platforms 2, 3", None),
]

passed = 0
failed = 0

for i, test_case in enumerate(test_cases, 1):
    station_name, route, next_station, expected_platform, expected_direction = test_case

    print(f"\nTest {i}: {station_name} | {route} -> {next_station or '(no destination)'}")

    station_data = stations.get(station_name)
    if not station_data:
        print(f"   [FAIL] Station '{station_name}' not found!")
        failed += 1
        continue

    result = skh.get_route_platform(station_data, route, next_station, csv_path=csv_path)

    print(f"   Result: {result}")
    print(f"   Expected: {expected_platform}", end="")
    if expected_direction:
        print(f" (with '{expected_direction}')")
    else:
        print()

    # Check result
    if result and expected_platform in result:
        if expected_direction:
            if expected_direction in result:
                print(f"   [PASS] Platform and direction correct")
                passed += 1
            else:
                print(f"   [FAIL] Platform correct but missing direction '{expected_direction}'")
                failed += 1
        else:
            print(f"   [PASS] Platform correct")
            passed += 1
    else:
        print(f"   [FAIL] Expected '{expected_platform}' but got '{result}'")
        failed += 1

print("\n" + "=" * 80)
print(f"TESTS COMPLETE: {passed} passed, {failed} failed")
print("=" * 80)

if failed == 0:
    print("\n[SUCCESS] All terminal detection tests passed!")
    sys.exit(0)
else:
    print(f"\n[WARNING] {failed} test(s) failed")
    sys.exit(1)
