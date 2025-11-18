# 📂 Custom GPT Upload Files - Ready to Go!

This folder contains **everything you need** to create your Stepford County Railway Custom GPT.

**🆕 Latest Updates:** See [CHANGELOG.md](CHANGELOG.md) for recent improvements including route-specific platform mapping and improved pathfinding!

---

## ✅ Files in This Folder (7 + Instructions)

### Files to Upload to Custom GPT Knowledge Section:

1. **rail_routes.csv** (61 KB)
   - Route network data with all train segments

2. **rail_helpers.py** (20 KB)
   - Python functions for route queries

3. **station_coords.csv** (1.8 KB)
   - Station coordinates for network maps

4. **plot_helpers.py** (7 KB)
   - Visualization functions

5. **scr_stations_part1.md** (368 KB) ⭐
   - Station wiki content for stations 1-41

6. **scr_stations_part2.md** (385 KB) ⭐
   - Station wiki content for stations 42-82

7. **station_knowledge_helper.py** (6 KB) ⭐
   - Parser for station knowledge

### Instructions Files:

8. **custom_gpt_instructions_COMPACT.txt** (6.7 KB) ⭐ **USE THIS**
   - Streamlined instructions under 8,000 character limit
   - Copy/paste this into your GPT's Instructions field

9. **GPT_USAGE_GUIDE.md** (16 KB) ⭐ **UPLOAD AS KNOWLEDGE FILE**
   - Detailed examples, workflows, and best practices
   - GPT references this for complex queries
   - Offloads instruction burden from system prompt

~~custom_gpt_instructions_with_station_knowledge.txt~~ (14 KB - TOO LONG, use COMPACT version instead)

**Total Upload Size:** ~843 KB ✅

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Custom GPT
1. Go to [ChatGPT](https://chat.openai.com/)
2. Click your profile → **My GPTs** → **Create a GPT**
3. Switch to **Configure** tab

### Step 2: Basic Info
- **Name:** Stepford County Railway Expert
- **Description:** Complete railway assistant with route planning, station details, history, and trivia for all 82 SCR stations

### Step 3: Enable Code Interpreter
- Scroll to **Capabilities**
- Toggle **ON**: Code Interpreter ✅ (REQUIRED!)

### Step 4: Upload Files
- Scroll to **Knowledge**
- Click **Upload files**
- Upload ALL **8 files** from this folder:
  - rail_routes.csv
  - rail_helpers.py
  - station_coords.csv
  - plot_helpers.py
  - scr_stations_part1.md
  - scr_stations_part2.md
  - station_knowledge_helper.py
  - **GPT_USAGE_GUIDE.md** ⭐ NEW - detailed examples for GPT to reference

### Step 5: Add Instructions
1. Open `custom_gpt_instructions_COMPACT.txt`
2. Select all and copy (6,680 characters - well under 8,000 limit!)
3. Paste into the **Instructions** field in your GPT

### Step 6: Add Conversation Starters
Add these 5 example prompts:

```
How do I get from Stepford Central to Benton?
```

```
Tell me everything about Airport Terminal 1
```

```
What's the history of Stepford Airport Central?
```

```
Which stations have the most platforms?
```

```
Show me interesting facts about Llyn-by-the-Sea
```

### Step 7: Save & Test
1. Click **Save**
2. Choose who can access it (Only me / Link / Public)
3. Test with: "Tell me about Benton station including its history"

---

## ✅ What Your GPT Will Know

### Route Planning:
- Find routes between any two stations (prioritizes direct routes!)
- Show all operators and lines
- Calculate journey times with transfers
- Visualize network maps
- **⭐ Route-specific platform guidance** (e.g., "R001 departs from Platforms 1, 4")

### Station Details:
- Platforms and tracks for all 82 stations
- **⭐ Accurate operator-to-platform mapping** (handles both ranges and individual platforms)
- Accessibility information
- Station codes and zones
- District locations

### Historical Information:
- When each station was built
- Major updates by game version
- Station renovations and changes

### Trivia & Facts:
- Real-life station inspirations
- Unique features per station
- Interesting historical tidbits

---

## 📊 File Verification

All files under 512 KB limit:

| File | Size | Status |
|------|------|--------|
| rail_routes.csv | 61 KB | ✅ |
| rail_helpers.py | 20 KB | ✅ |
| station_coords.csv | 1.8 KB | ✅ |
| plot_helpers.py | 7 KB | ✅ |
| scr_stations_part1.md | 368 KB | ✅ |
| scr_stations_part2.md | 385 KB | ✅ |
| station_knowledge_helper.py | 6 KB | ✅ |
| **TOTAL** | **843 KB** | ✅ |

---

## 🧪 Test Your GPT

After setup, test with these queries:

**Route Planning:**
```
How do I get from Benton to Llyn-by-the-Sea?
```

**Station Details:**
```
How many platforms does Stepford Central have?
```

**Station History:**
```
When was Airport Terminal 1 added to the network?
```

**Comprehensive Query:**
```
Tell me everything about Benton station - routes, details, and history
```

**Expected:** Your GPT should provide detailed answers with platform counts, operators, historical timeline, and trivia!

---

## ⚠️ Important Notes

### Why Two Station Files?
Custom GPT has a 512 KB per-file limit. The station content was split into:
- Part 1: Stations 1-41 (368 KB)
- Part 2: Stations 42-82 (385 KB)

The helper automatically combines them - your GPT will see all 82 stations!

### Must Have Code Interpreter!
Without Code Interpreter enabled, your GPT **cannot run Python code** and won't work properly.

### All 7 Files Required
Each file serves a purpose:
- CSV files = route data
- Python files = query functions
- Markdown files = station knowledge
- Missing any file = incomplete functionality

---

## 🎉 You're Ready!

Everything you need is in this folder. Just follow the steps above and you'll have a fully functional railway assistant GPT in minutes!

**Questions?** Check the main documentation files in the parent directory.

**Happy uploading! 🚂**
