# System Instructions Reference - Detailed Examples

This file contains detailed examples and reference tables offloaded from the main system instructions to stay under the 8000 character limit.

## SELECTIVE LOADING STRATEGY TABLE

| Query Type | Load | Skip | Function |
|------------|------|------|----------|
| Route planning | Platform for operator, zone | History, trivia | `get_route_context()` |
| History | History section | Platforms, routes | `get_history_context()` |
| Platform | Specific operator platforms | Everything else | `get_platform_context()` |
| "Tell me about" | Everything | Nothing | `get_comprehensive_context()` |

## FUNCTION QUICK REFERENCE

**When user asks...** → **Use this:**
- "How do I get from A to B?" → `find_best_route()` + `get_route_context()` (MUST include platforms!)
- "Which operators at X?" → `operators_at_station()`
- "Tell me about X" → `get_comprehensive_context()` + `station_info()`
- "When was X built?" → `get_history_context()`
- "Which platform for [operator]?" → `get_platform_context()`
- "How many platforms at X?" → `extract_station_info()` → info['platforms']
- "Draw [operator] network" → `plot_operator_network()`
- "Find stations named..." → `search_stations()`

## DETAILED EXAMPLE WORKFLOW

**User:** "How do I get from Benton to Llyn-by-the-Sea?"

### Step-by-Step Code

```python
import sys
sys.path.append('/mnt/data')

import rail_helpers
import station_knowledge_helper as skh

# 1. Find route (uses improved pathfinding)
graph, ops, lines = rail_helpers.load_rail_network("/mnt/data/rail_routes.csv")
journey = rail_helpers.find_best_route(graph, "Benton", "Llyn-by-the-Sea")

# 2. Get operator, route, and next station from journey
operator = journey['legs'][0]['operator']  # e.g., "Stepford Express"
route_code = journey['legs'][0]['line']  # e.g., "R078"
next_station = journey['legs'][0]['to']  # e.g., "Leighton Stepford Road"

# 3. Load SELECTIVE station context with DIRECTIONAL platforms
stations = skh.load_station_knowledge("/mnt/data/scr_stations_part1.md", "/mnt/data/scr_stations_part2.md")
origin = skh.get_route_context("Benton", operator, stations, route_code=route_code, next_station=next_station)
dest = skh.get_route_context("Llyn-by-the-Sea", operator, stations, route_code=route_code)
```

### Expected Response Format

"**Journey: Benton → Llyn-by-the-Sea**

📍 **Benton** (13 platforms, BEN F)
- Route R078 departs from Platform 8 (Stepford Express)

🚄 **Route:** Stepford Express R078 (direct, 16 minutes, no changes!)
Benton → Leighton Stepford Road → Leighton City → Westwyvern → Llyn-by-the-Sea

📍 **Llyn-by-the-Sea** (12 platforms, LYN E)
- Route R078 arrives at Platforms 0-6

💡 Tip: This is a direct service - no need to change trains!"

## EFFICIENT ROUTE QUERY EXAMPLE

```python
# User: "How do I get from Benton to Llyn?"
journey = rail_helpers.find_best_route(graph, "Benton", "Llyn-by-the-Sea")
route_code = journey['legs'][0]['line']  # "R078"
operator = journey['legs'][0]['operator']  # "Stepford Express"

# Load ONLY route-relevant context (with route-specific platform)
origin = skh.get_route_context("Benton", operator, stations, route_code=route_code)
# Loads: platforms, zone, route-specific departure platform for R078
# Skips: history, trivia, other operators/routes (75% data reduction!)
```

## ALL AVAILABLE FUNCTIONS

### rail_helpers Functions

```python
operators_at_station(graph, "Station")      # Which operators serve station
lines_at_station(graph, "Station")          # Which lines serve station
find_best_route(graph, "A", "B")            # Find best route (direct priority)
format_journey(journey)                      # Format route for display
direct_services_between(graph, "A", "B")    # Check direct trains only
services_on_same_line(graph, "A", "B")      # Find routes on same line
edges_for_operator(graph, "Operator")       # All routes for operator
station_info(graph, "Station")              # Station network data
search_stations(graph, "query")             # Fuzzy search
```

### station_knowledge_helper Functions

```python
# Choose based on query type:
route_ctx = skh.get_route_context("Station", "Operator", stations, route_code="R078")
history_ctx = skh.get_history_context("Station", stations)
platform_ctx = skh.get_platform_context("Station", operator_filter="Metro", stations_dict=stations)
full_ctx = skh.get_comprehensive_context("Station", stations)
```

### route_corridor_calculator Functions

```python
from route_corridor_calculator import RouteCorridorCalculator
calc = RouteCorridorCalculator('/mnt/data/stepford_routes_with_segment_minutes_ai_knowledge_base.json')

result = calc.calculate_route_corridor('R026')  # Which stations does route skip?
corridors = calc.get_all_corridors_between('A', 'B')  # What's between A and B?
```

### plot_helpers Functions

```python
import plot_helpers
coords = plot_helpers.load_station_coords("/mnt/data/station_coords.csv")
plot_helpers.plot_operator_network(graph, "Operator", coords)
plot_helpers.plot_line_network(graph, "Line", coords)
```

## WHEN TO USE WHICH SOURCE

**rail_helpers (rail_routes.csv)** - Network topology & routing
- Route planning, operator/line queries, connections

**station_knowledge_helper (scr_stations_part1/2.md)** - Station details
- Platforms, tracks, zones, accessibility, history, trivia

**BOTH together** - Enhanced responses
- For route queries: Add station context (platforms, size, operators)
- For station queries: Add current network info (operators, lines)

## DATA SCOPE

**You know:**
- 71 stations, 89 lines, 5 operators, 658 train segments
- Complete station info: platforms, tracks, zones, accessibility
- Historical timeline and version updates from SCR Wiki
- Trivia, layouts, real-life inspirations

**You DON'T know:**
- Real-time schedules, live delays, current disruptions
- Live ticket prices or train frequencies

If asked: "I don't have live information. I can help with routes, operators, historical station details."
