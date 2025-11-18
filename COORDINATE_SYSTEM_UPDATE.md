# Station Coordinate System Update

**Date:** 2025-11-18
**Version:** Map-based v2.0
**Previous:** Random grid v1.0

---

## Overview

Updated the station coordinate system from **random alphabetical grid** to **actual network map topology** extracted from the official Stepford County Railway transit map.

---

## Changes Made

### 1. **Coordinate Extraction**
- ✅ Analyzed official SCR network map image
- ✅ Manually extracted station positions based on visual topology
- ✅ Created coordinate system matching actual game layout

### 2. **Files Updated**
- ✅ `station_coords.csv` - Now uses map-based positions
- ✅ `generate_coordinates.py` - Updated with map topology logic
- ✅ `station_coords_old_random.csv` - Backup of old random system
- ✅ `station_coords_actual_map.csv` - New map-based coordinates

### 3. **Coordinate System**

**New System:**
- **X-axis:** 0 (west/left) → 30 (east/right)
- **Y-axis:** 0 (south/bottom) → 12 (north/top)

**Geographic Regions:**
- **Airport Cluster** (x>20, y>6): 13 stations
  - Terminals 1/2/3, Airport Central, Airport West, Airport Parkway
  - Right-top quadrant matching actual map

- **Coastal Line** (y<3): 12 stations
  - Llyn-by-the-Sea → Northshore → Starryloch → Millcastle → Westercoast
  - Bottom strip matching western coastal route

- **Central Hub** (6<x<12, 5<y<8): 4 core stations
  - Stepford Central, Benton (major interchanges)
  - Center of network topology

---

## Before vs After

### Old System (Random Grid)
```python
# Alphabetical placement - no geographic meaning
Airport Terminal 1: (0.14, -0.47)
Airport Terminal 2: (1.78, -0.28)
Airport Terminal 3: (4.24, 0.18)
Benton: (20.31, 0.2)
Llyn-by-the-Sea: (5.76, 5.75)
```

**Problems:**
- ❌ Alphabetically sorted (Airport near A, Benton near B)
- ❌ Random offsets for "natural look"
- ❌ No relationship to actual network
- ❌ Airport terminals scattered
- ❌ Doesn't show divergent routes visually

### New System (Map-Based)
```python
# Topology-based positioning
Airport Terminal 1: (26, 8)   # Clustered together
Airport Terminal 2: (27, 9)   # in top-right
Airport Terminal 3: (28, 10)  # as on actual map
Benton: (16, 6)               # Central interchange
Llyn-by-the-Sea: (2, 1)       # Western coastal
```

**Benefits:**
- ✅ Matches official network map
- ✅ Airport terminals clustered (top-right)
- ✅ Coastal stations form western line
- ✅ Shows Hampton Hargate vs Morganstown split
- ✅ Realistic geographic relationships

---

## Visual Improvements

### Divergent Routes Now Visible!

The **Hampton Hargate vs Morganstown** split is now properly visualized:

```
From St Helens Bridge to Leighton:

ROUTE 1 (Top path via Hampton Hargate):
St Helens Bridge (12,7) → Hampton Hargate (24,4) → James Street (27,6) → Leighton

ROUTE 2 (Middle path via Morganstown):
St Helens Bridge (12,7) → Benton (16,6) → Morganstown (18,4) → Leighton
```

This matches what `route_corridor_calculator.py` detects algorithmically!

---

## Impact on System

### Files Affected ✅
- **plot_helpers.py** - Will generate realistic network maps
- **Visualization outputs** - Now show actual topology

### Files Unchanged ✅
- **route_pathfinder.py** - Uses graph structure (no change)
- **rail_helpers.py** - Uses CSV edges (no change)
- **route_corridor_calculator.py** - Algorithmic (no change)
- **JSON data** - Route data unchanged

---

## Key Coordinate Examples

### Airport Cluster (Top-Right)
```
Airport Terminal 3:    (28, 10)  ← Furthest right/top
Airport Terminal 2:    (27, 9)
Airport Terminal 1:    (26, 8)
Airport West:          (25, 7)
Stepford Airport Central: (23, 8)
Airport Parkway:       (21, 7)
```

### Coastal Line (Bottom)
```
Llyn-by-the-Sea:  (2, 1)   ← Far west
Westwyvern:       (6, 1)
Northshore:       (4, 1)
Starryloch:       (5, 1)
Millcastle:       (7, 2)
Westercoast:      (8, 2)
```

### Central Hub
```
Stepford Central:  (7, 7)   ← Major hub
Benton:           (16, 6)   ← Major interchange
Stepford East:    (11, 7)
Financial Quarter: (2, 7)
```

### Divergent Corridors
```
Hampton Hargate:  (24, 4)   ← Eastern branch
Morganstown:      (18, 4)   ← Central branch
(Visually distinct paths now!)
```

---

## Testing

### Run Coordinate Generator
```bash
cd C:\Users\sydne\Documents\GitHub\edw
python generate_coordinates.py
```

**Expected Output:**
```
[OK] Created station_coords.csv with 71 station coordinates
[*] Based on official SCR network map topology

[STATS] Geographic distribution:
   Airport cluster (x>20, y>6): 13
   Coastal line (y<3): 12
   Central hub (6<x<12, 5<y<8): 4

[SAMPLES] Sample coordinates:
   Stepford Central: (7, 7)
   Benton: (16, 6)
   Airport Terminal 1: (26, 8)
   Llyn-by-the-Sea: (2, 1)
```

### Test Visualization
```python
import rail_helpers
import plot_helpers

graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
coords = plot_helpers.load_station_coords("station_coords.csv")

# Should now show realistic topology!
plot_helpers.plot_full_network(graph, coords)
```

---

## Backward Compatibility

Old random coordinates preserved in:
- `station_coords_old_random.csv`

To revert (not recommended):
```bash
copy station_coords_old_random.csv station_coords.csv
```

---

## Future Enhancements

Potential improvements:
1. **Fine-tune positions** - Adjust based on actual pixel measurements from map image
2. **Line curvature** - Add intermediate points for curved routes
3. **Auto-extraction** - Image processing to extract coordinates automatically
4. **3D elevation** - Add z-coordinate for elevation data if available

---

## References

- **Source:** Official Stepford County Railway network map (provided 2025-11-18)
- **Coordinate System:** Custom 30x12 grid matching map aspect ratio
- **Station Count:** 71 stations mapped
- **Coverage:** 100% of network stations positioned

---

## Summary

**Before:** Random alphabetical grid (no geographic meaning)
**After:** Map-based topology (matches actual game layout)
**Result:** Visualizations now accurately represent SCR network geography! ✨

The corridor calculator's algorithmic detection now has a matching visual representation.
