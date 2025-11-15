# Stepford County Railway - Route Data Update Guide

## 🎯 Purpose

This guide helps you systematically update all 89 routes in the JSON file with accurate data from the SCR wiki or game.

## 📊 Current Status

- ✅ **R081** - Fixed (Stepford Central → Leighton City → Llyn-by-the-Sea)
- ✅ **R083** - Fixed (Newry → ... → Llyn-by-the-Sea, 8 stations)
- ✅ **R085** - Fixed (Benton → ... → Llyn-by-the-Sea, 6 stations)
- ⏳ **R001-R089** - 86 routes remaining to verify/update

## 🔍 What We Found

### The Good News
- The pathfinding algorithm (Dijkstra's) works perfectly
- The edge-based graph model is correct
- The system correctly finds optimal routes

### The Issue
- Some routes have incomplete/simplified station lists
- Travel times may be estimates rather than actual
- Some routes may be outdated (game updates change routes)

## 📝 Route Information Sources

### Primary Source: SCR Wiki
- Main route list: https://scr.fandom.com/wiki/List_of_Routes
- Individual route pages: https://scr.fandom.com/wiki/List_of_Routes/R###
- Each route page contains:
  - Complete station list in order
  - Operator
  - Route type/name
  - Travel time
  - Price
  - Distance

### Secondary Source: In-Game
- Play Stepford County Railway on Roblox
- Check route boards at stations
- Time actual journeys

## 🛠️ How to Update Routes

### Method 1: Using the update_routes.py Script

```python
from update_routes import load_json, update_route, save_json

# Load data
data = load_json()

# Update a route
data = update_route(data, "R###",
    stations=["Station 1", "Station 2", ...],
    operator="Stepford Express",
    route_type="Express Service",
    travel_time={"up": "XX minutes", "down": "XX minutes"},
    price="XXX Points"
)

# Save
save_json(data)
```

### Method 2: Direct JSON Editing

1. Open `stepford_routes_with_segment_minutes_ai_knowledge_base.json`
2. Find the route (e.g., "R001")
3. Update the fields:
   - `stations`: Complete list in order [" Station1", "Station 2", ...]
   - `travel_time`: {"up": "XX minutes", "down": "XX minutes"}
   - `operator`: e.g., "Stepford Express"
   - `route_type`: e.g., "Airport Connect"
   - `price`: e.g., "450 Points"
   - `stops`: Number of stations (auto-calculated if using script)

### Method 3: Batch Updates from CSV

1. Create a CSV with route updates:
```csv
route_id,operator,origin,destination,route_type,travel_time_up,travel_time_down,price,stations
R001,Stepford Connect,Stepford Central,Airport,Airport Connect,18,18,450,"Stepford Central;Stepford East;..."
```

2. Use batch import script (see `batch_import_routes.py`)

## 📋 Route Update Checklist

For each route, verify:
- [ ] Complete station list (in correct order)
- [ ] Accurate travel time (up and down directions)
- [ ] Correct operator
- [ ] Route type/name matches wiki
- [ ] Price is current
- [ ] Origin and destination stations are correct

## 🔄 Workflow

### Step 1: Gather Data
For each batch of 10 routes:
1. Visit wiki pages for R001-R010
2. Copy station lists
3. Note travel times, operators, prices

### Step 2: Update JSON
```bash
# Edit routes using the script
python3 update_routes.py

# Or edit JSON directly
nano stepford_routes_with_segment_minutes_ai_knowledge_base.json
```

### Step 3: Regenerate CSV
```bash
python3 convert_to_edges.py
```

### Step 4: Test
```bash
python3 -c "
import rail_helpers
graph, ops, lines = rail_helpers.load_rail_network('rail_routes.csv')

# Test a specific route
journey = rail_helpers.shortest_path(graph, 'Station A', 'Station B')
print(rail_helpers.format_journey(journey))

# Check services on same line
same_line = rail_helpers.services_on_same_line(graph, 'Station A', 'Station B')
for svc in same_line:
    print(f'{svc[\"line\"]}: {svc[\"operator\"]}')
"
```

### Step 5: Commit
```bash
git add stepford_routes_with_segment_minutes_ai_knowledge_base.json rail_routes.csv
git commit -m "Update routes R###-R###"
```

## 📑 Route Batches

### Batch 1: R001-R020 (Stepford Connect/Express)
Focus: Core network routes

### Batch 2: R021-R040 (Metro/Connect)
Focus: Metro and regional routes

### Batch 3: R041-R060 (Express/AirLink)
Focus: Airport and express services

### Batch 4: R061-R089 (Mixed)
Focus: Specialty routes

## ⚠️ Known Issues to Fix

### Routes with Missing Intermediate Stations
Many routes show only origin → intermediate → destination, but actually stop at more stations.

**Example:**
- Current: `["Stepford Central", "Morganstown", "Llyn-by-the-Sea"]`
- Actual: `["Stepford Central", "Station X", "Station Y", "Morganstown", "Station Z", "Llyn-by-the-Sea"]`

### Routes with Estimated Times
Travel times were calculated as `total_time / (stations - 1)`, giving equal time per segment.

**Fix:** Use actual segment times from wiki/game

### Outdated Route Data
SCR game receives updates that change routes. Data may be from an older version.

**Fix:** Cross-reference with current wiki

## 🎯 Priority Routes to Fix

Based on importance/usage:

1. **High Priority** (Main network):
   - R001-R010 (Core Stepford Connect)
   - R075-R088 (Stepford Express main routes)
   - R051-R062 (AirLink airport services)

2. **Medium Priority** (Regional):
   - R020-R036 (Metro and regional)
   - R011-R019 (Connect services)

3. **Low Priority** (Specialty):
   - Remaining routes

## 📊 Validation

After updates, run validation:

```bash
python3 -c "
import json

with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json') as f:
    data = json.load(f)

issues = []
for rid, route in data['routes'].items():
    # Check for issues
    if len(route['stations']) < 2:
        issues.append(f'{rid}: Less than 2 stations')
    if route['stops'] != len(route['stations']):
        issues.append(f'{rid}: Stops count mismatch')

if issues:
    print('❌ Issues found:')
    for issue in issues:
        print(f'  - {issue}')
else:
    print('✅ All routes validated')
"
```

## 💡 Tips

1. **Work in batches** - Update 5-10 routes at a time
2. **Test frequently** - Regenerate CSV and test after each batch
3. **Keep backups** - The script creates `*_backup.json` automatically
4. **Use wiki search** - Search "SCR R### route" to find specific pages quickly
5. **Check both directions** - Some routes have different times up vs. down

## 🚀 Automated Approach (Future)

If you have access to the game's data files or API:
1. Extract route data programmatically
2. Convert to JSON format
3. Bulk import

## 📞 Need Help?

- SCR Wiki: https://scr.fandom.com/wiki/
- SCR Discord: (if available)
- Reddit: r/StepfordCountyRailway (if exists)

---

**Start with:** Routes R001-R010
**Tools:** `update_routes.py`, text editor, SCR wiki
**Goal:** Accurate, complete route data for all 89 routes
