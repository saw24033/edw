# Merge Conflict Resolution Guide

## Situation

Merging branch `claude/route-path-calculator-01Hof7xFLKARcqWx1tU3oFuH` into `main` creates conflicts with deleted files.

## Conflicting Files

These files exist in `main` but were **intentionally deleted** in our branch:

1. `custom_gpt_upload/GPT_USAGE_GUIDE.md`
2. `custom_gpt_upload/README.md`
3. `custom_gpt_upload/UPLOAD_CHECKLIST.txt`
4. `custom_gpt_upload/custom_gpt_instructions_COMPACT.txt`
5. `custom_gpt_upload/custom_gpt_instructions_with_station_knowledge.txt`

## Why They Were Deleted

These files are **redundant and superseded** by new v2.0 documentation:

- `GPT_USAGE_GUIDE.md` → superseded by `ROUTE_CORRIDOR_README.md`
- `README.md` → superseded by `ROUTE_CORRIDOR_README.md`
- `UPLOAD_CHECKLIST.txt` → superseded by `CUSTOM_GPT_UPLOAD_CHECKLIST.md`
- `custom_gpt_instructions_COMPACT.txt` → old version, replaced by `GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt`
- `custom_gpt_instructions_with_station_knowledge.txt` → old version, replaced by `GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt`

## Resolution Strategy

**Accept the deletion** - these files should be removed from main.

---

## Command Line Resolution (Option 1)

If you're merging via command line:

```bash
# Start the merge
git checkout main
git merge claude/route-path-calculator-01Hof7xFLKARcqWx1tU3oFuH

# For each conflicting file, accept the deletion (our version)
git rm custom_gpt_upload/GPT_USAGE_GUIDE.md
git rm custom_gpt_upload/README.md
git rm custom_gpt_upload/UPLOAD_CHECKLIST.txt
git rm custom_gpt_upload/custom_gpt_instructions_COMPACT.txt
git rm custom_gpt_upload/custom_gpt_instructions_with_station_knowledge.txt

# Complete the merge
git commit -m "Merge route corridor calculator v2.0 - remove redundant files"
```

---

## GitHub Web UI Resolution (Option 2)

If you're using GitHub's web interface:

1. **For each conflict**, choose: **"Use my version"** or **"Accept incoming changes"**
   - This will keep the files deleted

2. **Or manually resolve** by:
   - Opening the conflict editor
   - Confirming deletion for each file
   - Marking as resolved

---

## Alternative: Cherry-pick Strategy (Option 3)

If merge is too complex, cherry-pick the important commits:

```bash
git checkout main

# Cherry-pick the v2.0 feature commits
git cherry-pick 7b4ce20  # Add generic corridor query functionality
git cherry-pick 43c4242  # Update Custom GPT documentation for Version 2.0
git cherry-pick d04774e  # Add Route Corridor Calculator v2.0 to custom_gpt_upload folder
git cherry-pick 2c904ce  # Add repository consistency check report
git cherry-pick 3c8c577  # Clean up custom_gpt_upload folder - remove redundant documentation

# Push to main
git push origin main
```

---

## Verification After Resolution

After resolving conflicts, verify the custom_gpt_upload folder contains:

```bash
git checkout main
ls custom_gpt_upload/
```

**Expected files (14 total)**:
- ✓ CHANGELOG.md (if it exists in main)
- ✓ route_corridor_calculator.py
- ✓ GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt
- ✓ ROUTE_CORRIDOR_CHANGELOG.md
- ✓ CUSTOM_GPT_UPLOAD_CHECKLIST.md
- ✓ ROUTE_CORRIDOR_README.md
- ✓ ROUTE_CORRIDOR_CALCULATOR_GUIDE.md
- ✓ stepford_routes_with_segment_minutes_ai_knowledge_base.json
- ✓ rail_helpers.py
- ✓ plot_helpers.py
- ✓ station_knowledge_helper.py
- ✓ scr_stations_part1.md
- ✓ scr_stations_part2.md
- ✓ rail_routes.csv
- ✓ station_coords.csv

**Should NOT be present (deleted)**:
- ✗ GPT_USAGE_GUIDE.md
- ✗ README.md
- ✗ UPLOAD_CHECKLIST.txt
- ✗ custom_gpt_instructions_COMPACT.txt
- ✗ custom_gpt_instructions_with_station_knowledge.txt

---

## Summary

**Resolution**: Accept the deletion of all 5 conflicting files.

**Reason**: They are outdated and superseded by newer, better-organized v2.0 documentation.

**Risk**: None - these files contain old information that conflicts with v2.0 updates.

---

**Commit Reference**: 3c8c577 - "Clean up custom_gpt_upload folder - remove redundant documentation"
