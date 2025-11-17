# Changelog - Custom GPT Smart Selective Loading

All notable changes and improvements to the Stepford County Railway Custom GPT system.

---

## [2.2.0] - 2024-11-17

### Added - Bidirectional Platform Mapping ⭐⭐⭐

**Feature:** Directional (route + destination) platform lookup for bidirectional tracks.

**Why This Matters:**
At stations with bidirectional tracks, the SAME route uses DIFFERENT platforms depending on travel direction:
- R083 TO Llyn-by-the-Sea → Platform 2
- R083 TO Newry → Platforms 2-3

Without directional mapping, the system could only say "R083 uses Platforms 2, 2-3" (ambiguous).
Passengers wouldn't know which platform for their specific direction!

**New Functions:**
- `build_directional_platform_map(station_data)` - Parses "R### to Destination" patterns from Services section
  - Returns: `{('R083', 'Llyn-by-the-Sea'): ['2'], ('R083', 'Newry'): ['2-3']}`

- Updated `get_route_platform(station_data, route_code, next_station=None)` - Now accepts next_station parameter
  - Priority: directional > route-specific > non-directional

- Updated `get_route_context(..., next_station=None)` - Accepts next_station for directional lookup
  - Three priority levels:
    1. Directional (route + next_station): "R083 to Llyn → Platform 2"
    2. Route-specific (route only): "R083 → Platforms 2, 2-3"
    3. Operator-level (fallback): "Stepford Express → Platforms 7-10"

**Usage Example:**
```python
# Get directional platform (most accurate)
journey = find_best_route(graph, "Benton", "Llyn")
next_station = journey['legs'][0]['to']  # "Leighton Stepford Road"
ctx = get_route_context("Benton", operator, stations, route_code="R083", next_station=next_station)
print(ctx['departure_platforms'])  # "Platform 2" (directional - exact!)

# Without direction (less accurate)
ctx = get_route_context("Benton", operator, stations, route_code="R083")
print(ctx['departure_platforms'])  # "Platforms 2, 2-3" (ambiguous)
```

**Before vs After:**
```
Before: "Take R083 from Platforms 2, 2-3"  ❌ Passenger confused!
After:  "Take R083 to Llyn from Platform 2"  ✅ Clear guidance!
```

**Technical Details:**
- Regex pattern: `r'(R\d+)\s+to\s+([\w\s\-]+?)(?=\s+\w+\s+R\d+|$)'`
- Handles format: "R083 to Llyn-by-the-Sea Morganstown R084..."
- Fuzzy matching: "Llyn-by-the-Sea" matches "Llyn" or "Llyn by the Sea"

**Commits:**
- `464deb9` - Add bidirectional platform mapping for accurate directional guidance

---

## [2.1.0] - 2024-11-17

### Added - Route-Specific Platform Mapping ⭐

**Feature:** Granular route-to-platform lookup instead of operator-level grouping.

**Why This Matters:**
At stations like Benton Bridge, different routes of the same operator use different platforms:
- Airport routes (R001, R046, R048) → Platforms 1, 4
- Other Connect routes (R003, R024, R025) → Platforms 2, 3

Previously, the system only knew "Stepford Connect uses Platforms 2, 4" (operator-level).
Now it can tell you "R001 departs from Platforms 1, 4" (route-specific).

**New Functions:**
- `build_route_platform_map(station_data)` - Parses Services section to map routes to platforms
- `get_route_platform(station_data, route_code)` - Get specific platforms for a route code
- `get_route_context()` - Now accepts optional `route_code` parameter

**Usage Example:**
```python
# Get route-specific platform
ctx = get_route_context("Benton Bridge (Station)", "Stepford Connect", stations, route_code="R001")
print(ctx['departure_platforms'])  # "Platforms 1, 4"

# Falls back to operator-level if route_code not provided
ctx = get_route_context("Benton Bridge (Station)", "Stepford Connect", stations)
print(ctx['departure_platforms'])  # "Platforms 2, 4"
```

**Handles Both Platform Formats:**

1. **Individual Platforms** (Benton Bridge):
   - Format: `"1 Benton R001 R005..."`, `"2 R003 R039..."`
   - Result: R001 → "Platforms 1, 4"

2. **Platform Ranges** (Benton):
   - Format: `"4-7 Coxly R001 R005..."`, `"10-13 R078..."`
   - Result: R001 → "Platforms 4-7, 10-13"

**Commits:**
- `07eb228` - Add route-specific platform mapping for accurate guidance
- `d14ce04` - Handle platform ranges in route-specific platform mapping

---

## [2.0.1] - 2024-11-17

### Fixed - Operator-Platform Mapping with Route Number Heuristics

**Problem:**
- Llyn-by-the-Sea showed only "Stepford Express: Platforms 0-6"
- Missing "Stepford Connect: Platforms 7-11"
- Voting system incorrectly assigned Connect routes (R024, R026) to Express based on proximity

**Solution:**
- Implemented strong route number heuristics:
  - R001-R050 → Stepford Connect/Metro/Waterline
  - R075-R099 → Stepford Express
  - R100+ → Check content for operator
- Changed from greedy regex to segment-based parsing (splits by platform ranges)
- Fixed voting system to prioritize route ranges over proximity matching

**Results:**
- ✅ Llyn: Express (0-6), Connect (7-11)
- ✅ Benton: Waterline (1-3), Connect (4-6, 11-13), Express (7-10)
- ✅ Stepford Central: Express (0-3), Connect (4-9, 12-15)

**Commit:** `ce9a518` - Fix operator-platform mapping using route number heuristics

---

## [2.0.0] - 2024-11-17

### Added - Improved Pathfinding (Direct Route Priority)

**Problem:**
- Benton → Llyn showing 17.6 min with 1 transfer
- Should show 16 min direct on R078
- Dijkstra algorithm preferred shorter segments over continuous direct routes

**Solution:**
- Created `find_best_route()` wrapper function with two-step approach:
  1. Check for direct routes on same line (using BFS)
  2. Fall back to Dijkstra for multi-leg journeys
- Improved `services_on_same_line()` to trace actual paths using BFS

**Results:**
- ✅ Benton → Llyn: 16.0 min direct (R078, 0 transfers)
- ✅ Multi-transfer routes still work correctly
- ✅ All references in instructions updated

**Commit:** `4a0ef03` - Fix pathfinding to prioritize direct routes over transfers

---

## [1.1.1] - 2024-11-17

### Fixed - Platform Count Extraction

**Problem:**
- Llyn-by-the-Sea showing "Platforms: 0" instead of 12
- Benton showing "NOT FOUND"
- Regex matching "Platform 0" before "Platforms 12"

**Solution:**
```python
# Find ALL "Platforms X" matches and take the largest (total count)
platform_matches = re.findall(r'Platforms\s+(\d+)', content, re.IGNORECASE)
if platform_matches:
    info['platforms'] = max(platform_matches, key=int)
```

**Results:**
- ✅ Benton: 13 platforms
- ✅ Llyn: 12 platforms
- ✅ All 82 stations now extract correctly

**Commit:** `ed6db03` - Improve platform extraction from dense wiki content

---

## [1.1.0] - 2024-11-17

### Added - Compact Instructions (Under 8,000 Character Limit)

**Problem:**
- `custom_gpt_instructions_with_station_knowledge.txt` = 14,267 chars
- Custom GPT limit = 8,000 chars
- Instructions too long to upload

**Solution:**
- Created `custom_gpt_instructions_COMPACT.txt` (6,680 chars - 53% reduction)
- Moved detailed examples to `GPT_USAGE_GUIDE.md` as knowledge file
- GPT references usage guide when needed

**Benefits:**
- ✅ Fits under character limit
- ✅ Preserves all functionality
- ✅ More maintainable (examples in separate file)

**Commit:** (Part of consolidation work)

---

## [1.0.0] - Initial Release

### Features
- Smart Selective Loading (75-98% data reduction)
- Query-type detection:
  - `get_route_context()` - Route planning
  - `get_history_context()` - Historical queries
  - `get_platform_context()` - Platform queries
  - `get_comprehensive_context()` - Full details
- Operator-level platform mapping
- Dijkstra pathfinding
- 82 stations, 89 lines, 5 operators

---

## Summary of All Improvements

| Version | Feature | Impact |
|---------|---------|--------|
| 2.2.0 | Bidirectional platforms | ⭐⭐⭐ Directional accuracy (R083 to Llyn → Platform 2, to Newry → 2-3) |
| 2.1.0 | Route-specific platforms | ⭐ Route precision (R001 → Platform 1,4 vs all Connect → 2,4) |
| 2.0.1 | Operator-platform heuristics | Fixed Llyn showing both Express and Connect platforms |
| 2.0.0 | Direct route priority | Benton→Llyn now shows 16min direct (was 17.6min transfer) |
| 1.1.1 | Platform count extraction | All 82 stations show correct platform count |
| 1.1.0 | Compact instructions | Fits 8,000 char limit (was 14,267 chars) |

---

## Breaking Changes

None! All changes are backward compatible with fallback mechanisms.

---

## Upgrade Path

If using an older version:

1. **Replace files:**
   - `station_knowledge_helper.py` (new functions added)
   - `rail_helpers.py` (if using improved pathfinding)
   - `custom_gpt_instructions_COMPACT.txt` (updated workflow)

2. **Update Custom GPT:**
   - Re-upload the 3 files above
   - Instructions now use `route_code` parameter

3. **Test:**
   - Query: "How do I get from Benton Bridge to Airport?"
   - Should show route-specific platform (e.g., "R001 from Platforms 1, 4")

---

## Technical Details

### Route-Specific Platform Parsing

**Services Section Format 1 (Individual Platforms):**
```
Platform(s) Previous station Route Next station
1 Benton R001 R005 R033 to Airport Central
2 R003 R039 R045 to Leighton City
```

**Services Section Format 2 (Platform Ranges):**
```
Platform(s) Previous station Route Next station
1-2 West Benton R010 to Greenslade
4-7 Coxly R001 R005 R033 to Stepford Airport Central
```

**Regex Pattern:**
```python
# Matches both individual platforms and ranges
plat_match = re.match(r'^(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\s+', segment)

# Splits by platform entries (handles both formats)
segments = re.split(r'\s+(?=\d+(?:-\d+)?\s+[A-Z])', services_text)
```

**Result Dictionary:**
```python
{
    'R001': ['4-7', '10-13'],  # Platform ranges
    'R003': ['2', '3'],         # Individual platforms
    'R078': ['2', '10-13']      # Mixed
}
```

---

## Future Enhancements (Planned)

- [ ] Add real-time service updates
- [ ] Include fare information
- [ ] Accessibility routing (avoid stairs)
- [ ] Peak/off-peak service frequencies
- [ ] Station facility details (shops, toilets, etc.)

---

## Contributors

Developed by Claude (Anthropic) for Stepford County Railway Custom GPT project.

---

## License

This is documentation for a Custom GPT knowledge base. Use as needed for your SCR railway assistant.
