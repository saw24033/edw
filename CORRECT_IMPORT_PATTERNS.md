# Correct Import Patterns for Custom GPT Code Interpreter

**Updated:** 2025-11-18
**Environment:** ChatGPT Code Interpreter (`/mnt/data/`)

---

## The Problem

Python doesn't automatically search `/mnt/data/` for custom modules in the Code Interpreter environment.

### ❌ What DOESN'T Work

```python
# This FAILS - Python can't find the module
from route_corridor_calculator import RouteCorridorCalculator
calc = RouteCorridorCalculator()
```

**Error:**
```
ModuleNotFoundError: No module named 'route_corridor_calculator'
```

---

## The Solution

**ALWAYS add `/mnt/data/` to `sys.path` FIRST, then import:**

```python
import sys
sys.path.append('/mnt/data')

# Now imports work!
from route_corridor_calculator import RouteCorridorCalculator
```

---

## Correct Usage Patterns

### 1. Route Corridor Calculator

```python
import sys
sys.path.append('/mnt/data')

from route_corridor_calculator import RouteCorridorCalculator

# IMPORTANT: Provide FULL path to JSON file
calc = RouteCorridorCalculator('/mnt/data/stepford_routes_with_segment_minutes_ai_knowledge_base.json')

# Now use it
result = calc.calculate_route_corridor("R026")
result
```

**Why the full path?**
- The calculator opens the JSON file in its `__init__` method
- Without the full path, it looks in the current directory (not `/mnt/data/`)

---

### 2. Rail Helpers (Network Analysis)

```python
import sys
sys.path.append('/mnt/data')

import rail_helpers

# Load network with FULL path
graph, operators, lines = rail_helpers.load_rail_network("/mnt/data/rail_routes.csv")

# Find routes
journey = rail_helpers.shortest_path(graph, "Benton", "Llyn-by-the-Sea")
print(rail_helpers.format_journey(journey))
```

---

### 3. Station Knowledge Helper

```python
import sys
sys.path.append('/mnt/data')

import station_knowledge_helper as skh

# Load station data with FULL paths
stations = skh.load_station_knowledge(
    "/mnt/data/scr_stations_part1.md",
    "/mnt/data/scr_stations_part2.md"
)

# Get station details
benton = skh.get_station_details("Benton", stations)
print(benton['summary'])
```

---

### 4. Plot Helpers (Visualization)

```python
import sys
sys.path.append('/mnt/data')

import rail_helpers
import plot_helpers

# Load network
graph, _, _ = rail_helpers.load_rail_network("/mnt/data/rail_routes.csv")

# Load coordinates
coords = plot_helpers.load_station_coords("/mnt/data/station_coords.csv")

# Generate map
plot_helpers.plot_operator_network(graph, "Stepford Express", coords)
```

---

## Complete Working Example

Here's a FULL working example that combines everything:

```python
# STEP 1: Add /mnt/data to Python path
import sys
sys.path.append('/mnt/data')

# STEP 2: Import modules (now they're found!)
import rail_helpers
import station_knowledge_helper as skh
from route_corridor_calculator import RouteCorridorCalculator

# STEP 3: Load data with FULL paths
graph, operators, lines = rail_helpers.load_rail_network("/mnt/data/rail_routes.csv")
stations = skh.load_station_knowledge(
    "/mnt/data/scr_stations_part1.md",
    "/mnt/data/scr_stations_part2.md"
)
calc = RouteCorridorCalculator('/mnt/data/stepford_routes_with_segment_minutes_ai_knowledge_base.json')

# STEP 4: Query the data
# Example: "How do I get from Benton to Llyn, and which stations does the route skip?"

# Find best route
journey = rail_helpers.shortest_path(graph, "Benton", "Llyn-by-the-Sea")
route_code = journey['legs'][0]['line']  # e.g., "R078"

# Check what it skips
corridor = calc.calculate_route_corridor(route_code)

# Get platform info for departure station
operator = journey['legs'][0]['operator']
departure_info = skh.get_route_context("Benton", operator, stations, route_code=route_code)

# Display results
print(f"Route: {route_code} ({corridor['route_type']})")
print(f"From: {corridor['origin']} → {corridor['destination']}")
print(f"Travel time: {journey['total_time']:.1f} minutes")
print(f"Depart from: {departure_info.get('departure_platforms', 'Platform info not available')}")
print(f"\nStops at {len(corridor['stops'])} stations:")
for stop in corridor['stops']:
    print(f"  - {stop}")
print(f"\nSkips {len(corridor['skipped'])} stations:")
for skip in corridor['skipped']:
    print(f"  - {skip}")
```

**Expected Output:**
```
Route: R078 (Benton Express via Leighton)
From: Benton → Llyn-by-the-Sea
Travel time: 16.0 minutes
Depart from: Platform 10

Stops at 5 stations:
  - Benton
  - Leighton Stepford Road
  - Leighton City
  - Westwyvern
  - Llyn-by-the-Sea

Skips 3 stations:
  - Edgemead
  - Westercoast
  - Northshore
```

---

## Common Mistakes and Fixes

### Mistake 1: Forgetting sys.path

```python
# ❌ WRONG - No sys.path setup
from route_corridor_calculator import RouteCorridorCalculator
```

```python
# ✅ CORRECT
import sys
sys.path.append('/mnt/data')
from route_corridor_calculator import RouteCorridorCalculator
```

---

### Mistake 2: Relative Paths

```python
# ❌ WRONG - Relative path won't work
calc = RouteCorridorCalculator('stepford_routes_with_segment_minutes_ai_knowledge_base.json')
```

```python
# ✅ CORRECT - Full absolute path
calc = RouteCorridorCalculator('/mnt/data/stepford_routes_with_segment_minutes_ai_knowledge_base.json')
```

---

### Mistake 3: Missing File Extensions

```python
# ❌ WRONG - Missing .md extension
stations = skh.load_station_knowledge("scr_stations_part1", "scr_stations_part2")
```

```python
# ✅ CORRECT - Include .md
stations = skh.load_station_knowledge(
    "/mnt/data/scr_stations_part1.md",
    "/mnt/data/scr_stations_part2.md"
)
```

---

## Files in /mnt/data/

When uploaded to Custom GPT, these files are accessible:

### Core Modules (Python)
- `rail_helpers.py`
- `station_knowledge_helper.py`
- `route_corridor_calculator.py`
- `plot_helpers.py`

### Data Files
- `rail_routes.csv`
- `station_coords.csv`
- `stepford_routes_with_segment_minutes_ai_knowledge_base.json`
- `scr_stations_part1.md`
- `scr_stations_part2.md`

### Documentation
- `GPT_USAGE_GUIDE.md`
- `ROUTE_CORRIDOR_CALCULATOR_GUIDE.md`
- `CHANGELOG.md`
- `GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt`

---

## Template for GPT Instructions

Copy this into your Custom GPT instructions:

```
## PYTHON SETUP (CRITICAL!)

**All files are in /mnt/data/ - ALWAYS start with:**

```python
import sys
sys.path.append('/mnt/data')
```

Then import modules and load data with FULL paths:

```python
import rail_helpers
import station_knowledge_helper as skh
from route_corridor_calculator import RouteCorridorCalculator

# Load with absolute paths
graph, operators, lines = rail_helpers.load_rail_network("/mnt/data/rail_routes.csv")
stations = skh.load_station_knowledge("/mnt/data/scr_stations_part1.md", "/mnt/data/scr_stations_part2.md")
calc = RouteCorridorCalculator('/mnt/data/stepford_routes_with_segment_minutes_ai_knowledge_base.json')
```
```

---

## Troubleshooting

### Error: "ModuleNotFoundError"
**Solution:** Add `sys.path.append('/mnt/data')` before importing

### Error: "FileNotFoundError: stepford_routes..."
**Solution:** Use full path: `/mnt/data/stepford_routes_with_segment_minutes_ai_knowledge_base.json`

### Error: "No such file or directory: 'scr_stations_part1.md'"
**Solution:** Use full paths: `/mnt/data/scr_stations_part1.md`

---

## Quick Reference Card

| Task | Correct Pattern |
|------|----------------|
| **Setup** | `sys.path.append('/mnt/data')` |
| **Rail helpers** | `rail_helpers.load_rail_network("/mnt/data/rail_routes.csv")` |
| **Station data** | `skh.load_station_knowledge("/mnt/data/scr_stations_part1.md", "/mnt/data/scr_stations_part2.md")` |
| **Corridor calc** | `RouteCorridorCalculator('/mnt/data/stepford_routes_with_segment_minutes_ai_knowledge_base.json')` |
| **Coordinates** | `plot_helpers.load_station_coords("/mnt/data/station_coords.csv")` |

---

## Summary

1. **ALWAYS** start with `sys.path.append('/mnt/data')`
2. **ALWAYS** use full paths starting with `/mnt/data/`
3. **NEVER** use relative paths or assume current directory
4. The RouteCorridorCalculator needs the JSON path in its constructor

Follow these patterns and your Custom GPT will work perfectly! ✨
