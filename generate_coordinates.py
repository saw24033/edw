#!/usr/bin/env python3
"""
Generate station coordinates for Stepford County Railway network visualization
Based on actual official network map topology (not random placement)

UPDATED: Now uses actual map positions extracted from official SCR network map
Reference: Official Stepford County Railway transit map image

Coordinate System:
- X axis: 0 (left/west) to 30 (right/east)
- Y axis: 0 (bottom/south) to 12 (top/north)

Geographic Regions:
- Airport Cluster (top-right): Terminals 1/2/3, Airport Central/West/Parkway
- Central Hub (middle): Stepford Central, Benton, Financial Quarter
- Coastal Line (bottom): Llyn-by-the-Sea → Northshore → Millcastle → Westercoast
- Northern Branch (top-left): Willowfield, Hemdon Park, City Hospital
- Eastern Branch (right): Hampton Hargate, James Street, Farleigh
"""

import json
import csv

# Load the network to get station list
with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json', 'r') as f:
    network = json.load(f)

# Map-based coordinates (extracted from official SCR network map)
# Positioned to match actual game topology and line routes
coords = {
    # AIRPORT CLUSTER (Top-Right)
    "Airport Terminal 1": (26, 8),
    "Airport Terminal 2": (27, 9),
    "Airport Terminal 3": (28, 10),
    "Airport West": (25, 7),
    "Airport Central": (23, 8),  # Note: Using "Stepford Airport Central" as key
    "Airport Parkway": (21, 7),  # Note: Using "Stepford Airport Parkway" as key

    # CENTRAL HUB
    "Stepford Central": (7, 7),
    "Stepford East": (11, 7),
    "Stepford Victoria": (1, 7),
    "Stepford High Street": (9, 7),
    "Stepford United Football Club": (6, 7),
    "Financial Quarter": (2, 7),
    "Benton": (16, 6),
    "Port Benton": (15, 5),
    "West Benton": (23, 9),
    "Benton Bridge": (18, 5),

    # COASTAL LINE (Bottom - West to East)
    "Llyn-by-the-Sea": (2, 1),
    "Westwyvern": (6, 1),
    "Northshore": (4, 1),
    "Starryloch": (5, 1),
    "Westercoast": (8, 2),
    "Millcastle": (7, 2),
    "Millcastle Racecourse": (9, 2),

    # LEIGHTON AREA (Bottom-Center)
    "Leighton City": (10, 2),
    "Leighton Stepford Road": (12, 2),
    "Leighton West": (8, 1),

    # NORTHERN BRANCH (Top-Left)
    "Willowfield": (2, 4),
    "Hemdon Park": (3, 4),
    "Houghton Rake": (5, 4),
    "Whitefield": (5, 4),
    "Woodhead Lane": (6, 4),
    "City Hospital": (4, 7),
    "Beechley": (3, 7),

    # EASTERN BRANCH (Right)
    "Hampton Hargate": (24, 4),
    "James Street": (27, 6),
    "Esterfield": (23, 6),
    "Rosedale Village": (23, 5),
    "Farleigh": (28, 5),
    "Upper Staploe": (25, 4),

    # MORGANSTOWN CORRIDOR (Center-Right)
    "Morganstown": (18, 4),
    "Morganstown Docks": (19, 4),
    "Greenslade": (17, 4),
    "Whitney Green": (16, 4),

    # NORTHERN STATIONS
    "Newry": (25, 9),
    "Newry Harbour": (26, 10),
    "Eden Quay": (24, 9),
    "Faraday Road": (24, 9),

    # CONNOLLY BRANCH
    "Connolly": (21, 8),
    "Ashlan Park": (22, 8),
    "Cambridge Street Parkway": (19, 8),
    "Berrily": (17, 8),
    "East Berrily": (20, 8),

    # ST HELENS AREA
    "St Helens Bridge": (12, 7),
    "New Harrow": (13, 7),
    "Elsemere Junction": (17, 7),
    "Elsemere Pond": (13, 7),

    # CENTRAL STATIONS
    "Four Ways": (7, 7),
    "Bodin": (11, 5),
    "Coxly": (14, 5),
    "Coxly Newtown": (15, 4),
    "Barton": (13, 6),
    "Angel Pass": (9, 5),
    "Edgemead": (9, 3),
    "Faymere": (11, 3),

    # SOUTHERN STATIONS
    "Rayleigh Bay": (16, 2),
    "Carnalea Bridge": (18, 2),
    "Water Newton": (22, 4),
    "Rocket Parade": (26, 3),
    "Whitefield Lido": (7, 5),

    # MINOR STATIONS
    "Beaulieu Park": (20, 7),
    "Aslockby": (19, 3),
}

# Handle alternate station names (match JSON keys)
# The JSON uses full names like "Stepford Airport Central"
coord_mapping = {}
for station in network['stations']:
    if station in coords:
        coord_mapping[station] = coords[station]
    elif "Airport Central" in station and "Airport Central" in coords:
        coord_mapping[station] = coords["Airport Central"]
    elif "Airport Parkway" in station and "Airport Parkway" in coords:
        coord_mapping[station] = coords["Airport Parkway"]
    else:
        # Station not yet mapped - use placeholder or warn
        print(f"⚠️  Warning: {station} not mapped, using default position")
        coord_mapping[station] = (15, 6)  # Center of map

# Write to CSV
with open('station_coords.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['station', 'x', 'y'])

    for station in sorted(coord_mapping.keys()):
        x, y = coord_mapping[station]
        writer.writerow([station, x, y])

print(f"[OK] Created station_coords.csv with {len(coord_mapping)} station coordinates")
print(f"[*] Based on official SCR network map topology")
print(f"\n[STATS] Geographic distribution:")
print(f"   Airport cluster (x>20, y>6): {sum(1 for s, (x,y) in coord_mapping.items() if x > 20 and y > 6)}")
print(f"   Coastal line (y<3): {sum(1 for s, (x,y) in coord_mapping.items() if y < 3)}")
print(f"   Central hub (6<x<12, 5<y<8): {sum(1 for s, (x,y) in coord_mapping.items() if 6 < x < 12 and 5 < y < 8)}")
print(f"\n[SAMPLES] Sample coordinates:")
for station in ['Stepford Central', 'Benton', 'Airport Terminal 1', 'Llyn-by-the-Sea'][:4]:
    if station in coord_mapping:
        x, y = coord_mapping[station]
        print(f"   {station}: ({x}, {y})")
