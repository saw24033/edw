# 🚂 Stepford County Railway Custom GPT – Train Network Assistant

A Python-powered Custom GPT that acts as a railway information expert for the Stepford County Railway system.

## 🎯 What This Does

This GPT uses **Code Interpreter** to run real Python code that analyzes train network data. No hallucinations, no made-up routes – just accurate answers from real CSV data.

Your GPT can answer:
- "Which operators serve Stepford Central?"
- "Is there a direct train from A to B?"
- "Show me all routes operated by AirLink"
- "Draw the Metro network map"
- "Find stations with 'Airport' in the name"

**Covers:** 71 stations • 89 lines • 5 operators • 658 train segments

## 📁 Files Included

### Core Data Files
| File | Purpose |
|------|---------|
| `rail_routes.csv` | **Edge-based network data** – all train segments between stations |
| `station_coords.csv` | **Station coordinates** – x/y positions for map visualization |
| `stepford_routes_with_segment_minutes_ai_knowledge_base.json` | Original complete network data (source) |

### Python Code Files
| File | Purpose |
|------|---------|
| `rail_helpers.py` | **Network query functions** – find routes, operators, connections |
| `plot_helpers.py` | **Visualization functions** – draw network maps with matplotlib |

### GPT Configuration Files
| File | Purpose |
|------|---------|
| `custom_gpt_instructions.txt` | **GPT system prompt** – the "brain" that controls behavior |
| `CUSTOM_GPT_SETUP_GUIDE.md` | **Complete setup guide** – step-by-step instructions |
| `README.md` | This file – project overview |

### Utility Scripts
| File | Purpose |
|------|---------|
| `convert_to_edges.py` | Convert JSON to edge-based CSV format |
| `generate_coordinates.py` | Generate station coordinates for plotting |

## 🚀 Quick Start

### Prerequisites
- ChatGPT Plus or Enterprise account (required for Custom GPTs)
- Access to GPT builder

### Setup (5 minutes)
1. Go to [ChatGPT](https://chat.openai.com/) → My GPTs → **Create**
2. Switch to **Configure** tab
3. **Enable Code Interpreter** in Capabilities
4. **Upload 4 files** to Knowledge:
   - `rail_routes.csv`
   - `rail_helpers.py`
   - `plot_helpers.py`
   - `station_coords.csv`
5. **Copy/paste** entire contents of `custom_gpt_instructions.txt` into Instructions
6. **Save** and test!

📖 **Full guide:** See `CUSTOM_GPT_SETUP_GUIDE.md` for detailed step-by-step instructions

## 💡 Example Usage

### Query 1: Station Operators
```
"Which operators serve Benton?"
```

**GPT Response:**
```
At Benton, the following operators run trains:
- Metro
- Stepford Connect
- Stepford Express
- Waterline

Benton is a major hub with connections to 42 different lines.
```

**Behind the scenes (Python):**
```python
import rail_helpers
graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
rail_helpers.operators_at_station(graph, "Benton")
```

---

### Query 2: Direct Routes
```
"Is there a direct train from Stepford Central to Benton?"
```

**GPT Response:**
```
Yes! There are direct trains from Stepford Central to Benton:

Option 1:
- Operator: Stepford Express
- Line: R075
- Travel time: 5.0 minutes
- Service type: Benton Express

Option 2:
- Operator: Stepford Express
- Line: R078
- Travel time: 4.0 minutes
- Service type: Llyn via Benton

The fastest option is Line R078 at 4 minutes.
```

---

### Query 3: Network Visualization
```
"Draw the AirLink network map"
```

**GPT Response:**
```
Here's the network map for AirLink services:

[Shows matplotlib plot with stations and connections]

The map shows all stations served by AirLink and the direct connections
between them. Red dots represent stations, and blue lines represent
direct services.
```

## 🧠 How It Works

### The Data Model: Edge-Based Graph

Unlike traditional route-based systems, this uses an **edge-based network graph**:

- **Node** = Station (e.g., "Stepford Central")
- **Edge** = Direct train segment between two stations

From `rail_routes.csv`:
```csv
operator,line,from_station,to_station,travel_time_min,service_type
AirLink,R051,Stepford Central,Stepford Airport Central,8.0,Speed Link
```

This makes querying fast and flexible.

### The Workflow

1. **User asks a question**
   "Which operators serve Stepford Central?"

2. **GPT automatically writes Python code**
   ```python
   import rail_helpers
   graph, ops, lines = rail_helpers.load_rail_network("rail_routes.csv")
   rail_helpers.operators_at_station(graph, "Stepford Central")
   ```

3. **Code Interpreter runs the code** in a sandbox

4. **Returns accurate data** from the CSV
   `['AirLink', 'Metro', 'Stepford Connect', 'Stepford Express']`

5. **GPT formats the answer** in natural language
   "At Stepford Central, the following operators run trains:..."

No hallucinations. No fake routes. Just real data.

## 🎯 Key Features

### Python-Powered Accuracy
- Runs real code for every query
- No hallucinations or made-up routes
- Always queries actual CSV data

### Operator & Line Analysis
- Find all operators serving a station
- Show complete network for any operator
- Map individual lines or entire networks

### Station Intelligence
- Comprehensive station information
- Identify major hubs (10+ lines)
- List direct connections
- Fuzzy search for station names

### Network Visualization
- Draw operator-specific network maps
- Visualize individual lines
- Plot the entire Stepford County Railway system
- Uses matplotlib for professional diagrams

### Natural Language Interface
- Ask questions in plain English
- Get passenger-friendly answers
- Clear bullet-point formatting
- Helpful error messages with suggestions

## 📊 Network Coverage

- **71 Stations** across the Stepford County Railway network
- **89 Lines** operated by 5 companies
- **658 Train segments** (edges in the network graph)
- **5 Operators:** AirLink, Metro, Stepford Connect, Stepford Express, Waterline
- **Service types:** Airport Connect, Express, Regional, Metro, Speed Link

## 🛠️ Technical Details

### Data Format: Edge-Based CSV

The core data file `rail_routes.csv` uses an edge-based format:

```csv
operator,line,from_station,to_station,travel_time_min,service_type
AirLink,R051,Stepford Central,Stepford Airport Central,8.0,Speed Link
Metro,R022,Stepford Central,Stepford Victoria,1.2,Waterline Circle
Stepford Connect,R001,Stepford Central,Stepford East,1.8,Airport Connect
```

Each row = one direct train segment between two stations.

### Python Helper Functions (rail_helpers.py)

Core query functions:
- `load_rail_network(path)` → Load CSV into graph structure
- `operators_at_station(graph, station)` → List operators serving a station
- `lines_at_station(graph, station)` → List lines serving a station
- `direct_services_between(graph, a, b)` → Find direct trains between stations
- `edges_for_operator(graph, operator)` → Get all segments for an operator
- `edges_for_line(graph, line_id)` → Get all segments for a line
- `station_info(graph, station)` → Comprehensive station data
- `station_connections(graph, station)` → Directly connected stations
- `search_stations(graph, query)` → Fuzzy search for stations
- `find_interchanges(graph, a, b)` → Potential interchange stations

### Plotting Functions (plot_helpers.py)

Visualization tools:
- `load_station_coords(path)` → Load station x/y coordinates
- `plot_operator_network(graph, operator, coords)` → Draw operator map
- `plot_line_network(graph, line_id, coords)` → Draw single line map
- `plot_full_network(graph, coords)` → Draw entire railway system

## 🎨 Customization

### Change Response Style
Edit `custom_gpt_instructions.txt` → **YOUR PERSONALITY** section:
- Adjust formality level (professional vs. casual)
- Add regional character or dialect
- Include railway enthusiast facts
- Customize greeting behavior

### Update Network Data
When routes change:
1. Edit `rail_routes.csv` directly, OR
2. Update the JSON and re-run `convert_to_edges.py`
3. Re-upload `rail_routes.csv` to the GPT
4. The GPT automatically uses the new data

### Add New Python Functions
Extend `rail_helpers.py` with custom queries:
- Shortest path between stations (Dijkstra's algorithm)
- Find all stations on a specific operator
- Calculate average travel times
- Identify network bottlenecks

Then update the instructions to reference your new functions.

### Add External Data
Use GPT Actions to call external APIs:
- Real-time train tracking
- Live service disruptions
- Dynamic pricing
- Weather-based delays

## 🧪 Testing Scenarios

Test your GPT with these queries:

1. **Station operators:** "Which operators serve Stepford Central?"
2. **Direct routes:** "Is there a direct train from Stepford Central to Benton?"
3. **Operator networks:** "Show me all routes operated by AirLink"
4. **Station search:** "Find stations with 'Airport' in the name"
5. **Station info:** "Tell me about Benton station"
6. **Visualization:** "Draw the Metro network map"
7. **Line details:** "What stations are on line R001?"
8. **Edge case:** "How do I get to FakeStation?" (should suggest corrections)

## 📈 Future Enhancements

Potential additions:
- **Multi-hop routing** – Dijkstra's algorithm for complex journeys
- **Live data integration** – Real-time delays via GPT Actions
- **Fare calculator** – Total journey costs with transfers
- **Accessibility routing** – Step-free route planning
- **Peak time analysis** – Crowding and frequency data
- **Station facilities** – Parking, cafes, accessibility info
- **Historical analysis** – Usage patterns and statistics
- **Multi-modal planning** – Integrate bus/tram connections

## ⚠️ Limitations

### Code Interpreter Environment
- Resets between conversations (no persistent state)
- No internet access (only local files)
- Standard libraries + NumPy, Pandas, Matplotlib only
- Can't install additional packages

### Current Functionality
- No multi-transfer journey planning (yet)
- No real-time schedule information
- No ticket pricing (except route metadata)
- No accessibility information
- Coordinates are generated (not real geographic data)

### Data Constraints
- Static CSV data (updated manually)
- Travel times are estimates per segment
- No train frequency information
- No platform or track details

See `CUSTOM_GPT_SETUP_GUIDE.md` for workarounds and enhancement ideas.

## 📚 Documentation

- **Setup Guide:** `CUSTOM_GPT_SETUP_GUIDE.md` - Complete step-by-step walkthrough
- **System Instructions:** `custom_gpt_instructions.txt` - GPT behavior and workflow
- **Python Helpers:** `rail_helpers.py` - Network query function reference
- **Plot Helpers:** `plot_helpers.py` - Visualization function reference

## 🤝 Contributing & Extending

### Update Network Data
1. Edit `rail_routes.csv` directly with new train segments, OR
2. Update `stepford_routes_with_segment_minutes_ai_knowledge_base.json` and re-run `convert_to_edges.py`
3. Re-upload the CSV to your GPT
4. Test with sample queries

### Add New Helper Functions
1. Edit `rail_helpers.py` with your new function
2. Test it locally: `python3 rail_helpers.py`
3. Update `custom_gpt_instructions.txt` to mention the new function
4. Re-upload both files to the GPT

### Improve Visualizations
1. Edit `plot_helpers.py` with new plotting logic
2. Test locally with matplotlib
3. Re-upload to GPT
4. Try visualization queries

### Adapt for Other Transit Systems
This system works for **any network of nodes and edges**:
- Bus networks
- Metro systems
- Flight routes
- Power grids
- Road networks
- Supply chains

Just replace `rail_routes.csv` with your own edge data!

## 📝 License

This is a custom GPT configuration for the Stepford County Railway network. Adapt and customize as needed for your own transport networks, games, or data systems.

## 🎉 Credits

Built for Stepford County Railway to demonstrate how Custom GPTs + Python Code Interpreter can create intelligent, data-driven assistants that never hallucinate.

**Key Concept:** Edge-based graph + helper functions + strict instructions = Accurate AI

---

## 🚀 Ready to Build?

**📖 Full Setup Guide:** [`CUSTOM_GPT_SETUP_GUIDE.md`](CUSTOM_GPT_SETUP_GUIDE.md)

**❓ Questions?** Check the Troubleshooting section in the setup guide

**🎯 Quick Start:**
1. Create a Custom GPT
2. Enable Code Interpreter
3. Upload 4 files: `rail_routes.csv`, `rail_helpers.py`, `plot_helpers.py`, `station_coords.csv`
4. Paste `custom_gpt_instructions.txt` into Instructions
5. Test with: "Which operators serve Stepford Central?"

**Happy railway engineering! 🚂**
