# Deployment Checklist - Platform Detection Fix

**Quick reference for deploying v3.4.1 + instruction updates**

---

## Pre-Deployment

- [ ] Verify you have file: `custom_gpt_upload/station_knowledge_helper.py` (v3.4.1)
- [ ] Verify you have file: `custom_gpt_upload/custom_gpt_instructions_COMPACT.txt` (updated)
- [ ] Open Custom GPT settings in browser

---

## Step 1: Upload Python File (5 minutes)

- [ ] Go to **Knowledge** section in Custom GPT settings
- [ ] Find `station_knowledge_helper.py` in file list
- [ ] Click the **trash/delete icon** to remove old version
- [ ] Click **Upload files** button
- [ ] Select: `C:\Users\sydne\Documents\GitHub\edw\custom_gpt_upload\station_knowledge_helper.py`
- [ ] Wait for upload to complete (green checkmark)

---

## Step 2: Update Instructions (5 minutes)

- [ ] Open file: `C:\Users\sydne\Documents\GitHub\edw\custom_gpt_upload\custom_gpt_instructions_COMPACT.txt`
- [ ] Select all (Ctrl+A) and copy (Ctrl+C)
- [ ] In Custom GPT settings, find **Instructions** text box (top of page)
- [ ] Clear existing instructions
- [ ] Paste new instructions (Ctrl+V)
- [ ] Verify you see "MANDATORY WORKFLOW FOR EVERY ROUTE QUERY" near the top
- [ ] Click **Save** or **Update**

---

## Step 3: Test Deployment (10 minutes)

### Test 1: Benton Bridge Route
- [ ] Ask Custom GPT: "How to get from Benton Bridge to Port Benton"
- [ ] Verify Custom GPT runs Python code (shows code block)
- [ ] Verify `origin` variable is NOT `None`
- [ ] Verify response includes: "Platform 3 (toward Stepford Victoria)" or similar
- [ ] Verify platform data shown for all journey legs

**If Test 1 PASSES:** ✅ Deployment successful!

**If Test 1 FAILS:** See Troubleshooting below

### Test 2: Airport Parkway (Optional)
- [ ] Ask Custom GPT: "Which platform does R003 depart from at Airport Parkway?"
- [ ] Verify platform data returned with direction indicator

---

## Success Criteria

✅ **Deployment is successful when:**
- Custom GPT shows platform data for Benton Bridge (not `None`)
- Platform data includes direction: "(toward ...)"
- No errors about missing modules
- Custom GPT doesn't claim "no platform data in wiki"

---

## Troubleshooting

### ❌ Still returns `origin = None`

**Fix:**
1. Verify v3.4.1 was uploaded (check file date in Knowledge section)
2. Try deleting and re-uploading `station_knowledge_helper.py`
3. Check both `scr_stations_part1.md` and `part2.md` are in Knowledge

### ❌ Platform data but no direction indicator

**Example:** Shows "Platforms 2, 3" instead of "Platform 3 (toward ...)"

**Fix:**
1. Verify `rail_routes.csv` is in Knowledge section
2. Re-check instructions were pasted correctly (should say "MANDATORY WORKFLOW")

### ❌ Custom GPT doesn't call `get_route_context()` at all

**Fix:**
1. Verify instructions were pasted into **Instructions field** (not uploaded as Knowledge file)
2. Re-paste instructions (may have been auto-modified)
3. Check instructions start with "MANDATORY WORKFLOW FOR EVERY ROUTE QUERY"

### ❌ "Module not found: route_pathfinder"

**This is NORMAL** - Custom GPT tries `route_pathfinder` first, then uses `rail_helpers.py`.

**Only worry if:**
- Error message AND no platform data
- Then check `rail_helpers.py` is in Knowledge section

---

## Quick Test Command

After deployment, run this exact test:

```
How to get from Benton Bridge to Port Benton
```

**Expected output should include:**
```
Platform at Benton Bridge: Platform 3 (toward Stepford Victoria)
```

If you see this, deployment is successful! ✅

---

## Rollback (If Needed)

If deployment causes issues:

1. **Restore old station_knowledge_helper.py** (if you have backup)
2. **Restore old instructions** (if you saved them)
3. Report the error message for debugging

---

## Need Help?

See `FINAL_DEPLOYMENT_GUIDE.md` for:
- Detailed troubleshooting steps
- Technical explanations
- Additional test cases
- Complete verification checklist

---

**Estimated time:** 20 minutes total (upload + test)
**Status after completion:** Platform detection fully working ✅
