# ✅ Custom GPT Upload Checklist

## Files to Upload (7 Total)

Upload these files to your Custom GPT's **Knowledge** section:

### Core Network Files (4 files)
- [ ] `rail_routes.csv` (61 KB)
- [ ] `rail_helpers.py` (20 KB)
- [ ] `station_coords.csv` (1.8 KB)
- [ ] `plot_helpers.py` (7 KB)

### Station Knowledge Files (3 files) ⭐
- [ ] `scr_stations_part1.md` (368 KB) - Stations 1-41
- [ ] `scr_stations_part2.md` (385 KB) - Stations 42-82
- [ ] `station_knowledge_helper.py` (6 KB)

**Total Size:** ~843 KB ✅ (under limits)

---

## Important Notes

### Why Two Part Files?
Custom GPT has a **512 KB per-file limit**. The original `scr_stations_full_content.md` was 773 KB, so it was split into:
- Part 1: Stations 1-41 (368 KB) ✅
- Part 2: Stations 42-82 (385 KB) ✅

### How It Works
The `station_knowledge_helper.py` automatically loads **both** part files and combines them into a single dataset with all 82 stations. Your GPT doesn't need to know they're split!

---

## Setup Instructions

### 1. Enable Code Interpreter
In your GPT's Configure tab:
- Toggle **ON**: Code Interpreter

### 2. Upload All 7 Files
Upload all files listed above to the **Knowledge** section

### 3. Add Instructions
Copy/paste from: `custom_gpt_instructions_with_station_knowledge.txt`

### 4. Add Conversation Starters
```
How do I get from Stepford Central to Benton?
Tell me everything about Airport Terminal 1
What's the history of Stepford Airport Central?
Which stations have the most platforms?
Show me interesting facts about Llyn-by-the-Sea
```

### 5. Save & Test
Test with: "Tell me about Benton station including its history"

---

## File Size Breakdown

| File | Size | Under 512KB? |
|------|------|--------------|
| rail_routes.csv | 61 KB | ✅ |
| rail_helpers.py | 20 KB | ✅ |
| station_coords.csv | 1.8 KB | ✅ |
| plot_helpers.py | 7 KB | ✅ |
| scr_stations_part1.md | 368 KB | ✅ |
| scr_stations_part2.md | 385 KB | ✅ |
| station_knowledge_helper.py | 6 KB | ✅ |
| **TOTAL** | **843 KB** | **✅** |

---

## What Your GPT Can Do

### Route Planning
- "How do I get from A to B?"
- "Is there a direct train?"
- "Show me all Metro routes"

### Station Details (NEW!)
- "How many platforms at Benton?" → 13 platforms
- "Is Airport Terminal 1 accessible?" → Step-free via lifts
- "What zone is Stepford Central in?" → Stepford City Zone

### Station History (NEW!)
- "When was Benton built?" → Complete timeline
- "What changed in V1.10?" → Major station overhauls

### Trivia & Facts (NEW!)
- "Interesting facts about Llyn-by-the-Sea"
- "Which real station inspired Benton?"
- "Which station has multilingual signs?" → Airport Terminal 1

---

## Troubleshooting

### "Can't upload, file too large"
✅ **Fixed!** Use the split files:
- `scr_stations_part1.md` (368 KB)
- `scr_stations_part2.md` (385 KB)

**Don't use:** `scr_stations_full_content.md` (773 KB - too large)

### "Station knowledge not working"
Check:
1. Both `scr_stations_part1.md` AND `scr_stations_part2.md` uploaded
2. `station_knowledge_helper.py` uploaded
3. Code Interpreter enabled
4. Using correct instructions file

### "Only getting data for some stations"
Make sure **both** part files are uploaded:
- Part 1 has stations 1-41
- Part 2 has stations 42-82
- Missing either file = incomplete data

---

## Quick Verification

After setup, ask your GPT:
```
How many stations do you have knowledge about?
```

Expected response:
```
I have comprehensive knowledge about all 82 SCR stations...
```

If it says less than 82, check that both part files are uploaded.

---

## Full Documentation

📖 See `STATION_KNOWLEDGE_INTEGRATION_GUIDE.md` for complete details

🚀 See `INTEGRATION_SUMMARY.md` for quick start guide

---

**Ready to upload? Check off each file as you go!** ✅
