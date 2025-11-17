# Route Corridor Calculator - Usage Guide for Custom GPT

## Overview

The `route_corridor_calculator.py` tool enables your Custom GPT to answer questions about which stations a service passes through and which ones it skips.

This implements **proper public transport routing logic** - no hardcoded corridors, everything calculated algorithmically from the network data.

## What It Does

For any route code (e.g., R026, R075), the calculator can tell you:

1. **All stations the service stops at** (the timetable stops)
2. **All stations on the corridor** (including intermediate stations served by other routes)
3. **Skipped stations** (stations on the corridor that this service doesn't stop at)
4. **Which other routes serve the skipped stations** (useful for connections)

## How It Works

### The Algorithm

```
For each route:
  1. Get the list of stops (from route data)
  2. For each consecutive pair of stops:
     a. Find ALL routes that connect those two stops
     b. Collect ALL stations served by ANY of those routes
     c. This gives us the "corridor" - the full set of possible stops
  3. Compare the corridor to the route's actual stops
  4. Skipped stations = stations in corridor but not in stops list
```

### Example: R076 (Leighton Express)

**Stops:** Stepford Central → St Helens Bridge → Benton → Leighton Stepford Road → Leighton City

**Corridor Analysis:**

- Between **Stepford Central → St Helens Bridge**:
  - R076 goes direct (express)
  - R026, R001, R002, etc. go via: Four Ways, Stepford East, Stepford High Street
  - **R076 skips:** Four Ways, Stepford East, Stepford High Street

- Between **St Helens Bridge → Benton**:
  - R076 goes direct (express)
  - R026, R001, R002, etc. go via: Angel Pass, Bodin, Coxly
  - **R076 skips:** Angel Pass, Bodin, Coxly

**Total skipped:** 12 stations

## Usage in Custom GPT

### Basic Query

When a user asks:
> "Which stations does R026 skip?"

**GPT should run:**
```python
from route_corridor_calculator import RouteCorridorCalculator

calc = RouteCorridorCalculator()
result = calc.calculate_route_corridor('R026')

if result:
    print(f"Route {result['route_code']} skips {len(result['skipped'])} stations:")
    for station in result['skipped']:
        print(f"  - {station}")
```

**Expected output:**
```
Route R026 skips 11 stations:
  - City Hospital
  - Financial Quarter
  - Four Ways
  - Stepford High Street
  - Angel Pass
  - Benton Bridge
  - Upper Staploe
  - Rocket Parade
  - Faymere
  - Millcastle Racecourse
  - Starryloch
```

### Detailed Report

For more comprehensive information:
```python
corridor = calc.calculate_route_corridor('R026')
print(calc.format_corridor_report(corridor, verbose=True))
```

This shows:
- Full corridor listing (all stations)
- Which stations are stops vs. skipped
- Segment-by-segment breakdown
- Which other routes serve the skipped stations

### Quick Skipped List

For a simple answer:
```python
skipped = calc.get_skipped_stations('R026')
print(f"R026 skips: {', '.join(skipped)}")
```

### Compare Two Services

To compare express vs. local service:
```python
comparison = calc.compare_services('R076', 'R026')
print(comparison)
```

Shows:
- How many stations each service stops at
- How many each service skips
- Common skipped stations
- Unique skipped stations

## Sample Questions & Answers

### Q: "Which stops does R026 skip?"

**GPT Response:**
```
R026 (Regional One) skips 11 stations along its corridor:

1. City Hospital - between Stepford Victoria and Stepford Central
2. Financial Quarter - between Stepford Victoria and Stepford Central
3. Four Ways - between Stepford Central and St Helens Bridge
4. Stepford High Street - between Stepford Central and St Helens Bridge
5. Angel Pass - between St Helens Bridge and Bodin
6. Benton Bridge - between Benton and Hampton Hargate
7. Upper Staploe - between Hampton Hargate and Water Newton
8. Rocket Parade - between Hampton Hargate and Leighton Stepford Road
9. Faymere - between Edgemead and Westercoast
10. Millcastle Racecourse - between Westercoast and Millcastle
11. Starryloch - between Westwyvern and Northshore

These stations are served by other routes on the same corridor.
```

### Q: "Does R075 stop at Stepford East?"

**GPT Response:**
```
No, R075 (Benton Express) does not stop at Stepford East.

R075 is an express service that runs directly from Stepford Central to Benton,
skipping 7 intermediate stations:
- Angel Pass
- Bodin
- Coxly
- Four Ways
- St Helens Bridge
- Stepford East
- Stepford High Street

For service to Stepford East, you can use:
- R001, R002, R003, R005, R006, R026, R032, R033, R035, R036, or R045
```

### Q: "What's the difference between R026 and R076?"

**GPT Response:**
```
R026 (Regional One) vs R076 (Leighton Express):

R026:
- Stops: 17 stations
- Corridor: 28 stations total
- Skips: 11 stations
- Travel time: 43 minutes (up) / 35 minutes (down)
- Price: 450 Points

R076:
- Stops: 5 stations
- Corridor: 17 stations total
- Skips: 12 stations
- Travel time: 12 minutes (up) / 13 minutes (down)
- Price: 300 Points

R076 is an express service that skips most intermediate stations,
while R026 is a semi-fast service that stops at more (but not all) stations.

Both skip some stations that are served by slower local services.
```

## CLI Usage

The calculator can also be run from the command line:

```bash
# Basic analysis
python3 route_corridor_calculator.py R026

# Verbose output with segment details
python3 route_corridor_calculator.py R026 --verbose

# Compare two routes
python3 route_corridor_calculator.py R076 R026
```

## Integration with Existing GPT Tools

This calculator **complements** the existing `rail_helpers.py`:

- **rail_helpers.py**: Journey planning, finding routes between stations
- **route_corridor_calculator.py**: Understanding what each individual route does

### Combined Example

User asks: "How do I get from Stepford Central to Bodin?"

**GPT workflow:**
```python
# 1. Find possible routes
from rail_helpers import *
graph, ops, lines = load_rail_network("rail_routes.csv")
services = direct_services_between(graph, "Stepford Central", "Bodin")

# 2. For each service, check if it actually stops at Bodin
from route_corridor_calculator import RouteCorridorCalculator
calc = RouteCorridorCalculator()

for service in services:
    route_code = service['line']
    corridor = calc.calculate_route_corridor(route_code)

    if 'Bodin' in corridor['stops']:
        print(f"{route_code}: Stops at Bodin ✓")
    elif 'Bodin' in corridor['corridor']:
        print(f"{route_code}: Passes Bodin but doesn't stop ✗")
```

## Adding to Custom GPT

### 1. Upload the File

Add `route_corridor_calculator.py` to your Custom GPT's knowledge files.

### 2. Update Instructions

Add this section to your Custom GPT instructions:

```markdown
## Route Corridor Analysis

When users ask about which stations a route skips or passes:

1. Use route_corridor_calculator.py to analyze the route
2. Import: `from route_corridor_calculator import RouteCorridorCalculator`
3. Create calculator: `calc = RouteCorridorCalculator()`
4. Get corridor data: `result = calc.calculate_route_corridor('R026')`

The result includes:
- `stops`: Stations where the service stops
- `corridor`: All stations on the corridor
- `skipped`: Stations passed but not stopped at

Sample queries:
- "Which stops does R026 skip?"
- "Does R075 stop at Bodin?"
- "What's the difference between R026 and R076?"
- "Show me all stations R078 passes through"

Always provide context about which other services serve the skipped stations.
```

### 3. Required Files

Make sure these files are uploaded to your GPT:

- `stepford_routes_with_segment_minutes_ai_knowledge_base.json` (route data)
- `route_corridor_calculator.py` (the calculator)
- `rail_helpers.py` (for journey planning)
- `rail_routes.csv` (for network queries)

## Technical Details

### Data Sources

The calculator uses the `connections` section of the JSON file, which shows:
- Which routes connect each pair of stations
- The specific service codes for each connection
- Travel times between stations

### Network Graph

The calculator builds a station network graph showing physical track connections.
This is used for pathfinding when needed, but the primary algorithm uses route
comparison to identify corridor stations.

### Algorithm Complexity

- **Time:** O(R × S²) where R = number of routes, S = max stations per route
- **Space:** O(N) where N = number of stations
- **Typical runtime:** < 100ms for a single route analysis

## Troubleshooting

### "Route not found"

- Check the route code spelling (case-sensitive: "R026" not "r026")
- Verify the route exists in the JSON file
- Some historical routes may be marked as REMOVED

### "No skipped stations" for an express service

This is correct if the express service uses a different physical corridor
than local services. For example:
- R075 goes direct Stepford Central → Benton (no skips on its corridor)
- R001 goes SC → Stepford East → ... → Benton (different corridor)

### Unexpected stations in corridor

The corridor includes all stations served by ANY route between the stops.
If multiple physical paths exist, all stations on all paths are included.

## Examples

### All-Stations Service

```python
corridor = calc.calculate_route_corridor('R001')
# Result: corridor == stops (no skips)
```

### Express Service

```python
corridor = calc.calculate_route_corridor('R075')
# Result: skips many stations between origin and destination
```

### Semi-Fast Service

```python
corridor = calc.calculate_route_corridor('R026')
# Result: skips some stations, stops at others
```

## Future Enhancements

Possible additions:
- Calculate which skipped stations have the most services (major hubs)
- Identify "limited stop" patterns (e.g., "skips all stations except major hubs")
- Generate natural language descriptions ("R026 is a semi-fast service...")
- Compare multiple routes at once (e.g., "show all express services to Benton")

---

**Ready to use!** 🚂

Your Custom GPT can now intelligently answer questions about route corridors
and skipped stations using real algorithmic analysis, not hardcoded data.
