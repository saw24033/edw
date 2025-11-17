# Route Corridor Calculator v2.0 - Upload Files

## Files in This Folder for Custom GPT Upload

### 🔄 REPLACE These Files (Updated to v2.0)

**1. route_corridor_calculator.py** (30K)
- Main calculator with generic corridor queries
- Divergent route detection
- CLI with `--between` flag

**2. GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt** (9.1K)
- Updated instructions for Custom GPT
- New query pattern #5: Generic corridor queries
- Clarified "skip" vs "different route" terminology

### ✨ ADD These Files (New Documentation)

**3. ROUTE_CORRIDOR_CHANGELOG.md** (9.2K)
- Complete version history (v1.0 → v2.0)
- Feature explanations and migration guide

**4. CUSTOM_GPT_UPLOAD_CHECKLIST.md** (7.0K)
- Upload checklist and testing plan
- Quick reference card

### ✅ KEEP These Files (No Changes)

**5. stepford_routes_with_segment_minutes_ai_knowledge_base.json** (376K)
- Network data (no changes)

**6. ROUTE_CORRIDOR_CALCULATOR_GUIDE.md** (10K)
- Algorithm documentation (still valid)

---

## Quick Upload Steps

1. **Log into Custom GPT settings**
2. **Go to Knowledge/Files section**
3. **Delete old versions** of:
   - route_corridor_calculator.py
   - GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt
4. **Upload NEW versions** from this folder:
   - route_corridor_calculator.py ⭐
   - GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt ⭐
   - ROUTE_CORRIDOR_CHANGELOG.md 🆕
   - CUSTOM_GPT_UPLOAD_CHECKLIST.md 🆕
5. **Verify** existing files are still present:
   - stepford_routes_with_segment_minutes_ai_knowledge_base.json
   - ROUTE_CORRIDOR_CALCULATOR_GUIDE.md

---

## What's New in v2.0

### 1. Generic Corridor Queries
```python
calc.get_all_corridors_between('St Helens Bridge', 'Leighton Stepford Road')
```
Shows ALL routes: primary, divergent, express

### 2. Divergent Route Detection
- R080 via Morganstown correctly analyzed
- No longer shows Hampton Hargate as "skipped"
- Matches actual physical path

### 3. Terminology Clarification
- **"Skip"** = passes without stopping (same corridor)
- **"Different route"** = uses different physical path

---

## Testing After Upload

**Test 1: R080 Divergent Route**
```
Q: "Which stations does R080 skip?"
✓ Should NOT include Hampton Hargate
✓ Should mention Morganstown route
```

**Test 2: Generic Corridor**
```
Q: "What's between St Helens Bridge and Leighton Stepford Road?"
✓ Should show 3 corridors
✓ Should identify Morganstown as divergent
```

**Test 3: R076 Express**
```
Q: "Does R076 stop at Hampton Hargate?"
✓ Should say "No, R076 skips Hampton Hargate"
```

---

## File Locations

All files ready in: `/home/user/edw/custom_gpt_upload/`

**Total Size**: ~441K (well under GPT limits)

---

**Version**: 2.0
**Last Updated**: 2025-11-17
**Status**: ✅ PRODUCTION READY
