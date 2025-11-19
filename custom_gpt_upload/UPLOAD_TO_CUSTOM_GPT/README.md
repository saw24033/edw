# Custom GPT Knowledge Files - UPLOAD THESE 12 FILES

This folder contains the **12 files** that must be uploaded to Custom GPT's Knowledge section.

## 📁 Files to Upload (12 Total)

### Core Functionality (9 files)
1. ✅ `rail_helpers.py` - Network routing and pathfinding functions
2. ✅ `station_knowledge_helper.py` - Station data parser with platform detection (v3.4.1)
3. ✅ `route_corridor_calculator.py` - Corridor analysis and skipped station calculation
4. ✅ `plot_helpers.py` - Network visualization functions
5. ✅ `rail_routes.csv` - Railway network graph data
6. ✅ `scr_stations_part1.md` - Station wiki data (A-M)
7. ✅ `scr_stations_part2.md` - Station wiki data (N-Z)
8. ✅ `station_coords.csv` - Station coordinates for plotting
9. ✅ `stepford_routes_with_segment_minutes_ai_knowledge_base.json` - Complete route data with timings

### New/Updated Files (2 files)
10. ✅ `scr_lines.json` ⭐ **NEW** - Authoritative branch/line data from SCR wiki
    - Fixes Morganstown Branch hallucination
    - Contains all 15 official SCR lines/branches with station lists
    - Prevents Custom GPT from fabricating branch data

11. ✅ `SYSTEM_INSTRUCTIONS_REFERENCE.md` ⭐ **UPDATED** - Detailed function reference and examples
    - Added "CORRIDOR DETECTION FOR EXPRESS ROUTES" section
    - Shows how to identify which corridor routes like R081 use
    - Explains Benton vs Morganstown corridor differences

### Documentation (1 file)
12. ✅ `ROUTE_CORRIDOR_CALCULATOR_GUIDE.md` - Route corridor calculator usage guide

---

## 🚫 Important Limits

**Custom GPT Knowledge Limit:** Maximum 12 files
**Current Count:** 12 files ✅

---

## 📝 Instructions File (NOT in Knowledge)

The instructions file is in `../DOCUMENTATION/custom_gpt_instructions_COMPACT.txt`:
- **7,112 characters** (under 8,000 limit ✅)
- This goes in the **Instructions** field, NOT Knowledge
- Contains core behavior, workflow, and references to these knowledge files

---

## 🎯 What These Fixes Solve

### 1. Morganstown Branch Hallucination ❌ → ✅
**Before:** Custom GPT claimed "Stepford High Street" and "Whitefield" are on Morganstown Branch
**After:** Loads `scr_lines.json` and shows correct stations: New Harrow, Elsemere Pond, Elsemere Junction, Berrily, East Berrily, Beaulieu Park, Morganstown

### 2. R081 Corridor Detection ❌ → ✅
**Before:** Listed Benton corridor stations (wrong physical line!)
**After:** Identifies R081 uses Morganstown corridor (via R080 relationship) and lists correct 20 skipped stations

---

## 📤 Upload Instructions

1. Go to Custom GPT settings
2. Navigate to Knowledge section
3. **Upload all 12 files from this folder**
4. Go to Instructions section
5. **Paste contents of `../DOCUMENTATION/custom_gpt_instructions_COMPACT.txt`**
6. Save and test with:
   - "What stations are on Morganstown Branch?"
   - "What stations does R081 skip?"
