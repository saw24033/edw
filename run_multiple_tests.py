#!/usr/bin/env python3
"""
Run multiple random station/route tests
"""

import subprocess
import sys

print("=" * 80)
print("RUNNING 5 RANDOM STATION/ROUTE TESTS")
print("=" * 80)

results = []

for i in range(1, 6):
    print(f"\n{'='*80}")
    print(f"TEST RUN #{i}")
    print('='*80)

    result = subprocess.run([sys.executable, "test_random_station.py"],
                          capture_output=True, text=True, cwd=r"C:\Users\sydne\Documents\GitHub\edw")

    output = result.stdout

    # Extract key information
    lines = output.split('\n')
    station = None
    route = None
    destination = None
    platforms = None
    lookup_result = None
    status = None

    for line in lines:
        if 'Randomly selected station:' in line or 'Found station with services:' in line:
            station = line.split(':')[-1].strip()
        elif 'Route:' in line and route is None:
            route = line.split(':')[-1].strip()
        elif 'Destination:' in line:
            destination = line.split(':')[-1].strip()
        elif 'Platforms:' in line and platforms is None:
            platforms = line.split(':')[-1].strip()
        elif 'Result:' in line and lookup_result is None:
            lookup_result = line.split(':')[-1].strip()
        elif '[OK]' in line and 'Platform lookup' in line:
            status = 'PASS'
        elif '[WARN]' in line and 'Platform lookup' in line:
            status = 'WARN'

    if station:
        result_data = {
            'run': i,
            'station': station,
            'route': route,
            'destination': destination,
            'platforms': platforms,
            'lookup': lookup_result,
            'status': status or 'UNKNOWN'
        }
        results.append(result_data)

        print(f"\nStation: {station}")
        print(f"Route: {route}")
        print(f"Destination: {destination}")
        print(f"Expected Platforms: {platforms}")
        print(f"Lookup Result: {lookup_result}")
        print(f"Status: {status or 'UNKNOWN'}")

print(f"\n{'='*80}")
print("SUMMARY OF ALL TESTS")
print('='*80)

print(f"\n{'Run':<5} {'Station':<30} {'Route':<8} {'Destination':<25} {'Status':<10}")
print('-'*80)

for r in results:
    print(f"{r['run']:<5} {r['station']:<30} {r['route']:<8} {r['destination']:<25} {r['status']:<10}")

pass_count = sum(1 for r in results if r['status'] == 'PASS')
print(f"\n{'='*80}")
print(f"PASSED: {pass_count}/{len(results)} tests")
print('='*80)
