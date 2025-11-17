# 🎯 Selective Context Loading - Smart Data Retrieval

## The Problem with Generic Loading

### Current Approach (Less Efficient):
```python
# User asks: "How do I get from Benton to Llyn?"
# AI loads EVERYTHING:
stations = load_all_stations()
benton = get_station_details("Benton")
info = extract_station_info(benton)  # All fields
history = get_station_history(benton)  # Not needed!
trivia = get_station_trivia(benton)  # Not needed!
platform_summary = get_platform_summary(benton)  # Good!
```

**Issue:** Loading unnecessary data (history, trivia) when user just wants route advice.

---

## ✅ Better Approach: Query-Specific Context

### Route Planning Query:
```python
# User asks: "How do I get from Benton to Llyn?"
# AI should ONLY load:
1. Route pathfinding data (always needed)
2. Operator for the route (to know which platforms)
3. Platform assignments for THAT OPERATOR at origin
4. Basic station info (platforms count, zone) - minimal
```

### History Query:
```python
# User asks: "When was Benton built?"
# AI should ONLY load:
1. Station history section
2. Skip platforms, routes, trivia (not relevant)
```

### Platform Query:
```python
# User asks: "Which platform for Stepford Connect at Benton?"
# AI should ONLY load:
1. Platform assignments
2. Filter for "Stepford Connect" only
3. Skip history, full station info
```

---

## 🔧 Implementation: Smart Context Functions

I'll create specialized functions that pull ONLY what's needed:

### 1. For Route Planning:
```python
def get_route_context(station_name, operator_name, stations_dict):
    """
    Get ONLY route-relevant context for a station.

    Returns:
    - Platform numbers for the specific operator
    - Zone
    - Total platform/track count (for context)
    - Accessibility (brief)

    SKIPS: History, trivia, full layout
    """
    station = get_station_details(station_name, stations_dict)

    # Minimal station info
    info = {
        'platforms': extract_field(station, 'platforms'),
        'zone': extract_field(station, 'zone'),
        'accessibility': extract_field(station, 'accessibility')
    }

    # Operator-specific platforms
    platform_summary = get_platform_summary(station)
    if operator_name in platform_summary:
        info['departure_platforms'] = platform_summary[operator_name]

    return info
```

### 2. For Station Information:
```python
def get_comprehensive_context(station_name, stations_dict):
    """
    Get FULL context for "tell me about X" queries.

    Returns everything:
    - Station info
    - Platform details
    - History
    - Trivia
    - All operators
    """
    station = get_station_details(station_name, stations_dict)
    return {
        'info': extract_station_info(station),
        'history': get_station_history(station),
        'trivia': get_station_trivia(station),
        'platforms': get_platform_summary(station)
    }
```

### 3. For Historical Queries:
```python
def get_history_context(station_name, stations_dict):
    """
    Get ONLY historical context.

    SKIPS: Platform details, current operators, trivia
    """
    station = get_station_details(station_name, stations_dict)
    return {
        'name': station['name'],
        'history': get_station_history(station),
        'url': station['url']  # For "read more"
    }
```

### 4. For Platform-Specific Queries:
```python
def get_platform_context(station_name, operator_filter=None, stations_dict=None):
    """
    Get ONLY platform assignments.

    Args:
        operator_filter: Optional - return platforms for specific operator only

    SKIPS: History, trivia, full station details
    """
    station = get_station_details(station_name, stations_dict)

    if operator_filter:
        # Return only platforms for this operator
        summary = get_platform_summary(station)
        return {
            'operator': operator_filter,
            'platforms': summary.get(operator_filter, 'Not available')
        }
    else:
        # Return all platform assignments
        return get_platform_summary(station)
```

---

## 📋 Query Type Detection

The AI should automatically detect what kind of query it is:

### Route Planning Keywords:
- "how do I get", "route from", "travel to", "get from...to"
- **→ Use:** `get_route_context()` with operator info

### Station Information Keywords:
- "tell me about", "information about", "what is"
- **→ Use:** `get_comprehensive_context()`

### Historical Keywords:
- "when was", "history of", "built", "opened", "changed"
- **→ Use:** `get_history_context()`

### Platform Keywords:
- "which platform", "what platform", "platform for"
- **→ Use:** `get_platform_context()` with operator filter

### Accessibility Keywords:
- "wheelchair", "step-free", "accessible", "lift", "elevator"
- **→ Use:** Extract ONLY accessibility field

---

## 🎯 Real Examples

### Example 1: Route Query
**User:** "How do I get from Benton to Llyn?"

**AI Workflow:**
```python
# 1. Find route
journey = shortest_path("Benton", "Llyn")
# Result: R078, Stepford Express, 16 min

# 2. Pull SELECTIVE context for route planning
origin_context = get_route_context(
    "Benton",
    operator_name="Stepford Express"  # From route result
)
# Returns:
# {
#   'platforms': '13',
#   'zone': 'Benton Zone',
#   'departure_platforms': 'Platforms 1, 3, 10'  # Only for Express
# }

# 3. NO LOADING of:
# - History ❌
# - Trivia ❌
# - Full platform details for other operators ❌
# - Detailed layouts ❌
```

**Response:**
```
Journey: Benton → Llyn-by-the-Sea

📍 Benton (13 platforms, Benton Zone)
   Stepford Express departs from Platforms 1, 3, or 10

🚄 Take R078 (16 minutes, direct)

📍 Llyn-by-the-Sea
```

---

### Example 2: Historical Query
**User:** "When was Benton station built?"

**AI Workflow:**
```python
# Pull ONLY history
context = get_history_context("Benton")
# Returns:
# {
#   'name': 'Benton',
#   'history': '2019: 1 February - Version 1.1.9 Benton added...',
#   'url': 'https://scr.fandom.com/wiki/Benton'
# }

# NO LOADING of:
# - Platform assignments ❌
# - Current operators ❌
# - Trivia ❌
# - Routes ❌
```

**Response:**
```
Benton Station History:

Opened: February 1, 2019 (Version 1.1.9)

Major Updates:
- V1.1.9 (2019): Station opened as major terminus
- V1.5 (2020): Platform expansion to 13 platforms
- V1.8 (2021): Added Metro services

Read more: https://scr.fandom.com/wiki/Benton
```

---

### Example 3: Platform-Specific Query
**User:** "Which platform for Metro at Benton?"

**AI Workflow:**
```python
# Pull ONLY platform info for Metro
context = get_platform_context(
    "Benton",
    operator_filter="Metro"
)
# Returns:
# {
#   'operator': 'Metro',
#   'platforms': 'Platform 10'
# }

# NO LOADING of:
# - History ❌
# - Trivia ❌
# - Full station info ❌
# - Other operators' platforms ❌
```

**Response:**
```
Metro at Benton uses Platform 10.

Service: Metro to Stepford Victoria (COX route)

Platform 10 is on the upper level of the station.
```

---

## 🚀 Efficiency Gains

### Before (Generic Loading):
```
User: "Which platform for Metro at Benton?"

Loading:
- Full station details (5 KB)
- All platform assignments (2 KB)
- History section (3 KB)
- Trivia section (2 KB)
- All operators' info (4 KB)
Total: ~16 KB loaded

Processing time: ~200ms
```

### After (Selective Loading):
```
User: "Which platform for Metro at Benton?"

Loading:
- Platform assignments (2 KB)
- Filter for Metro only
Total: ~0.5 KB loaded (after filtering)

Processing time: ~50ms
```

**75% reduction in data loaded!** ⚡

---

## 📊 Query-to-Context Mapping Table

| Query Type | Load | Skip |
|------------|------|------|
| **Route Planning** | Platform for operator, zone, basic info | History, trivia, other operators |
| **"Tell me about"** | Everything | Nothing (comprehensive) |
| **Historical** | History section only | Platforms, current routes, trivia |
| **Platform Query** | Platform assignments (filtered) | History, trivia, full info |
| **Accessibility** | Accessibility field only | Everything else |
| **Zone Query** | Zone field only | Everything else |
| **Trivia Query** | Trivia section only | History, platforms, routes |

---

## 🎨 Updated AI Instructions

Add this to the GPT instructions:

```
## SELECTIVE CONTEXT LOADING

Always identify the query type FIRST, then load ONLY relevant data:

1. Route Planning Queries ("How do I get from A to B?")
   - Load: Route path, operator, platforms for THAT operator
   - Skip: History, trivia, unrelated operators

2. Station Info Queries ("Tell me about station X")
   - Load: Everything (comprehensive response)

3. Historical Queries ("When was X built?")
   - Load: History section only
   - Skip: Current platforms, routes, trivia

4. Platform Queries ("Which platform for operator Y at X?")
   - Load: Platform assignments for THAT operator only
   - Skip: History, trivia, other operators

5. Specific Field Queries ("What zone is X in?")
   - Load: That field only
   - Skip: Everything else

Example Code:
```python
# Detect query type
if "how do i get" in user_query.lower():
    # Route planning - selective loading
    operator = extract_operator_from_route(journey)
    context = get_route_context(station, operator)
elif "which platform" in user_query.lower():
    # Platform query - operator-filtered loading
    operator = extract_operator_from_query(user_query)
    context = get_platform_context(station, operator_filter=operator)
elif "when was" in user_query.lower() or "history" in user_query.lower():
    # History query - history only
    context = get_history_context(station)
```

This makes responses:
- ✅ Faster (less data loaded)
- ✅ More focused (only relevant info)
- ✅ More professional (not overwhelming with unrelated details)
```

---

## ✅ Summary

### Your Insight:
"Let AI pull relevant details for each inquiry, like pathfinding with platforms, rather than generalized collecting"

### Implementation:
1. **Detect query intent** (route, history, platform, etc.)
2. **Load ONLY relevant data** for that intent
3. **Skip unnecessary sections** (history when doing routes, etc.)
4. **Filter to specific operators** when applicable

### Benefits:
- ⚡ Faster responses (less data to process)
- 🎯 More focused answers (no irrelevant info)
- 💡 Smarter AI (context-aware data loading)
- 📉 Lower token usage (efficiency)

---

**This makes your AI work like a smart assistant who knows exactly what information is needed for each question!** 🧠
