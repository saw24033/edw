# Stepford County Railway GPT - Setup Instructions

## 📋 Overview

This guide will help you create a custom GPT that acts as an intelligent public transport navigation system for the Stepford County Railway network. The GPT will use Python (Code Interpreter) to analyze route data and provide real-time journey planning assistance.

---

## 🎯 What You Need

1. **ChatGPT Plus or Enterprise account** (required for custom GPTs and Code Interpreter)
2. **The files in this repository:**
   - `stepford_routes_with_segment_minutes_ai_knowledge_base.json` - Network data
   - `gpt_system_prompt.txt` - Instructions for the GPT
   - `navigation_helper.py` - Reference code for the GPT

---

## 🚀 Step-by-Step Setup

### Step 1: Create a New GPT

1. Go to [https://chat.openai.com/](https://chat.openai.com/)
2. Click your profile icon (bottom left)
3. Select **"My GPTs"**
4. Click **"Create a GPT"**

### Step 2: Configure Basic Settings

1. **Name:** `Stepford County Railway Assistant`

2. **Description:**
   ```
   Your intelligent travel assistant for the Stepford County Railway network. Get real-time route planning, journey times, and interchange information for all 71 stations and 89 routes.
   ```

3. **Profile Picture:** (Optional) Upload a train/railway themed image

### Step 3: Add Instructions (System Prompt)

1. In the GPT editor, go to the **"Configure"** tab
2. In the **"Instructions"** field, paste the ENTIRE contents of `gpt_system_prompt.txt`
3. This tells the GPT how to behave like a real transport information system

### Step 4: Enable Code Interpreter (CRITICAL!)

1. Scroll down to the **"Capabilities"** section
2. **Toggle ON** the switch for **"Code Interpreter"**
3. This allows the GPT to run Python code to analyze routes

### Step 5: Upload Knowledge Files

1. Scroll to the **"Knowledge"** section
2. Click **"Upload files"**
3. Upload these files:
   - ✅ `stepford_routes_with_segment_minutes_ai_knowledge_base.json`
   - ✅ `navigation_helper.py` (optional but helpful as reference)

**Important:** The JSON file MUST be uploaded for the GPT to work!

### Step 6: Configure Conversation Starters

Add these example prompts so users know what to ask:

```
1. "How do I get from Stepford Central to Airport Terminal 1?"
2. "What routes serve Benton station?"
3. "Find me the fastest route to Newry Harbour"
4. "Show me all stations with 'Airport' in the name"
```

### Step 7: Save and Test

1. Click **"Save"** in the top right
2. Choose visibility:
   - **"Only me"** - Private use
   - **"Anyone with a link"** - Share with friends
   - **"Public"** - List in GPT store (if eligible)

3. **Test it!** Try asking:
   ```
   "I need to get from Stepford Central to Newry. What are my options?"
   ```

---

## 🧪 Testing Your GPT

Once created, test with these scenarios:

### Test 1: Direct Route Query
**Ask:**
```
"How do I get from Stepford Central to Stepford Airport Central?"
```

**Expected behavior:**
- GPT runs Python code to analyze routes
- Shows direct route options
- Includes travel time, stops, and price
- Displays station sequence

### Test 2: Multi-Interchange Journey
**Ask:**
```
"What's the best way to get from Llyn-by-the-Sea to Airport Terminal 1?"
```

**Expected behavior:**
- GPT finds routes requiring interchanges
- Calculates total journey time including interchange penalties
- Ranks options by speed and convenience

### Test 3: Station Information
**Ask:**
```
"Tell me about Benton station"
```

**Expected behavior:**
- GPT loads station data using Python
- Shows number of routes serving the station
- Lists interchange connections
- Identifies if it's a major hub

### Test 4: Station Search
**Ask:**
```
"Which stations have 'Leighton' in their name?"
```

**Expected behavior:**
- Searches station list
- Returns matching station names
- May provide additional context about each

---

## 💡 How It Works Behind the Scenes

### When a User Asks for Directions:

1. **GPT receives the query** (e.g., "How do I get from A to B?")

2. **GPT automatically writes Python code:**
   ```python
   import json

   # Load network data
   with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json', 'r') as f:
       network = json.load(f)

   # Find routes connecting the stations
   # ... navigation logic ...
   ```

3. **Code runs in isolated sandbox** (Code Interpreter environment)

4. **GPT receives results** and formats them in a passenger-friendly way

5. **User gets clear, accurate journey options** with times and interchanges

### The Python Code:

The GPT uses the patterns from `navigation_helper.py` to:
- Search for direct routes between stations
- Find connections requiring interchanges
- Calculate total journey times
- Rank routes by speed and convenience
- Format results in a readable way

---

## 📊 Knowledge Base Structure

The JSON file contains:

```json
{
  "metadata": {
    "total_stations": 71,
    "total_routes": 89
  },
  "stations": ["Station 1", "Station 2", ...],
  "station_index": {
    "Station Name": {
      "routes": ["R001", "R002"],
      "interchanges": ["Other Station"],
      "connections": 5
    }
  },
  "routes": {
    "R001": {
      "operator": "Stepford Connect",
      "origin": "Stepford Central",
      "destination": "Airport",
      "stations": [...],
      "travel_time": {"up": "18 minutes"},
      "price": "450 Points"
    }
  }
}
```

---

## 🛠️ Customization Options

### Change the Assistant's Personality

Edit `gpt_system_prompt.txt` and modify the **RESPONSE STYLE** section:

- Make it more formal/casual
- Add humor or regional dialect
- Include railway enthusiast facts
- Add emoji variety

### Add New Features

You can extend the system prompt to:
- Provide accessibility information
- Show ticket purchasing guidance
- Include service disruption alerts
- Suggest tourist destinations near stations

### Update Route Data

When routes change:
1. Update the JSON file with new routes/stations
2. Re-upload to the GPT
3. The GPT will automatically use the new data

---

## ⚠️ Important Notes

### File Access in Code Interpreter

The GPT can access files using simple paths:
```python
# ✅ Correct
with open('stepford_routes_with_segment_minutes_ai_knowledge_base.json', 'r') as f:
    data = json.load(f)

# ❌ Wrong - Don't use full paths
with open('/mnt/data/stepford_routes...', 'r') as f:
```

### Session Persistence

- Python environment **resets between conversations**
- Each new chat loads fresh - no memory of previous sessions
- Variables don't persist across messages (but files do)

### Limitations

- No internet access (only local knowledge files)
- Can't make real-time API calls
- Standard library + NumPy, Pandas, Matplotlib only
- No installing new packages

### File Size Limits

- Maximum 512 MB total across all knowledge files
- Your JSON (~400KB) is well within limits
- Can upload multiple files if needed

---

## 🎨 Example Interactions

### Example 1: Basic Journey Query

**User:**
```
I need to travel from Stepford Central to Newry Harbour. What's the quickest way?
```

**GPT Response:**
```
I'll find the best routes for you from Stepford Central to Newry Harbour.

[Runs Python code to analyze routes]

I've found a direct route:

**Option 1 - Direct Route (Fastest)**
🚆 Connect Service to Newry Harbour
- Route: R002
- Operator: Stepford Connect
- Travel time: 12 minutes
- Stops: 5
- Price: 350 Points
- Stations: Stepford Central → Stepford Victoria → James Street →
            Connolly → Newry → Newry Harbour

This is the fastest option - just 12 minutes with no changes needed!
```

### Example 2: Complex Journey with Interchanges

**User:**
```
How do I get to Airport Terminal 1 from Beechley?
```

**GPT Response:**
```
Let me check the best routes from Beechley to Airport Terminal 1.

[Runs Python code]

I've found several options:

**Option 1 - Via Benton (Recommended)**
🚆 Route R032 → Change at Benton → Route R046
- Total time: ~23 minutes (including 4 min interchange)
- Change at: Benton
- Total stops: 8

**Option 2 - Via Stepford Central**
🚆 Route R103 → Change at Stepford Central → Route R001
- Total time: ~28 minutes (including 4 min interchange)
- Change at: Stepford Central
- Total stops: 12

I'd recommend Option 1 - it's faster and requires only one change at Benton,
which is a major interchange hub with good connections.
```

---

## 🐛 Troubleshooting

### "I can't see the Python code running"

**Solution:** The GPT runs code in the background. If you want to see it:
- Ask: "Show me the Python code you're using"
- The GPT will display its analysis logic

### "The GPT says it can't find the file"

**Check:**
1. Did you upload the JSON file in the Knowledge section?
2. Is Code Interpreter enabled?
3. Try asking: "List the files you have access to"

### "Routes seem incorrect"

**Verify:**
1. The JSON file is properly formatted (valid JSON)
2. Station names match exactly (case-sensitive)
3. Route data is complete

### "GPT isn't using Python"

**Fix:**
1. Ensure Code Interpreter is enabled in Capabilities
2. The system prompt tells it to "Use Python" - check this is included
3. Ask explicitly: "Use Python to find routes between X and Y"

---

## 📈 Next Steps

### Enhancements You Can Add:

1. **Live Service Updates**
   - Add a text file with service disruptions
   - GPT reads and announces delays

2. **Fare Calculator**
   - Extend Python code to sum prices for multi-leg journeys
   - Apply discounts for return tickets

3. **Station Amenities**
   - Add JSON with facilities info (parking, accessibility, cafes)
   - GPT includes this in station information

4. **Visual Maps**
   - Upload a network map image
   - GPT can display it when asked "Show me the network map"

5. **Peak Time Advice**
   - Add crowding data
   - GPT suggests less busy routes during peak hours

---

## 📚 Additional Resources

### OpenAI Documentation
- [Creating GPTs](https://help.openai.com/en/articles/8554397-creating-a-gpt)
- [Code Interpreter Guide](https://platform.openai.com/docs/guides/code-interpreter)

### Python JSON Handling
- [Python JSON Tutorial](https://docs.python.org/3/library/json.html)

### GPT Best Practices
- Keep instructions clear and structured
- Test thoroughly with edge cases
- Update knowledge files when data changes

---

## ✅ Final Checklist

Before publishing your GPT:

- [ ] Code Interpreter is enabled
- [ ] JSON knowledge file is uploaded
- [ ] System prompt is pasted in Instructions
- [ ] Conversation starters are added
- [ ] Tested with multiple journey queries
- [ ] Tested station information queries
- [ ] Tested edge cases (non-existent stations)
- [ ] Response style matches your preference
- [ ] Privacy settings are configured

---

## 🎉 You're Done!

You now have a fully functional public transport navigation GPT that uses Python to intelligently route passengers across the Stepford County Railway network.

**Share it, use it, and enjoy your AI-powered railway assistant!**

---

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all files are uploaded correctly
3. Test with the provided example queries
4. Review the system prompt for any modifications you made

**Happy travels on the Stepford County Railway! 🚂**
