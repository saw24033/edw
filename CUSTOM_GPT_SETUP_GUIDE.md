# 🚂 Stepford County Railway Custom GPT – Complete Setup Guide

## Overview

This guide shows you how to create a **train network assistant GPT** that uses Python Code Interpreter to answer questions about the Stepford County Railway system.

Your GPT will be able to:
- Answer "Which operators serve Station X?"
- Find direct routes between stations
- Show all routes for a specific operator or line
- Visualize network maps
- Provide comprehensive station information

All powered by **real data** from CSV files and Python code – no hallucinations, no made-up routes.

---

## 📦 What's In This Repository

| File | Purpose |
|------|---------|
| `rail_routes.csv` | **Edge-based network data** – 658 train segments connecting 71 stations |
| `rail_helpers.py` | **Python helper functions** – query the network, find routes, get station info |
| `plot_helpers.py` | **Visualization functions** – draw network maps with matplotlib |
| `station_coords.csv` | **Station coordinates** – x/y positions for plotting |
| `custom_gpt_instructions.txt` | **GPT system prompt** – the "brain" that tells the GPT how to behave |

---

## 🏗️ How This System Works

### The Data Model: Trains as Edges

Unlike the original JSON (which stored routes as complete journeys), this system uses an **edge-based graph** where:

- **Node** = Station (like "Stepford Central")
- **Edge** = Direct train segment between two stations

Example from `rail_routes.csv`:

```csv
operator,line,from_station,to_station,travel_time_min,service_type
AirLink,R051,Stepford Central,Stepford Airport Central,8.0,Speed Link
Stepford Connect,R001,Stepford Central,Stepford East,1.8,Airport Connect
Metro,R022,Stepford Central,Stepford Victoria,1.2,Waterline Circle
```

This format makes it easy to:
- Find all operators at a station (check all edges touching that node)
- Find direct routes (check if edge A→B exists)
- Build network maps (plot all edges)

### The Python Brain: Helper Functions

The `rail_helpers.py` module provides functions that the GPT will call:

```python
import rail_helpers

# Load the network
graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")

# Query it
rail_helpers.operators_at_station(graph, "Stepford Central")
# Returns: ['AirLink', 'Metro', 'Stepford Connect', 'Stepford Express']

rail_helpers.direct_services_between(graph, "Stepford Central", "Benton")
# Returns: [{'operator': 'Stepford Express', 'line': 'R075', 'time': 5.0, ...}, ...]
```

### The GPT Instructions: The Operating Manual

The `custom_gpt_instructions.txt` file tells the GPT:
1. You are a train network assistant
2. Use Python to load `rail_routes.csv` and `rail_helpers`
3. Never guess – always query the data
4. Format answers clearly for passengers

---

## 🚀 Step-by-Step Setup

### Step 1: Create the Custom GPT

1. Go to [ChatGPT](https://chat.openai.com/)
2. Click your profile → **"My GPTs"**
3. Click **"Create a GPT"**
4. Switch to the **"Configure"** tab (ignore the "Create" chat for now)

### Step 2: Name and Description

**Name:**
```
Stepford County Railway Assistant
```

**Description:**
```
Train network expert for Stepford County Railway. Answers questions about routes, operators, and stations using Python-powered data analysis. Covers 71 stations and 89 lines across 5 operators.
```

**Instructions:**
Copy and paste the **ENTIRE contents** of `custom_gpt_instructions.txt` into the Instructions box.

This is the most important part – it's the GPT's "operating manual."

### Step 3: Enable Code Interpreter

Scroll to **Capabilities** and toggle **ON**:
- ✅ **Code Interpreter** (this is critical!)

Leave the others as default (you can enable web browsing if you want, but it's not needed).

### Step 4: Upload Knowledge Files

Scroll to **Knowledge** and click **"Upload files"**.

Upload these 4 files:
1. ✅ `rail_routes.csv` **(required)**
2. ✅ `rail_helpers.py` **(required)**
3. ✅ `plot_helpers.py` **(required for maps)**
4. ✅ `station_coords.csv` **(required for maps)**

These files become available to the Python Code Interpreter when it runs.

### Step 5: Add Conversation Starters

These are example prompts users see when they open your GPT.

Add these four:

```
Which operators serve Stepford Central?
```

```
Is there a direct train from Stepford Central to Benton?
```

```
Show me all routes operated by AirLink
```

```
Draw the network map for Metro services
```

### Step 6: Configure Actions (Skip This)

You don't need Actions for this GPT. That's for calling external APIs.

### Step 7: Save and Choose Privacy

Click **"Save"** in the top right.

Choose who can access it:
- **Only me** – Private (recommended for testing)
- **Anyone with a link** – Shareable with friends
- **Public** – Listed in GPT store (requires OpenAI approval)

---

## 🧪 Testing Your GPT

Once saved, click **"View GPT"** or open it from your GPT list.

### Test 1: Station Query

**Ask:**
```
Which operators serve Benton?
```

**Expected response:**
```
At Benton, the following operators run trains:
- Metro
- Stepford Connect
- Stepford Express
- Waterline

Benton is a major hub with connections to 42 different lines.
```

Behind the scenes, the GPT ran:
```python
import rail_helpers
graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
rail_helpers.operators_at_station(graph, "Benton")
```

### Test 2: Direct Route Query

**Ask:**
```
Is there a direct train from Stepford Central to Stepford Airport Central?
```

**Expected response:**
```
Yes! There are direct trains from Stepford Central to Stepford Airport Central:

Option 1:
- Operator: AirLink
- Line: R051
- Travel time: 8.0 minutes
- Service type: Speed Link

Option 2:
- Operator: Stepford Connect
- Line: R001
- Travel time: 1.8 minutes
- Service type: Airport Connect

The fastest option is Line R001 at 1.8 minutes.
```

### Test 3: Operator Routes

**Ask:**
```
Show me all routes operated by Waterline
```

**Expected response:**
```
Waterline operates the following routes on the Stepford County Railway network:

Lines operated: R020, R021, R022, R023, R026, R027, R037, R038, ...

Total segments: 156

[Lists key routes and connections]

Would you like me to visualize the Waterline network map?
```

### Test 4: Network Visualization

**Ask:**
```
Yes, draw the Waterline network map
```

**Expected response:**
```
Here's the network map for Waterline services:

[Shows matplotlib plot with stations as red dots and connections as blue lines]

The map shows all stations served by Waterline and the direct connections between them.
```

### Test 5: Station Search

**Ask:**
```
Find stations with "Airport" in their name
```

**Expected response:**
```
I found 6 stations with "Airport" in their name:

- Airport Terminal 1
- Airport Terminal 2
- Airport Terminal 3
- Airport West
- Stepford Airport Central
- Stepford Airport Parkway

Would you like information about any of these stations?
```

---

## 🔍 How the GPT Uses Your Files

### When you ask a question...

1. **GPT reads the question**
   "Which operators serve Stepford Central?"

2. **GPT writes Python code automatically**
   ```python
   import rail_helpers
   graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
   ops = rail_helpers.operators_at_station(graph, "Stepford Central")
   print(ops)
   ```

3. **Code Interpreter runs the code**
   Loads `rail_routes.csv`, processes it with functions from `rail_helpers.py`

4. **Returns result**
   `['AirLink', 'Metro', 'Stepford Connect', 'Stepford Express']`

5. **GPT formats the answer**
   "At Stepford Central, the following operators run trains:..."

### File Access in Code Interpreter

Files in the Knowledge section are available as if they're in the current directory:

```python
# ✅ Correct way to access files
with open("rail_routes.csv", "r") as f:
    ...

import rail_helpers  # Works because rail_helpers.py is uploaded

import plot_helpers  # Works because plot_helpers.py is uploaded
```

The GPT doesn't need to know full paths or special syntax – just the filename.

---

## 🎨 Customization Options

### Change Response Style

Edit `custom_gpt_instructions.txt` and modify the **RESPONSE STYLE** section:

- Make it more formal: "You are a professional railway information specialist..."
- Make it casual: "You're a friendly train nerd who loves helping people..."
- Add humor: "Include a fun train fact with every response..."
- Regional flavor: "Speak with British railway terminology..."

Re-upload the instructions after editing.

### Add New Query Types

Want to answer "What's the busiest station?"

1. Add a function to `rail_helpers.py`:
   ```python
   def busiest_stations(graph, top_n=5):
       station_counts = [(s, len(edges)) for s, edges in graph.items()]
       station_counts.sort(key=lambda x: x[1], reverse=True)
       return station_counts[:top_n]
   ```

2. Update `custom_gpt_instructions.txt` to mention this function

3. Re-upload both files

### Change Visualization Style

Edit `plot_helpers.py` to:
- Change colors (e.g., use operator-specific colors)
- Add labels for travel times
- Use different marker sizes for major hubs
- Create interactive plots

### Update Network Data

When routes change:
1. Edit `rail_routes.csv` (or re-run `convert_to_edges.py` with updated JSON)
2. Re-upload to the GPT
3. No code changes needed – the GPT automatically uses the new data

---

## 📊 Understanding the Data Files

### rail_routes.csv

Format:
```csv
operator,line,from_station,to_station,travel_time_min,service_type,route_origin,route_destination
AirLink,R051,Stepford Central,Stepford Airport Central,8.0,Speed Link,Stepford Central,Stepford Airport Central
```

- **operator**: Company running the train (AirLink, Metro, etc.)
- **line**: Route ID (R001, R022, etc.)
- **from_station** / **to_station**: Direct connection
- **travel_time_min**: Time for this segment
- **service_type**: Express, Connect, Regional, etc.
- **route_origin** / **route_destination**: Full route endpoints

**Stats:**
- 658 edges (train segments)
- 71 unique stations
- 89 unique lines
- 5 operators

### station_coords.csv

Format:
```csv
station,x,y
Stepford Central,0.5,0.5
Airport Terminal 1,0.14,-0.47
```

Simple x/y coordinates for plotting. These are generated algorithmically for a reasonable layout.

You can replace these with real geographic coordinates if you have them (lat/long converted to x/y).

---

## 🛠️ Python Helper Functions Reference

### Core Functions

| Function | What It Does | Example |
|----------|-------------|---------|
| `load_rail_network(path)` | Load CSV into graph structure | `graph, ops, lines = load_rail_network("rail_routes.csv")` |
| `operators_at_station(graph, station)` | List operators serving a station | `operators_at_station(graph, "Benton")` |
| `lines_at_station(graph, station)` | List lines serving a station | `lines_at_station(graph, "Benton")` |
| `direct_services_between(graph, a, b)` | Find direct trains between stations | `direct_services_between(graph, "A", "B")` |
| `edges_for_operator(graph, operator)` | Get all segments for an operator | `edges_for_operator(graph, "AirLink")` |
| `edges_for_line(graph, line_id)` | Get all segments for a line | `edges_for_line(graph, "R001")` |
| `station_info(graph, station)` | Comprehensive station data | `station_info(graph, "Benton")` |
| `station_connections(graph, station)` | Direct connections from station | `station_connections(graph, "Benton")` |
| `search_stations(graph, query)` | Fuzzy search for stations | `search_stations(graph, "airport")` |
| `find_interchanges(graph, a, b)` | Stations connecting both A and B | `find_interchanges(graph, "A", "B")` |

### Plotting Functions

| Function | What It Does |
|----------|-------------|
| `load_station_coords(path)` | Load coordinates from CSV |
| `plot_operator_network(graph, operator, coords)` | Draw operator's network map |
| `plot_line_network(graph, line_id, coords)` | Draw single line map |
| `plot_full_network(graph, coords)` | Draw entire railway system |

---

## ⚠️ Important Notes & Limitations

### Code Interpreter Environment

- **Resets between conversations** – Each new chat loads fresh
- **Files persist** – Uploaded knowledge files stay available
- **No internet access** – Only local files
- **Standard libraries only** – Can't install packages (but has NumPy, Pandas, Matplotlib)
- **No state across messages** – Variables don't persist (but you can reload the graph in each Python block)

### Best Practices

1. **Always load the network at the start of Python code blocks:**
   ```python
   import rail_helpers
   graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
   ```

2. **Don't hardcode station names** – Use the data to find them

3. **Handle missing stations gracefully** – Use `search_stations()` for suggestions

4. **Only plot when asked** – Visualization is expensive, don't auto-generate

### Current Limitations

What this GPT **cannot** do (yet):
- Real-time train tracking (no live API)
- Multi-interchange route planning (only single-change suggestions)
- Ticket pricing (except what's in metadata)
- Schedule/timetable information
- Train composition or capacity
- Accessibility routing
- Alternative transport modes (bus, taxi, etc.)

These could be added with:
- External APIs (using Actions)
- More detailed CSV data
- Advanced pathfinding algorithms

---

## 🎓 Example Use Cases

### For Passengers
- "How do I get from A to B?"
- "Which operators serve my station?"
- "Is there a direct train to the airport?"

### For Railway Enthusiasts
- "Show me the entire Metro network"
- "What's the longest line?"
- "Which station has the most connections?"

### For Planners
- "Visualize operator coverage"
- "Find stations with only one operator"
- "Analyze network connectivity"

---

## 🐛 Troubleshooting

### "The GPT isn't running Python"

**Fix:**
1. Check that Code Interpreter is enabled in Capabilities
2. Verify files are uploaded to Knowledge section
3. Try explicitly asking: "Use Python to check which operators serve Benton"

### "It can't find the files"

**Fix:**
1. Re-upload all 4 files to Knowledge section
2. Make sure filenames match exactly:
   - `rail_routes.csv`
   - `rail_helpers.py`
   - `plot_helpers.py`
   - `station_coords.csv`

### "The routes seem wrong"

**Fix:**
1. Check `rail_routes.csv` – is the data correct?
2. Did you modify the CSV? Re-upload it
3. Test the helpers directly: Ask "Load the network and show me all operators"

### "Plots aren't showing"

**Fix:**
1. Make sure `plot_helpers.py` and `station_coords.csv` are uploaded
2. Check matplotlib is being imported correctly
3. Try: "Import plot_helpers and show me what functions are available"

### "It's hallucinating stations"

**Fix:**
1. Update the instructions to be more strict:
   ```
   NEVER invent stations. If a station doesn't exist in the data, say so explicitly.
   Always use rail_helpers.search_stations() to verify station names first.
   ```
2. Re-upload `custom_gpt_instructions.txt`

---

## 📈 Advanced Customizations

### Add Multi-Interchange Routing

Implement Dijkstra's algorithm in `rail_helpers.py`:

```python
def shortest_path(graph, start, end):
    # Implement pathfinding logic
    # Return: list of stations in path + total time
    ...
```

Update instructions to use this for complex journeys.

### Add Real-Time Data

Use GPT Actions to call an external API:
1. Create an API endpoint that returns live train data
2. Add Action in GPT config
3. Update instructions to check both static + live data

### Multi-Language Support

Add translations to instructions:
```
If the user asks in Spanish, respond in Spanish.
Station names remain in English.
```

### Add Historical Context

Upload a PDF about railway history to Knowledge:
- GPT can reference it for background information
- Useful for enthusiasts asking about line origins

---

## 🎉 You're Ready!

You now have a fully functional **train network assistant GPT** that:
- Uses real data from CSV
- Runs Python code to analyze routes
- Answers passenger questions accurately
- Visualizes network maps
- Never hallucinates stations or routes

### Next Steps

1. Test thoroughly with the example queries above
2. Customize the response style to match your preferences
3. Add your own helper functions for specific use cases
4. Share with friends or publish to the GPT store

---

## 📞 Reference Files

- **Instructions**: `custom_gpt_instructions.txt`
- **Data**: `rail_routes.csv`
- **Helpers**: `rail_helpers.py`, `plot_helpers.py`
- **Coordinates**: `station_coords.csv`

**Questions?** Check the Troubleshooting section above or test individual functions in Python to debug.

**Happy railway assisting! 🚂**
