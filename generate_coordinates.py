#!/usr/bin/env python3
"""
Generate approximate station coordinates for network visualization
Uses a simple layout algorithm to spread stations reasonably
"""

import json
import csv
import random

# Load the network to get station list
with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json', 'r') as f:
    network = json.load(f)

stations = network['stations']

# Set seed for reproducibility
random.seed(42)

# Generate coordinates in a grid-like pattern with some randomness
# This creates a reasonable spread for visualization
coords = {}

# Simple grid layout with randomization
grid_size = 12  # ~12x12 grid for 71 stations
stations_sorted = sorted(stations)

for i, station in enumerate(stations_sorted):
    row = i // grid_size
    col = i % grid_size

    # Add some random offset for natural look
    x = col * 2 + random.uniform(-0.5, 0.5)
    y = row * 2 + random.uniform(-0.5, 0.5)

    coords[station] = (round(x, 2), round(y, 2))

# Write to CSV
with open('station_coords.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['station', 'x', 'y'])

    for station in sorted(coords.keys()):
        x, y = coords[station]
        writer.writerow([station, x, y])

print(f"✅ Created station_coords.csv with {len(coords)} station coordinates")
print(f"📍 Sample coordinates:")
for station in list(sorted(coords.keys()))[:5]:
    x, y = coords[station]
    print(f"  {station}: ({x}, {y})")
