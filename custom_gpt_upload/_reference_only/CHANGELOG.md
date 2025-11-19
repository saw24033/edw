# Changelog - Custom GPT Smart Selective Loading

All notable changes and improvements to the Stepford County Railway Custom GPT system.

---

## [3.5.0] - 2025-11-19

### Added - Branch/Line Infrastructure Data & Corridor Detection ⭐⭐⭐

**Major Features:**

1. **Authoritative Branch/Line Data (scr_lines.json)**
   - Added official branch/line definitions from SCR wiki
   - 15 lines/branches with complete station lists
   - Scraped from https://scr.fandom.com/wiki/Category:Lines
   - **Fixes Morganstown Branch hallucination:**
     - ❌ Before: Custom GPT invented "Stepford High Street, Whitefield" on Morganstown Branch
     - ✅ After: Loads scr_lines.json showing correct stations: New Harrow, Elsemere Pond, Elsemere Junction, Berrily, East Berrily, Beaulieu Park, Morganstown

2. **Express Route Corridor Detection**
   - Added corridor identification for express routes without intermediate stops
   - Detects physical route via related route analysis
   - **Fixes R081 corridor calculation:**
     - ❌ Before: Listed Benton corridor stations (wrong physical line!)
     - ✅ After: Identifies Morganstown corridor via R080 relationship, lists correct 20 skipped stations

**Why This Matters:**

**Problem 1 - Branch Hallucination:**
- Custom GPT had no authoritative source for branch/line station lists
- When asked "What stations are on Morganstown Branch?", it fabricated answers
- Mixed up Whitefield Branch stations with Morganstown Branch

**Problem 2 - Corridor Confusion:**
- Between Stepford Central and Leighton City, there are TWO different physical corridors:
  - **Benton Corridor** (11 routes): R003, R009, R024, R026, R035, R036, R045, R076, R077, R078, R088
  - **Morganstown Corridor** (3 routes): R080, R081, R082
- R081 "Llyn (super fast)" has no intermediate stops, so calculator defaulted to wrong corridor
- Listed Benton, Benton Bridge, Hampton Hargate (stations R081 never passes!)

**New Files:**
- `scr_lines.json` - 15 official SCR lines with station lists, summaries, and wiki URLs
- `UPLOAD_TO_CUSTOM_GPT/README.md` - Upload instructions and file list
- `DOCUMENTATION/README.md` - Setup documentation guide

**Updated Files:**
- `custom_gpt_instructions_COMPACT.txt` (7,112 chars)
  - Added corridor detection workflow with reference to detailed guide
  - Added mandatory scr_lines.json loading for branch queries
  - Rule: "ALWAYS state which corridor in your answer"

- `SYSTEM_INSTRUCTIONS_REFERENCE.md`
  - Added "CORRIDOR DETECTION FOR EXPRESS ROUTES" section
  - Step-by-step R081 example showing Morganstown corridor identification
  - Explains two physical corridors (Benton vs Morganstown)
  - Shows correct vs incorrect answer formats

**Technical Implementation:**

**Branch Query Workflow:**
```python
import json
# Load authoritative branch data
with open('/mnt/data/scr_lines.json', 'r') as f:
    lines_data = json.load(f)

# Find specific branch
for line in lines_data:
    if 'Morganstown Branch' in line['title']:
        print(line['summary'])
        print(line['content_text'])  # Contains station list
```

**Corridor Detection Workflow:**
```python
# Step 1: Check route_type for corridor hints
route = routes['R081']  # "Llyn (super fast)" - no corridor specified

# Step 2: Find related routes with same origin/destination
related = {code: r['route_type'] for code, r in routes.items()
           if r['origin'] == route['origin'] and r['destination'] == route['destination']
           and 'via' in r['route_type'].lower()}
# Result: R080 "Llyn via Morganstown (fast)" ← Reveals corridor!

# Step 3: Use R080's corridor to determine R081's skipped stations
r080_corridor = calc.calculate_route_corridor('R080')['corridor']
r081_stops = set(routes['R081']['stations'])
skipped = [s for s in r080_corridor if s not in r081_stops]
```

**Results:**

**R081 Corridor Analysis (Correct):**
- Uses Morganstown corridor (same as R080)
- Skips 20 stations including:
  - Four Ways, Stepford East, Stepford High Street
  - St Helens Bridge (junction to Morganstown Branch)
  - **Morganstown Branch stations:** New Harrow, Elsemere Pond, Elsemere Junction, Berrily, East Berrily, Beaulieu Park
  - Morganstown, Leighton Stepford Road
  - Edgemead, Faymere, Westercoast, Millcastle Racecourse, Millcastle, Westwyvern, Starryloch, Northshore

**Folder Organization:**
- Created `UPLOAD_TO_CUSTOM_GPT/` folder with exactly 12 knowledge files
- Created `DOCUMENTATION/` folder with instructions and setup files
- Moved old docs to `_reference_only/` folder

**Breaking Changes:** None - backward compatible with fallback mechanisms

**Commits:** Session 2025-11-19 - Branch data & corridor detection fixes

---

## [3.4.1] - 2025-11-19

### Fixed - Integration Fixes for Custom GPT Environment ⭐

**Problem:**
- Platform detection (v3.4) wasn't working in Custom GPT
- Terminal detection required csv_path parameter but get_route_context() wasn't passing it
- Station name mismatches: "Benton Bridge" vs "Benton Bridge (Station)"

**Solution:**
1. **Fixed get_route_context() csv_path parameter**
   - Now passes csv_path to get_route_platform() for terminal detection
   - Enables terminal detection in Custom GPT environment (/mnt/data/)

2. **Added fuzzy station name matching**
   - Normalizes station names by removing "(Station)" suffix
   - Matches "Benton Bridge" with "Benton Bridge (Station)"
   - Prevents lookup failures due to suffix inconsistencies

3. **Updated CSV path handling**
   - Works in both local and Custom GPT (/mnt/data/) environments
   - Automatically detects correct path format

**Results:**
- ✅ get_route_context("Benton Bridge", ..., "R045", "Benton") returns "Platform 3 (toward Stepford Victoria)"
- ✅ Terminal detection now works in Custom GPT
- ✅ Station name variations handled automatically

**Commits:** v3.4.1 integration fixes

---

## [3.4.0] - 2025-11-18

### Added - Terminal Detection for Intermediate Stops ⭐⭐

**Problem:**
- Directional platform lookup (v2.2.0) only worked when next_station was a terminus
- For intermediate stations, couldn't determine direction/terminal
- Example: R045 at Benton Bridge → Benton (Benton isn't a terminus!)

**Solution:**
- Added intelligent terminal detection using route analysis
- Parses CSV to find route's full stop list
- Determines which direction passenger is traveling
- Identifies the terminal station for that direction

**How It Works:**
```python
# Example: R045 from Benton Bridge to Benton (intermediate stop)
# Step 1: Load route R045's full stop list from CSV
# Step 2: Find Benton Bridge position and Benton position
# Step 3: Determine direction (toward which end of route?)
# Step 4: Identify terminal: Stepford Victoria
# Step 5: Look up platform: R045 to Stepford Victoria → Platform 3
```

**New Function:**
- `_get_terminal_for_direction(route_code, current_station, next_station, csv_path)`
  - Determines terminal station based on travel direction
  - Returns terminal name for platform lookup

**Results:**
- ✅ R045 at Benton Bridge → Benton: "Platform 3 (toward Stepford Victoria)"
- ✅ Works for any intermediate station, not just termini
- ✅ Solves "intermediate station problem"

**Commits:** v3.4 terminal detection

---

## [3.3.0] - 2025-11-18

### Improved - Platform Parsing for Wiki Table Format

**Problem:**
- Services table parsing failed on some wiki formats
- Multiple routes sharing one destination caused parsing errors
- Missed some route-to-platform mappings

**Solution:**
- Enhanced Services table parsing logic
- Better handling of wiki table format variations
- Improved regex patterns for route detection
- More accurate route-to-platform mapping

**Results:**
- ✅ Handles edge cases in wiki formatting
- ✅ Better coverage of route-platform relationships
- ✅ More robust parsing

**Commits:** v3.3 platform parsing improvements

---

## [3.1.0] - 2025-11-18

### Fixed - Python Import Paths & Station Coordinates ⭐

**Problem:**
1. Import errors in Custom GPT environment
   - Missing sys.path.append('/mnt/data')
   - File paths not using /mnt/data/ prefix
   - RouteCorridorCalculator couldn't find JSON file

2. Station coordinates were placeholder data
   - Random alphabetical grid layout
   - Not reflecting actual network topology

**Solution:**
1. **Fixed all import paths**
   - Added: `sys.path.append('/mnt/data')` to all code examples
   - Fixed: All file paths use `/mnt/data/` prefix
   - Fixed: RouteCorridorCalculator gets full JSON path

2. **Rewrote station_coords.csv**
   - Was: Random alphabetical grid
   - Now: Actual network map topology
   - Positions reflect real SCR network layout

**Results:**
- ✅ All Python imports work in Custom GPT
- ✅ File paths resolve correctly in /mnt/data/
- ✅ Network visualizations show realistic layout

**Commits:** v3.1 import path and coordinates fixes

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

| Version | Date | Feature | Impact |
|---------|------|---------|--------|
| 3.5.0 | 2025-11-19 | Branch/line data + corridor detection | ⭐⭐⭐ Fixes hallucination & corridor errors (Morganstown Branch, R081) |
| 3.4.1 | 2025-11-19 | Integration fixes for Custom GPT | ⭐ Terminal detection now works in Custom GPT |
| 3.4.0 | 2025-11-18 | Terminal detection for intermediate stops | ⭐⭐ Solves intermediate station problem (Benton Bridge → Benton) |
| 3.3.0 | 2025-11-18 | Improved platform parsing | Better wiki table format handling |
| 3.1.0 | 2025-11-18 | Python import paths & coordinates | ⭐ Fixes Custom GPT environment, realistic map layout |
| 2.2.0 | 2024-11-17 | Bidirectional platforms | ⭐⭐⭐ Directional accuracy (R083 to Llyn → Platform 2, to Newry → 2-3) |
| 2.1.0 | 2024-11-17 | Route-specific platforms | ⭐ Route precision (R001 → Platform 1,4 vs all Connect → 2,4) |
| 2.0.1 | 2024-11-17 | Operator-platform heuristics | Fixed Llyn showing both Express and Connect platforms |
| 2.0.0 | 2024-11-17 | Direct route priority | Benton→Llyn now shows 16min direct (was 17.6min transfer) |
| 1.1.1 | 2024-11-17 | Platform count extraction | All 82 stations show correct platform count |
| 1.1.0 | 2024-11-17 | Compact instructions | Fits 8,000 char limit (was 14,267 chars) |

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
