# Troubleshooting: Platform Information Not Loading

## Problem
Custom GPT shows warnings like:
```
Warning: /mnt/data/scr_stations_part1.md not found
Warning: /mnt/data/scr_stations_part2.md not found
```

AI can't tell users which platform to board from.

---

## Solution Checklist

### Step 1: Verify Files Are Uploaded to Custom GPT

1. Go to ChatGPT → My GPTs
2. Click on your Stepford County Railway GPT
3. Click "Edit GPT"
4. Click "Configure" tab
5. Scroll down to "Knowledge" section

**You should see these 12 files listed:**
- [ ] GPT_USAGE_GUIDE.md
- [ ] ROUTE_CORRIDOR_CALCULATOR_GUIDE.md
- [ ] SYSTEM_INSTRUCTIONS_REFERENCE.md
- [ ] plot_helpers.py
- [ ] rail_helpers.py
- [ ] route_corridor_calculator.py
- [ ] station_knowledge_helper.py
- [ ] rail_routes.csv
- [ ] station_coords.csv
- [ ] **scr_stations_part1.md** ⭐ CRITICAL
- [ ] **scr_stations_part2.md** ⭐ CRITICAL
- [ ] stepford_routes_with_segment_minutes_ai_knowledge_base.json

**If any files are missing**, upload them:
- Click "Upload files" in Knowledge section
- Navigate to: `C:\Users\sydne\Documents\GitHub\edw\custom_gpt_upload`
- Select the missing files
- Click Upload

---

### Step 2: Verify Instructions Were Copied

In the Configure tab, check the "Instructions" text box contains:

```python
import sys
sys.path.append('/mnt/data')
```

This line MUST be in your instructions! Without it, Python can't find the uploaded files.

**If missing:**
1. Open `custom_gpt_instructions_COMPACT.txt`
2. Select ALL (Ctrl+A)
3. Copy (Ctrl+C)
4. Paste into Instructions box (replacing old content)
5. Click Save

---

### Step 3: Test After Upload

After uploading all files, click "Save" and test with:

**Test Query:**
> "How do I get from Port Benton to Benton Bridge?"

**Expected Response Should Include:**
- Route information (R013, R045)
- **Platform numbers** (e.g., "Depart from Platform 1")
- Operator names
- Travel times

**If you still see warnings:**
- The files might not have uploaded properly
- Try deleting and re-uploading scr_stations_part1.md and scr_stations_part2.md

---

### Step 4: Verify File Upload Success

In your GPT, run this test code directly:

```python
import sys
sys.path.append('/mnt/data')

import os
print("Files in /mnt/data/:")
for f in os.listdir('/mnt/data'):
    print(f" - {f}")
```

**Expected output should include:**
- scr_stations_part1.md
- scr_stations_part2.md
- rail_routes.csv
- All other 9 files

**If files are missing from output:**
- They weren't uploaded successfully
- Upload them again

---

## Common Issues

### Issue 1: "Files uploaded but still not found"

**Cause:** Files uploaded as attachments to conversation, not to Knowledge base

**Fix:**
- Files must be uploaded in Configure → Knowledge section
- NOT sent as file attachments in conversation

### Issue 2: "Platform data loads for some stations but not others"

**Cause:** Station name mismatch or parsing error

**Fix:**
- Check station name spelling matches exactly
- Station names are case-sensitive

### Issue 3: "GPT works but gives generic answers without platform numbers"

**Cause:** GPT is using fallback behavior (network data only, not station details)

**Fix:**
- Verify scr_stations_part1.md and scr_stations_part2.md are uploaded
- Check Instructions include selective loading commands
- Test with: `skh.get_route_context("Benton", "Stepford Express", stations, route_code="R078")`

---

## File Size Reference

**scr_stations_part1.md:** 387 KB (Stations A-M)
**scr_stations_part2.md:** 404 KB (Stations N-Z)

If your uploaded files are significantly smaller, they may be corrupted or incomplete.

---

## Still Not Working?

1. Delete ALL files from Knowledge section
2. Re-upload all 12 files fresh
3. Replace Instructions with fresh copy of `custom_gpt_instructions_COMPACT.txt`
4. Save
5. Test again

---

**Last Updated:** 2025-11-18
**Version:** 3.2
