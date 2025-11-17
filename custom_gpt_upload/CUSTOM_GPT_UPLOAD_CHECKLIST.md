# Custom GPT Upload Checklist - Stepford Railway Network Assistant

## Required Files for Custom GPT

### Core Data File
✅ **stepford_routes_with_segment_minutes_ai_knowledge_base.json**
- **Purpose**: Complete railway network data
- **Size**: ~500KB
- **Contains**: All routes, stations, connections, travel times, prices
- **Status**: Already uploaded, no changes needed

---

### Route Corridor Calculator (Updated)

✅ **route_corridor_calculator.py** ⭐ **UPDATED - VERSION 2.0**
- **Purpose**: Main corridor analysis tool
- **Size**: ~35KB
- **Last Updated**: 2025-11-17
- **New Features**:
  - Generic corridor queries (`get_all_corridors_between()`)
  - Divergent route detection
  - CLI `--between` flag support
- **Status**: **REPLACE PREVIOUS VERSION**

✅ **GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt** ⭐ **UPDATED - VERSION 2.0**
- **Purpose**: Instructions for GPT on how to use corridor calculator
- **Size**: ~10KB
- **Last Updated**: 2025-11-17
- **New Sections**:
  - Query Pattern #5: Generic corridor queries
  - Updated Response Guidelines (skip vs different route)
  - New example response for generic queries
  - Updated Key Functions section
- **Status**: **REPLACE PREVIOUS VERSION**

✅ **ROUTE_CORRIDOR_CALCULATOR_GUIDE.md**
- **Purpose**: Comprehensive usage guide for reference
- **Size**: ~15KB
- **Contains**: Algorithm explanation, examples, troubleshooting
- **Status**: No changes needed (comprehensive enough)

✅ **ROUTE_CORRIDOR_CHANGELOG.md** ⭐ **NEW**
- **Purpose**: Complete changelog of all updates
- **Size**: ~8KB
- **Contains**: Version history, breaking changes, migration guide
- **Status**: **UPLOAD NEW FILE**

---

### Journey Planning Tool (Optional but Recommended)

✅ **route_pathfinder.py**
- **Purpose**: Multi-transfer journey planning
- **Size**: ~10KB
- **Contains**: BFS pathfinding, route optimization
- **Status**: No changes, keep existing

---

### Test/Demo Files (Optional - Not Required for GPT)

⚠️ **test_corridor_query.py**
- **Purpose**: Demonstrates different corridor query approaches
- **Status**: **DO NOT UPLOAD** (only for testing)

⚠️ **rail_helpers.py** (if exists)
- **Purpose**: Additional helper functions
- **Status**: Only upload if GPT currently uses it

---

## Upload Summary

### Files to REPLACE (Updated)
1. ✅ `route_corridor_calculator.py` - Version 2.0
2. ✅ `GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt` - Version 2.0

### Files to ADD (New)
3. ✅ `ROUTE_CORRIDOR_CHANGELOG.md` - New documentation

### Files to KEEP (No changes)
4. ✅ `stepford_routes_with_segment_minutes_ai_knowledge_base.json`
5. ✅ `ROUTE_CORRIDOR_CALCULATOR_GUIDE.md`
6. ✅ `route_pathfinder.py` (if already uploaded)

---

## GPT Instructions Update

### Add to Custom GPT Instructions

Add this section to your Custom GPT's main instructions:

```markdown
## Route Corridor Analysis

When users ask about stations between two points or which stations a route skips:

### Two Types of Queries

1. **Route-specific**: "Which stations does R026 skip?"
   - Use: `calc.calculate_route_corridor('R026')`
   - Shows only stations on that route's actual physical path

2. **Generic corridor**: "What's between St Helens Bridge and Leighton Stepford Road?"
   - Use: `calc.get_all_corridors_between('St Helens Bridge', 'Leighton Stepford Road')`
   - Shows ALL possible routes/corridors, including divergent paths

### Important Distinction

**"Skip" vs "Different Route"**:
- A route **skips** a station if it passes by it without stopping (same corridor)
- A route uses a **different route** if it takes a completely different physical path
- Example: R080 via Morganstown doesn't "skip" Hampton Hargate (different corridor)
- Example: R076 DOES skip Benton Bridge (same corridor, no stop)

### Always provide context:
- For skipped stations, mention which other routes serve them
- For divergent routes, explain they're different physical paths
- Use the segment_details to show alternative routes
```

---

## Testing After Upload

### Verify Route-Specific Queries
1. Test: "Which stations does R080 skip?"
   - Should show 15 stations
   - Should NOT include Hampton Hargate
   - Should mention it uses Morganstown route

2. Test: "Does R076 stop at Hampton Hargate?"
   - Should say "No, R076 skips Hampton Hargate"
   - Should list it as skipped station #8

### Verify Generic Corridor Queries
3. Test: "What stations are between St Helens Bridge and Leighton Stepford Road?"
   - Should show 3 corridors
   - Should identify primary (11 stations via Hampton Hargate)
   - Should identify divergent (3 stations via Morganstown)
   - Should identify express (3 stations direct)

4. Test: "Show me all routes from Central to Hornsby" (if you have Sydney analogy)
   - Should distinguish T1 North Shore vs CCN Western as different corridors
   - Should not say one "skips" the other's stations

---

## File Sizes (for upload limits)

| File | Size | Priority |
|------|------|----------|
| stepford_routes...json | ~500KB | Required |
| route_corridor_calculator.py | ~35KB | Required |
| GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt | ~10KB | Required |
| ROUTE_CORRIDOR_CALCULATOR_GUIDE.md | ~15KB | Recommended |
| ROUTE_CORRIDOR_CHANGELOG.md | ~8KB | Recommended |
| route_pathfinder.py | ~10KB | Optional |
| **Total** | **~578KB** | |

All files comfortably under typical GPT upload limits (10MB per file, 100MB total).

---

## Version Information

- **Route Corridor Calculator**: Version 2.0
- **Release Date**: 2025-11-17
- **Breaking Changes**: None (backward compatible)
- **New Features**: Generic corridor queries, divergent route detection

---

## Quick Reference Card

### For Route-Specific Queries
```python
from route_corridor_calculator import RouteCorridorCalculator
calc = RouteCorridorCalculator()

# Analyze specific route
corridor = calc.calculate_route_corridor('R026')
print(f"Skips {len(corridor['skipped'])} stations")

# Get formatted report
print(calc.format_corridor_report(corridor, verbose=True))
```

### For Generic Corridor Queries
```python
# Find ALL corridors between two stations
result = calc.get_all_corridors_between('St Helens Bridge', 'Leighton Stepford Road')

# Show formatted comparison
print(calc.format_corridor_comparison(result))

# Access specific corridor types
for corridor in result['corridors']:
    if corridor['type'] == 'divergent':
        print(f"Divergent via: {corridor['unique_stations']}")
```

---

## Rollback Instructions (If Needed)

If issues occur after upload:

1. **Check error messages** - Most likely cause is missing import
2. **Verify JSON data file** is still uploaded
3. **Revert to Version 1.0** if necessary:
   - Remove `get_all_corridors_between()` calls
   - Use only `calculate_route_corridor()` for all queries

---

## Support

For issues or questions:
- Check `ROUTE_CORRIDOR_CHANGELOG.md` for detailed changes
- Review `ROUTE_CORRIDOR_CALCULATOR_GUIDE.md` for algorithm explanation
- Test locally with CLI: `python3 route_corridor_calculator.py --between "A" "B"`

---

**Last Updated**: 2025-11-17
**Prepared by**: Claude (Route Corridor Calculator Development)
**Status**: Ready for Production Upload
