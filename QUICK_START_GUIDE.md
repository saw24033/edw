# ⚡ Quick Start Guide - Custom GPT v3.0

**Goal:** Get your Custom GPT running in 10 minutes

---

## 📦 What You Have

**Location:** `/custom_gpt_upload/` folder
**Files:** 16 total (14 to upload + 2 reference)
**Size:** ~1.3 MB
**Version:** 3.0.0 Unified System

---

## 🚀 5-Minute Upload

### Step 1: Open ChatGPT (1 minute)
1. Go to https://chat.openai.com
2. Click "My GPTs"
3. Click "Create a GPT"
4. Switch to "Configure" tab

### Step 2: Enable Code Interpreter (30 seconds)
- Under "Capabilities", check ✅ "Code Interpreter"

### Step 3: Upload 14 Files (3 minutes)

Click "Upload files" under Knowledge and select these from `/custom_gpt_upload/`:

**Quick selection list:**
```
✅ station_knowledge_helper.py
✅ rail_helpers.py
✅ plot_helpers.py
✅ rail_routes.csv
✅ route_corridor_calculator.py
✅ GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt
✅ stepford_routes_with_segment_minutes_ai_knowledge_base.json
✅ scr_stations_part1.md
✅ scr_stations_part2.md
✅ station_coords.csv
✅ GPT_USAGE_GUIDE.md
✅ ROUTE_CORRIDOR_CALCULATOR_GUIDE.md
✅ CHANGELOG.md
✅ README.txt (optional)
```

### Step 4: Copy Instructions (30 seconds)
1. Open `custom_gpt_upload/custom_gpt_instructions_COMPACT.txt`
2. Select all (Ctrl+A / Cmd+A)
3. Copy (Ctrl+C / Cmd+C)
4. Paste into "Instructions" field in GPT

⚠️ **Do NOT upload this file - paste it into Instructions!**

### Step 5: Save (30 seconds)
1. Click "Save"
2. Name it (e.g., "Stepford County Railway Guide v3.0")
3. Done!

---

## ✅ Quick Test

Test with this simple query:

> "How do I get from Benton to Llyn?"

**Expected response:**
- Direct service R078
- 16 minutes
- Platform 1, 3, or 10
- No transfers

If you see this, **you're done!** ✅

---

## 🧪 Full Test (5 Verification Queries)

### Test 1: Route Planning
**Ask:** "How do I get from Benton to Llyn?"
**Should say:** R078, 16 min, direct, Platform 1/3/10

### Test 2: Skip Analysis
**Ask:** "Which stations does R026 skip?"
**Should say:** 11 skipped stations with alternatives

### Test 3: Corridor Query
**Ask:** "What's between St Helens Bridge and Leighton Stepford Road?"
**Should say:** 3 corridors (primary, express, divergent)

### Test 4: Divergent Path
**Ask:** "Does R080 stop at Hampton Hargate?"
**Should say:** "No, uses Morganstown route" (NOT "skips")

### Test 5: Directional Platform
**Ask:** "Take R083 from Benton to Llyn"
**Should say:** Platform 2 (specific, not "2, 2-3")

---

## ❓ Troubleshooting

### "File too large" error
- Upload files one at a time, not in batch
- Largest file is 395 KB (well under limits)

### Generic answers (not using custom data)
- ✅ Check Code Interpreter is enabled
- ✅ Verify all 14 files uploaded
- ✅ Confirm instructions pasted (not uploaded as file)

### Missing platform info
- ✅ Ensure `scr_stations_part1.md` and `part2.md` uploaded
- ✅ Check `station_knowledge_helper.py` present

### Corridor calculator not working
- ✅ Verify `route_corridor_calculator.py` uploaded
- ✅ Check JSON file present (376 KB file)
- ✅ Ensure instructions include corridor section

---

## 📖 Need More Help?

**Detailed guides:**
- `SYSTEM_DOCUMENTATION.md` - Complete documentation
- `UPLOAD_CHECKLIST.txt` - Detailed upload steps
- `EXAMPLE_QUERY_BENTON_TO_LLYN.md` - Real usage example

**Feature verification:**
- `BRANCH_FEATURE_AUDIT_REPORT.md` - All features verified

---

## ✨ What Your GPT Can Do

### Smart Selective Loading
- Detects query type automatically
- Loads only relevant data (75-90% reduction)
- Fast responses (<1 second)

### Route Planning
- Direct route priority
- Direction-specific platforms
- Multi-transfer journeys

### Corridor Analysis
- Skip detection
- Generic corridor queries
- Divergent path handling

### Station Information
- 82 complete profiles
- Platform layouts
- Service information
- Historical data

---

## 🎯 Next Steps

1. Upload the 14 files (3 minutes)
2. Paste instructions (30 seconds)
3. Test with "Benton to Llyn" query
4. Run full 5-query test
5. Start using!

**Total time:** 10 minutes
**Result:** Fully functional Custom GPT v3.0 ✅

---

**Version:** 3.0.0 Unified
**Last Updated:** 2025-11-18
**Status:** Production Ready
