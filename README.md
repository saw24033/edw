# 🚂 Stepford County Railway GPT - AI Navigation Assistant

An intelligent custom GPT that provides real-time public transport navigation for the Stepford County Railway network using Python code execution.

## 🎯 What This Does

This GPT acts as a **real-world public transport information system**, helping passengers plan journeys across 71 stations and 89 routes. It uses Python (Code Interpreter) to analyze route data and provide:

- **Direct route finding** between any two stations
- **Multi-leg journey planning** with interchange optimization
- **Travel time calculations** including interchange penalties
- **Station information** (routes served, connections, hub status)
- **Intelligent route ranking** by speed and convenience

## 📁 Files Included

| File | Purpose |
|------|---------|
| `stepford_routes_with_segment_minutes_ai_knowledge_base.json` | Complete network data (71 stations, 89 routes) |
| `gpt_system_prompt.txt` | Instructions that make the GPT behave like a transport assistant |
| `navigation_helper.py` | Reference Python code for route planning algorithms |
| `GPT_SETUP_INSTRUCTIONS.md` | Complete step-by-step setup guide |
| `README.md` | This file |

## 🚀 Quick Start

### Prerequisites
- ChatGPT Plus or Enterprise account
- Access to GPT builder

### Setup (5 minutes)
1. Go to [ChatGPT](https://chat.openai.com/) → My GPTs → Create
2. **Enable Code Interpreter** in Capabilities
3. **Upload** `stepford_routes_with_segment_minutes_ai_knowledge_base.json` to Knowledge
4. **Paste** contents of `gpt_system_prompt.txt` into Instructions
5. **Save** and test!

📖 **Full guide:** See `GPT_SETUP_INSTRUCTIONS.md` for detailed instructions

## 💡 Example Usage

### Query:
```
"How do I get from Stepford Central to Airport Terminal 1?"
```

### GPT Response:
```
I've found 2 ways to get from Stepford Central to Airport Terminal 1:

**Option 1 - Direct Route (Fastest)**
🚆 Airport Connect Service
- Route: R001
- Travel time: 18 minutes
- Stops: 10
- Price: 450 Points
- Stations: Stepford Central → Stepford East → St Helens Bridge →
  Angel Pass → Bodin → Coxly → Benton → Benton Bridge →
  Stepford Airport Parkway → Airport Terminal 1

**Option 2 - Via Benton**
🚆 Route R005 → Change at Benton → Route R046
- Total time: ~25 minutes (including 4 min interchange)
- Total stops: 12

I'd recommend Option 1 - it's direct and takes just 18 minutes!
```

## 🧠 How It Works

1. User asks for journey directions
2. GPT automatically writes Python code to:
   - Load the JSON knowledge base
   - Search for direct routes
   - Find alternative routes with interchanges
   - Calculate total journey times
   - Rank options by speed
3. Python code runs in isolated sandbox
4. Results formatted in passenger-friendly language
5. User gets clear, accurate journey plans

## 🎯 Key Features

### Smart Route Finding
- Direct routes prioritized
- Multi-interchange alternatives when needed
- Journey time calculation with 4-minute interchange penalties

### Station Intelligence
- Identifies major interchange hubs
- Shows all routes serving a station
- Lists possible connections

### Fuzzy Search
- Handles misspelled station names
- Suggests corrections
- Partial name matching

### Natural Language
- Responds like a helpful station assistant
- Clear, passenger-focused language
- No robotic technical jargon

## 📊 Network Coverage

- **71 Stations** across the Stepford County Railway network
- **89 Routes** operated by multiple companies
- **Multiple operators:** Stepford Connect, Express, Regional services
- **Route types:** Airport Connect, Express, Regional, Local

## 🛠️ Technical Details

### Knowledge Base Structure
```json
{
  "metadata": {...},
  "stations": ["Station 1", "Station 2", ...],
  "station_index": {
    "Station": {
      "routes": ["R001", ...],
      "interchanges": ["Other Station"],
      "connections": 5
    }
  },
  "routes": {
    "R001": {
      "operator": "Stepford Connect",
      "origin": "Start",
      "destination": "End",
      "stations": [...],
      "travel_time": {"up": "18 minutes"},
      "price": "450 Points"
    }
  }
}
```

### Python Functions Used
- `find_direct_routes()` - Direct connections
- `find_one_interchange_routes()` - Routes with one change
- `calculate_journey_time()` - Total time including interchanges
- `get_station_info()` - Station details
- `search_station_name()` - Fuzzy station search

## 🎨 Customization

### Change Response Style
Edit `gpt_system_prompt.txt` → **RESPONSE STYLE** section
- Adjust formality level
- Add regional character
- Include more/less detail

### Update Network Data
Replace `stepford_routes_with_segment_minutes_ai_knowledge_base.json` with new data
- GPT automatically uses updated routes
- No code changes needed

### Add New Features
Extend the system prompt to include:
- Accessibility information
- Real-time disruptions
- Ticket pricing calculations
- Station amenity details

## 🧪 Testing Scenarios

Test your GPT with these queries:

1. **Direct route:** "How do I get from Stepford Central to Newry?"
2. **Complex journey:** "Best way to reach Airport Terminal 1 from Llyn-by-the-Sea?"
3. **Station info:** "What routes serve Benton?"
4. **Search:** "Find stations with 'Leighton' in the name"
5. **Edge case:** "How do I get to XYZ Station?" (non-existent)

## 📈 Future Enhancements

Potential additions:
- Live service disruption alerts
- Peak/off-peak travel advice
- Multi-modal journey planning (bus + train)
- Fare calculation for complete journeys
- Station facility information
- Accessibility routing options
- Visual network map display

## ⚠️ Limitations

- No real-time data (uses static JSON)
- No internet access (Code Interpreter sandbox)
- Standard Python libraries only
- Session data doesn't persist between chats
- Maximum 512 MB knowledge file size

## 📚 Documentation

- **Setup Guide:** `GPT_SETUP_INSTRUCTIONS.md` - Complete setup walkthrough
- **System Prompt:** `gpt_system_prompt.txt` - GPT behavior instructions
- **Code Reference:** `navigation_helper.py` - Python implementation examples

## 🤝 Contributing

To update the network data:
1. Edit the JSON file with new routes/stations
2. Maintain the existing structure
3. Re-upload to the GPT
4. Test with the new data

## 📝 License

This is a custom GPT configuration for the Stepford County Railway network. Adapt and customize as needed for your own transport networks.

## 🎉 Credits

Built for Stepford County Railway to demonstrate how custom GPTs can be used as intelligent public transport information systems using Python code execution.

---

**Ready to build your GPT?** Start with `GPT_SETUP_INSTRUCTIONS.md`

**Questions?** Check the Troubleshooting section in the setup guide

**Happy travels! 🚂**
