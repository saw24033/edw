# Mobile Merge Conflict Resolution Guide

## Resolving Route Corridor Calculator v2.0 Merge Conflicts on Phone

### Option 1: GitHub Mobile App (Recommended)

**If you have the GitHub mobile app installed:**

1. **Open the Pull Request**
   - Open GitHub app
   - Go to your repository: `saw24033/edw`
   - Find the Pull Request for branch: `claude/route-path-calculator-01Hof7xFLKARcqWx1tU3oFuH`

2. **Resolve Conflicts**
   - Tap "Resolve conflicts" button
   - For each of the 5 conflicting files:
     - `custom_gpt_upload/GPT_USAGE_GUIDE.md`
     - `custom_gpt_upload/README.md`
     - `custom_gpt_upload/UPLOAD_CHECKLIST.txt`
     - `custom_gpt_upload/custom_gpt_instructions_COMPACT.txt`
     - `custom_gpt_upload/custom_gpt_instructions_with_station_knowledge.txt`

   - **Choose**: "Use branch version" or "Accept incoming changes"
     (This keeps the files deleted)

3. **Complete Merge**
   - After resolving all conflicts, tap "Mark as resolved"
   - Tap "Commit merge"
   - Tap "Merge pull request"

---

### Option 2: GitHub Mobile Web (Browser)

**If using Safari, Chrome, or any mobile browser:**

1. **Open GitHub in Browser**
   - Go to: `https://github.com/saw24033/edw`
   - Sign in if needed

2. **Navigate to Pull Request**
   - Tap "Pull requests" tab
   - Find and open the PR from `claude/route-path-calculator-01Hof7xFLKARcqWx1tU3oFuH`

3. **Resolve Conflicts**
   - Scroll down and tap "Resolve conflicts"
   - GitHub will show a web-based editor

   For each file, you'll see something like:
   ```
   <<<<<<< HEAD
   [file content from main]
   =======
   [file deleted]
   >>>>>>> claude/route-path-calculator-01Hof7xFLKARcqWx1tU3oFuH
   ```

4. **Edit Each Conflict**
   - **Delete everything** (accept the deletion)
   - Remove all conflict markers and content
   - Leave the file empty or completely removed

   Or tap "Use this version" if GitHub provides buttons

5. **Mark Resolved**
   - After editing all 5 files
   - Tap "Mark as resolved" button at top
   - Tap "Commit merge"

6. **Complete Merge**
   - Tap "Merge pull request"
   - Add merge commit message (optional)
   - Tap "Confirm merge"

---

### Option 3: Simple Web Instructions (Step by Step)

**For each of the 5 conflicting files:**

1. **Open the conflict**
   - GitHub shows: "This file has conflicts"

2. **What you'll see:**
   ```
   <<<<<<< HEAD (main branch)
   [old file content - from main]
   =======
   [nothing here - file deleted in our branch]
   >>>>>>> claude/route-path-calculator-01Hof7xFLKARcqWx1tU3oFuH
   ```

3. **What to do:**
   - **Delete EVERYTHING between `<<<<<<<` and `>>>>>>>`**
   - Including the conflict markers themselves
   - Leave the file completely empty
   - Or use "Accept incoming" button if available

4. **Why?**
   - The file was intentionally removed
   - It's outdated and replaced by v2.0 docs
   - Keeping it deleted is correct

---

### Quick Decision Guide

**For each conflicting file, when GitHub asks:**

❓ **"Which version do you want to keep?"**

✅ **Answer**: "Incoming changes" or "This branch" or "Delete the file"

❌ **Don't choose**: "Current changes" or "Main branch" or "Keep the file"

---

### Files You're Deleting (and Why)

1. ❌ **GPT_USAGE_GUIDE.md**
   - Replaced by: `ROUTE_CORRIDOR_README.md` (better organized)

2. ❌ **README.md**
   - Replaced by: `ROUTE_CORRIDOR_README.md` (v2.0 specific)

3. ❌ **UPLOAD_CHECKLIST.txt**
   - Replaced by: `CUSTOM_GPT_UPLOAD_CHECKLIST.md` (more comprehensive)

4. ❌ **custom_gpt_instructions_COMPACT.txt**
   - Replaced by: `GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt` (v2.0)

5. ❌ **custom_gpt_instructions_with_station_knowledge.txt**
   - Replaced by: `GPT_INSTRUCTIONS_ROUTE_CORRIDOR.txt` (v2.0)

**All 5 files are old/redundant. Delete them all.**

---

### Visual Guide for Mobile

**GitHub Mobile App:**
```
[Pull Request]
  ↓
[Resolve conflicts button]
  ↓
For each file:
  [Use incoming] ← Tap this!
  [ Keep current ]
  ↓
[Mark as resolved]
  ↓
[Merge pull request]
```

**Mobile Browser:**
```
[Pull Request]
  ↓
[Resolve conflicts]
  ↓
[Web editor opens]
  ↓
Delete all content in each file
  ↓
[Mark as resolved]
  ↓
[Commit merge]
  ↓
[Merge pull request]
```

---

### Troubleshooting

**Can't see "Resolve conflicts" button?**
- Make sure you're viewing the Pull Request (not just the branch)
- Scroll down past the conversation
- Look for a yellow/orange banner

**Too hard to edit on phone?**
- Use "Desktop site" mode in browser settings
- Or wait until you have access to a computer
- The branch is ready - merge can wait

**Accidentally kept the wrong version?**
- Don't worry! You can:
  - Close the PR and create a new one
  - Or manually delete the files after merge
  - Or ask for help to revert the merge

---

### After Successful Merge

✅ You should see:
- "Pull request successfully merged"
- Branch can be deleted (optional)
- Main branch now has Route Corridor Calculator v2.0

✅ Verify in `custom_gpt_upload/`:
- 14 files total
- New v2.0 documentation present
- Old 5 files gone

---

### Summary for Phone

**Simplest approach:**

1. Open GitHub (app or browser)
2. Go to Pull Request
3. Tap "Resolve conflicts"
4. For all 5 files → Choose "incoming" or "delete"
5. Tap "Mark resolved"
6. Tap "Merge pull request"

**Remember**: Accept deletion of all 5 files - they're replaced by better v2.0 docs!

---

**Need help?** These files are safe to delete. They're old versions superseded by new documentation.
