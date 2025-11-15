# Pathfinding Systems Comparison Results

## Test Query: Benton → Llyn-by-the-Sea

### System 1: CSV System (rail_helpers.py)
- **Result**: 17.6 minutes with 1 transfer
- **Route**: R077 to Leighton City → transfer → R085 to Llyn
- **Algorithm**: Dijkstra's shortest path
- **Issue Found**: Chose suboptimal route due to transfer penalty calculation

### System 2: route_pathfinder.py (BFS Method 3)
- **Result**: 16.0 minutes direct (NO transfers!)
- **Route**: R078 direct (Benton → LSR → Leighton City → Westwyvern → Llyn)
- **Algorithm**: BFS with route filtering
- **Advantage**: Found the genuinely better passenger experience

### System 3: Simple JSON Filtering
- **Result**: Shows R078 as 20 min (total route time, not segment)
- **Limitation**: Can't calculate segment times accurately
- **Not recommended** for pathfinding

---

## Key Finding

**System 2 (route_pathfinder) found a better route than System 1!**

- System 1: 17.6 min with transfer (suboptimal)
- System 2: 16.0 min direct (optimal) ✅
- **Difference**: 11% faster, no transfers needed

---

## Why This Happened

System 1's Dijkstra algorithm:
1. Saw R077's short edges (2.8 min each) and started down that path
2. Added a 4-minute transfer penalty
3. Resulted in 17.6 minutes total

System 2's BFS:
1. Checked ALL routes from Benton to Llyn
2. Found R078 direct route = 16.0 minutes
3. Correctly identified it as best option

---

## Recommendation for Custom GPT

### 🏆 **BEST CHOICE: Use BOTH Systems**

#### **Primary System: CSV (rail_helpers.py)**
Upload for Custom GPT:
- `rail_routes.csv`
- `rail_helpers.py`
- `station_coords.csv`

**Use for**:
- Quick station info queries
- Operator/line lookups
- Network visualization
- General navigation

#### **Secondary System: route_pathfinder.py**
Upload additionally:
- `stepford_routes_with_segment_minutes_ai_knowledge_base.json`
- `route_pathfinder.py`

**Use for**:
- Finding optimal routes with detailed comparison
- Showing multiple route options
- When you need the absolute best route

---

## Custom GPT Instructions

Add this to your GPT instructions:

```python
# For route finding between stations:
import route_pathfinder
import json

# Load and find best routes
with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json') as f:
    data = json.load(f)

pathfinder = route_pathfinder.RoutePathfinder(data)
routes = pathfinder.find_routes("Station A", "Station B", top_n=5, max_transfers=2)

# Show top 3 options to user
for i, route in enumerate(routes[:3], 1):
    print(f"{i}. {pathfinder.format_route(route, verbose=True)}")
```

For other queries (station info, operators, lines), use rail_helpers functions.

---

## Performance Comparison

| Feature | CSV/rail_helpers | route_pathfinder |
|---------|------------------|------------------|
| **Speed** | Fast | Slower (50k routes searched) |
| **Accuracy** | ⚠️ Sub-optimal (transfer penalty issue) | ✅ Optimal |
| **Memory** | Low | High |
| **Route Options** | Single best (may be wrong) | All options |
| **Transfer Handling** | ✅ Supports | ✅ Supports |
| **Direct Routes** | ⚠️ May miss | ✅ Finds all |
| **Setup** | Simple | Medium |

---

## Final Verdict

### For Your Custom GPT: **Upload BOTH**

1. **Use route_pathfinder for journey planning** (more accurate)
2. **Use rail_helpers for everything else** (faster, easier)

This gives you:
- ✅ Best of both worlds
- ✅ Accurate route finding
- ✅ Fast station/operator queries
- ✅ Complete functionality

---

## Files to Upload

**Complete Setup (Recommended)**:
```
✅ rail_routes.csv (61 KB)
✅ rail_helpers.py (20 KB)
✅ station_coords.csv (1.8 KB)
✅ stepford_routes_with_segment_minutes_ai_knowledge_base.json (377 KB)
✅ route_pathfinder.py (7.1 KB)
```

**Minimal Setup (If file limit)**:
```
✅ stepford_routes_with_segment_minutes_ai_knowledge_base.json (377 KB)
✅ route_pathfinder.py (7.1 KB)
✅ rail_routes.csv (61 KB) - for station lookups
```

Total: ~470 KB (well under Custom GPT limits)
