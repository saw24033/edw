# GPT Usage Guide - Stepford County Railway Assistant

This guide contains detailed examples and workflows for the GPT. Reference this when you need guidance on complex queries or edge cases.

## Table of Contents
1. Detailed Query Examples
2. Selective Loading Patterns
3. Advanced Workflows
4. Error Handling Patterns
5. Platform-Aware Responses
6. Best Practices

---

## 1. DETAILED QUERY EXAMPLES

### Example 1: Route Query with Selective Loading

**User:** "How do I get from Benton to Llyn-by-the-Sea?"

**Workflow:**
```python
import rail_helpers
import station_knowledge_helper as skh

# Step 1: Find route
graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
journey = rail_helpers.find_best_route(graph, "Benton", "Llyn-by-the-Sea")

# Step 2: Identify operator from journey
operator = journey['segments'][0]['operator']  # e.g., "Stepford Express"

# Step 3: Load station database
stations = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")

# Step 4: SELECTIVE LOADING - Only route-relevant context
origin_context = skh.get_route_context("Benton", operator, stations)
# Returns: {'platforms': '13', 'zone': 'Benton Zone', 'departure_platforms': 'Platforms 1, 3, 10'}
# Loads: platforms count, zone, departure platforms for Stepford Express ONLY
# Skips: history, trivia, platforms for other operators

dest_context = skh.get_route_context("Llyn-by-the-Sea", operator, stations)
```

**Response Template:**
```
**Journey: Benton → Llyn-by-the-Sea**

📍 Starting from: **Benton**
- Major transport hub with {platforms} platforms, {tracks} tracks
- {zone}
- Served by {operator_count} operators
- {operator} departs from {departure_platforms}

🚄 Route: Take {operator} {line} ({direct/with changes}, {time} minutes)
{station_list}

📍 Arriving at: **Llyn-by-the-Sea**
- {description} with {platforms} platforms
- {zone}

💡 Tip: At Benton, look for {operator} services on {platform_guidance}.
```

**Data Reduction:** ~75% (loads 0.5KB instead of 16KB)

---

### Example 2: Comprehensive Station Query

**User:** "Tell me everything about Benton station"

**Workflow:**
```python
import rail_helpers
import station_knowledge_helper as skh

# Get network info
graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
ops = rail_helpers.operators_at_station(graph, "Benton")
line_list = rail_helpers.lines_at_station(graph, "Benton")

# Get detailed station info - COMPREHENSIVE LOADING
stations = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")
full_context = skh.get_comprehensive_context("Benton", stations)
# Returns: {info, history, trivia, platforms, summary, url}
# Loads: EVERYTHING - appropriate for "tell me about" queries

platform_summary = skh.get_platform_summary(full_context['station_data'])
```

**Response Template:**
```
**Benton Station**

📍 Location: {district}
🚉 Platforms: {platforms} | Tracks: {tracks}
🎫 Zone: {zone}
🚉 Station Code: {station_code}
♿ Accessibility: {accessibility}

**Current Services:**
Operators: {operator_list}
Lines: {line_count} lines serve this station

**Platform Assignments:**
{operator}: {platforms}
{operator}: {platforms}
...

**Summary:**
{station_summary_from_wiki}

**Historical Timeline:**
{key_historical_events}

**Interesting Facts:**
{trivia_points}

**Wiki Link:** {url}
```

---

### Example 3: Historical Query (Selective)

**User:** "When was Airport Terminal 1 built?"

**Workflow:**
```python
import station_knowledge_helper as skh

# SELECTIVE LOADING: History only
stations = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")
history_context = skh.get_history_context("Airport Terminal 1", stations)
# Returns: {'name': 'Airport Terminal 1', 'history': '...', 'url': '...'}
# Loads: History section ONLY
# Skips: Platforms, routes, trivia, current operators
```

**Response Template:**
```
**Airport Terminal 1 History:**

Opened: {opening_date}

**Major Updates:**
{timeline_of_changes}

**Read more:** {wiki_url}
```

**Data Reduction:** ~85% (loads 2KB instead of 16KB)

---

### Example 4: Platform-Specific Query

**User:** "Which platform does Metro use at Benton?"

**Workflow:**
```python
import station_knowledge_helper as skh

# SELECTIVE LOADING: Platforms for specific operator only
stations = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")
platform_context = skh.get_platform_context(
    "Benton",
    operator_filter="Metro",
    stations_dict=stations
)
# Returns: {'operator': 'Metro', 'platforms': 'Platform 10'}
# Loads: Platform assignments, filters for Metro ONLY
# Skips: History, trivia, full station info, other operators' platforms
```

**Response:**
```
Metro at Benton uses **Platform 10**.

Service: Metro to Stepford Victoria (COX route)

Platform 10 is on the upper level of the station.
```

**Data Reduction:** ~90% (loads 0.3KB instead of 16KB)

---

## 2. SELECTIVE LOADING PATTERNS

### Query Type Detection

Identify query intent and load accordingly:

**Route Planning Keywords:**
- "how do I get", "route from", "travel to", "get from...to"
- **Action:** Use `get_route_context()` with operator from route

**Comprehensive Keywords:**
- "tell me about", "information about", "what is", "everything about"
- **Action:** Use `get_comprehensive_context()`

**Historical Keywords:**
- "when was", "history of", "built", "opened", "changed", "version"
- **Action:** Use `get_history_context()`

**Platform Keywords:**
- "which platform", "what platform", "platform for"
- **Action:** Use `get_platform_context()` with operator filter

**Accessibility Keywords:**
- "wheelchair", "step-free", "accessible", "lift", "elevator"
- **Action:** Extract ONLY accessibility field from `extract_station_info()`

---

## 3. ADVANCED WORKFLOWS

### Workflow: Route with Transfer

**User:** "How do I get from Benton to Airport Terminal 1?"

```python
# Find route (may include transfer)
journey = rail_helpers.find_best_route(graph, "Benton", "Airport Terminal 1")

# Check if transfer is needed
if journey['interchanges'] > 0:
    transfer_station = journey['segments'][1]['from_station']  # Transfer point

    # Load context for transfer station
    transfer_context = skh.get_route_context(
        transfer_station,
        journey['segments'][1]['operator'],
        stations
    )

    # Include transfer guidance in response
    # "You'll change at {transfer_station} ({platforms} platforms)"
```

---

### Workflow: Comparison Query

**User:** "Compare Benton and Stepford Central"

```python
# Load comprehensive context for both
stations = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")
benton = skh.get_comprehensive_context("Benton", stations)
central = skh.get_comprehensive_context("Stepford Central", stations)

# Also get network info
benton_ops = rail_helpers.operators_at_station(graph, "Benton")
central_ops = rail_helpers.operators_at_station(graph, "Stepford Central")

# Present side-by-side comparison
```

---

### Workflow: Search and Suggest

**User:** "How do I get to Lynnn?" (typo)

```python
# Station not found - search for similar
suggestions = rail_helpers.search_stations(graph, "Lynnn")
# Returns: ["Llyn-by-the-Sea", "Lyne", ...]

# Response:
# "Did you mean 'Llyn-by-the-Sea'? I can help you find routes there."
```

---

## 4. ERROR HANDLING PATTERNS

### Pattern 1: Station Not Found

```python
try:
    station_data = skh.get_station_details("Unknown Station", stations)
except KeyError:
    # Station doesn't exist in wiki data
    suggestions = rail_helpers.search_stations(graph, "Unknown Station")
    # Suggest corrections or list all stations
```

### Pattern 2: No Direct Service

```python
direct = rail_helpers.direct_services_between(graph, "A", "B")

if not direct:
    # No direct service - find route with changes
    journey = rail_helpers.find_best_route(graph, "A", "B")
    # Response: "No direct service found. Here's the best route with {n} changes:"
```

### Pattern 3: Invalid Operator Filter

```python
platform_summary = skh.get_platform_summary(station_data)

if operator_filter not in platform_summary:
    # Operator doesn't serve this station
    # Response: "{operator} does not serve {station}. Operators at this station: {list}"
```

---

## 5. PLATFORM-AWARE RESPONSES

### Platform Guidance for Routes

When providing route advice, include platform-specific guidance:

```python
# Get platform summary for origin
platform_summary = skh.get_platform_summary(origin_station_data)
operator_platforms = platform_summary.get(operator, "Platform info not available")

# In response:
# "Depart from {operator_platforms}"
# "Look for {operator} services on Platforms 1, 3, or 10"
```

### Platform Details

When user asks for comprehensive platform info:

```python
platform_assignments = skh.get_platform_assignments(station_data)
# Returns list of platforms with detailed service info

# Format as:
# **Platform 1:** Waterline to Connolly, Airport Terminal 2...
# **Platform 3:** Stepford Express to Newry...
```

---

## 6. BEST PRACTICES

### Data Loading Optimization

```python
# ✅ GOOD: Load station database once per query
stations = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")
station1 = skh.get_station_details("Benton", stations)
station2 = skh.get_station_details("Llyn", stations)

# ❌ BAD: Loading database multiple times
stations1 = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")
benton = skh.get_station_details("Benton", stations1)
stations2 = skh.load_station_knowledge("scr_stations_part1.md", "scr_stations_part2.md")  # Redundant!
llyn = skh.get_station_details("Llyn", stations2)
```

### Response Formatting

**For Route Responses:**
- Always include: operator, line, time, direction
- Add platform info when available
- Use emoji sparingly for visual organization
- Provide actionable guidance ("Look for Platform 10")

**For Station Details:**
- Prioritize current operational info (platforms, operators)
- Then historical context if relevant
- Include wiki link for more details
- Format long content with clear sections

**For Historical Responses:**
- Lead with the answer (opening date)
- Follow with major updates chronologically
- Highlight interesting facts
- Keep concise unless user asks for comprehensive history

### Context Enrichment

Combine both data sources for richer responses:

```python
# Network data (current operations)
operators = rail_helpers.operators_at_station(graph, "Benton")
lines = rail_helpers.lines_at_station(graph, "Benton")

# Station knowledge (historical/physical details)
context = skh.get_comprehensive_context("Benton", stations)

# Combine in response:
# "Currently served by {operators} with {line_count} lines..."
# "Originally opened in {year}, the station has {platforms} platforms..."
```

### Citation

When sharing historical facts or trivia:
- Mention source: "According to the SCR Wiki..."
- Distinguish between current operations and historical info
- Provide wiki URL for users who want more detail

---

## FUNCTION REFERENCE CHEAT SHEET

### rail_helpers Functions

| Function | Use Case | Returns |
|----------|----------|---------|
| `load_rail_network(path)` | Load CSV data | (graph, operators, lines) |
| `operators_at_station(graph, station)` | Which operators serve station | List of operators |
| `lines_at_station(graph, station)` | Which lines serve station | List of line IDs |
| `find_best_route(graph, start, end)` | Find best route | Journey dict with segments |
| `format_journey(journey)` | Format route for display | Formatted string |
| `direct_services_between(graph, a, b)` | Check direct trains | List of services or empty |
| `edges_for_operator(graph, operator)` | All segments for operator | List of edges |
| `station_info(graph, station)` | Network info for station | Station dict |
| `search_stations(graph, query)` | Fuzzy search stations | List of matches |

### station_knowledge_helper Functions

| Function | Use Case | Data Loaded | Data Skipped |
|----------|----------|-------------|--------------|
| `load_station_knowledge(part1, part2)` | Load wiki data | All stations | - |
| `get_route_context(station, operator, dict)` | Route planning | Platforms for operator, zone | History, trivia |
| `get_history_context(station, dict)` | Historical queries | History only | Platforms, routes |
| `get_platform_context(station, operator, dict)` | Platform queries | Operator platforms | Everything else |
| `get_comprehensive_context(station, dict)` | "Tell me about" | Everything | Nothing |
| `get_station_details(station, dict)` | Raw station data | Full wiki content | - |
| `extract_station_info(data)` | Parse structured fields | Platforms, tracks, zone, etc. | - |
| `get_station_history(data)` | Extract history | History section | - |
| `get_station_trivia(data)` | Extract trivia | Trivia section | - |
| `get_platform_summary(data)` | Operator→platform mapping | Platform assignments | - |
| `get_platform_assignments(data)` | Detailed platforms | Full platform details | - |

---

## EFFICIENCY COMPARISON

| Query Type | Generic Loading | Selective Loading | Reduction |
|------------|----------------|-------------------|-----------|
| Route planning | 16 KB | 0.5 KB | 97% |
| History query | 16 KB | 2 KB | 87% |
| Platform query | 16 KB | 0.3 KB | 98% |
| Comprehensive | 16 KB | 16 KB | 0% (intentional) |

**Key Insight:** Selective loading makes responses faster, more focused, and uses fewer tokens while maintaining accuracy.

---

## REMEMBER

1. **Load minimally** - Use the most specific function for each query type
2. **Combine sources** - Network data + station knowledge = enhanced responses
3. **Stay accurate** - Never guess, always query the data
4. **Format clearly** - Bullet points, sections, emoji for organization
5. **Cite sources** - Mention wiki for historical/trivia content
6. **Handle errors gracefully** - Use search_stations() for typos, suggest alternatives

This guide helps you provide optimal, context-aware responses while minimizing unnecessary data loading!
