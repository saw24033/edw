"""
Station Knowledge Helper - Parse scr_stations_part1.md and scr_stations_part2.md for detailed station info

Version 3.4.1 - INTEGRATION FIXES FOR CUSTOM GPT
- Fixed get_route_context() to pass csv_path parameter for terminal detection
- Added fuzzy station name matching in get_station_details() for "(Station)" suffix
- Updated CSV path handling to work in both local and Custom GPT (/mnt/data/) environments
- Example: get_route_context("Benton Bridge", ..., "R045", "Benton") now returns "Platform 3 (toward Stepford Victoria)"

Version 3.4 - TERMINAL DETECTION FOR INTERMEDIATE STOPS
- Added intelligent terminal detection for intermediate station lookups
- Parser now determines direction and finds terminal to query platform data
- Solves "intermediate station problem" where next_station isn't a terminus
- Example: R045 at Benton Bridge → Benton now correctly returns Platform 3 (toward Stepford Victoria)

Version 3.3 - IMPROVED PLATFORM PARSING
- Enhanced Services table parsing for directional platforms
- Better wiki table format handling
- More accurate route-to-platform mapping
"""

import re

def load_station_knowledge(filepath1="scr_stations_part1.md", filepath2="scr_stations_part2.md"):
    """
    Load and parse the station content markdown files (split into 2 parts).
    Returns a dictionary mapping station names to their full content.
    """
    stations = {}

    # Load both parts
    for filepath in [filepath1, filepath2]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split by station headers (## Station N: Name)
            pattern = r'## Station \d+: (.+?)\n\n\*\*Page ID:\*\* (\d+)\n\*\*URL:\*\* (.+?)\n\n\*\*Summary:\*\*\n(.+?)\n\n\*\*Full Content:\*\*\n\n(.+?)\n\n={80}'

            matches = re.findall(pattern, content, re.DOTALL)

            for match in matches:
                station_name = match[0].strip()
                page_id = match[1]
                url = match[2]
                summary = match[3].strip()
                full_content = match[4].strip()

                stations[station_name] = {
                    'name': station_name,
                    'page_id': page_id,
                    'url': url,
                    'summary': summary,
                    'full_content': full_content
                }
        except FileNotFoundError:
            print(f"Warning: {filepath} not found")
            continue

    return stations


def get_station_details(station_name, stations_dict):
    """
    Get detailed information for a specific station.

    Args:
        station_name: Name of the station
        stations_dict: Dictionary returned by load_station_knowledge()

    Returns:
        Dictionary with station details, or None if not found
    """
    # Exact match
    if station_name in stations_dict:
        return stations_dict[station_name]

    # Case-insensitive search
    for name, data in stations_dict.items():
        if name.lower() == station_name.lower():
            return data

    # Fuzzy match: Try adding/removing "(Station)" suffix (v3.4)
    # Handles "Benton Bridge" <-> "Benton Bridge (Station)"
    def normalize_name(name):
        return name.replace(' (Station)', '').strip()

    query_normalized = normalize_name(station_name).lower()

    for name, data in stations_dict.items():
        name_normalized = normalize_name(name).lower()
        if name_normalized == query_normalized:
            return data

    return None


def search_station_content(query, stations_dict):
    """
    Search for query string in all station content.

    Args:
        query: Search term
        stations_dict: Dictionary returned by load_station_knowledge()

    Returns:
        List of (station_name, matches) tuples
    """
    query_lower = query.lower()
    results = []

    for station_name, data in stations_dict.items():
        content_lower = data['full_content'].lower()
        if query_lower in content_lower:
            # Count occurrences
            count = content_lower.count(query_lower)
            results.append((station_name, count))

    # Sort by number of matches
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def extract_station_info(station_data):
    """
    Extract structured information from station content.

    Returns a dictionary with parsed fields like:
    - platforms, tracks, zone, location, accessibility, etc.
    """
    content = station_data['full_content']
    info = {
        'name': station_data['name'],
        'summary': station_data['summary'],
        'url': station_data['url']
    }

    # Extract common fields using improved regex patterns

    # Special handling for platforms - find ALL matches and take the largest number
    # This avoids matching "Platform 0" instead of "Platforms 12" at stations with Platform 0
    platform_matches = re.findall(r'Platforms\s+(\d+)', content, re.IGNORECASE)
    if platform_matches:
        # Take the largest number (total platform count)
        info['platforms'] = max(platform_matches, key=int)

    # Handle other fields with simple patterns
    patterns = {
        # Match "Tracks 14" or "14 tracks"
        'tracks': r'Tracks\s+(\d+)',
        # Match zone info - be more specific to avoid matching "Zone X" in random text
        'zone': r'Zone[:\s]+([A-Z\-\s]+?)(?:\s+Platforms?|\s+Station|\s+Accessibility|Ticket|$)',
        'location': r'Location[:\s]+([^\n]+?)(?:\s+Zone|District|$)',
        'station_code': r'Station code[:\s]+([A-Z]{2,4})',
        'operator': r'(?:Served by|Operated by|Managed by)[:\s]+([^\n]+?)(?:Station Information|Operational|$)',
        'accessibility': r'Accessibility[:\s]+([^\n]+?)(?:Ticket|Service|$)',
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            extracted = match.group(1).strip()
            # Clean up common artifacts
            extracted = re.sub(r'\s+', ' ', extracted)  # Normalize whitespace
            extracted = extracted.split('Ticket machines')[0].strip()  # Remove trailing info
            info[field] = extracted

    return info


def get_station_history(station_data):
    """
    Extract history section from station content.
    """
    content = station_data['full_content']

    # Look for History section
    history_match = re.search(r'History\s*\[\s*\]\s*(.+?)(?:Trivia|Gallery|Notes|$)',
                             content, re.DOTALL | re.IGNORECASE)

    if history_match:
        return history_match.group(1).strip()

    return None


def get_station_trivia(station_data):
    """
    Extract trivia section from station content.
    """
    content = station_data['full_content']

    # Look for Trivia section
    trivia_match = re.search(r'Trivia\s*\[\s*\]\s*(.+?)(?:Gallery|Notes|References|Stations|$)',
                            content, re.DOTALL | re.IGNORECASE)

    if trivia_match:
        return trivia_match.group(1).strip()

    return None


def list_all_stations(stations_dict):
    """
    Return sorted list of all station names.
    """
    return sorted(stations_dict.keys())


def find_stations_by_operator(operator, stations_dict):
    """
    Find all stations mentioning a specific operator.
    """
    results = []
    operator_lower = operator.lower()

    for station_name, data in stations_dict.items():
        content_lower = data['full_content'].lower()
        if operator_lower in content_lower:
            results.append(station_name)

    return sorted(results)


def get_platform_assignments(station_data):
    """
    Extract platform-by-platform assignments from station content.

    Returns a list of dictionaries with platform numbers and their services.
    Example: [
        {'platform': '1', 'services': 'Waterline to Connolly, Airport Terminal 2...'},
        {'platform': '2', 'services': 'Stepford Connect to...'},
    ]
    """
    content = station_data['full_content']
    platforms = []

    # Look for platform assignments in the station layout section
    # Pattern: "Platform X → Service details" or "Platform X ← Service details"
    platform_pattern = r'Platform (\d+(?:-\d+)?)\s*[→←]\s*([^\n]+?)(?=Platform \d+|Terminating|⊢|Lift|Stairs|$)'

    matches = re.findall(platform_pattern, content, re.DOTALL)

    for plat_num, services in matches:
        # Clean up the services text
        services_clean = services.strip()
        # Remove excessive whitespace
        services_clean = re.sub(r'\s+', ' ', services_clean)

        if services_clean and len(services_clean) > 10:  # Skip empty or very short entries
            platforms.append({
                'platform': plat_num,
                'services': services_clean[:200]  # Limit length
            })

    return platforms


def get_platform_summary(station_data):
    """
    Get a human-readable summary of which operators use which platforms.

    Returns a dictionary mapping operators to their platform ranges.
    Example: {
        'Waterline': 'Platforms 1-3',
        'Stepford Connect': 'Platforms 4, 10-13',
        'Stepford Express': 'Platforms 1, 3, 10'
    }
    """
    content = station_data['full_content']
    operator_platforms = {}

    # Strategy 1: Look for explicit platform range statements in History section
    # Format: "Platform 1-3 are for Waterline" or "Platform 7-10 are for Stepford Express"
    history_pattern = r'Platform[s]?\s+([\d\-,\s&]+)\s+(?:are|is)\s+for\s+(Waterline|Stepford Connect|Stepford Express|Metro|AirLink)'
    history_matches = re.findall(history_pattern, content, re.IGNORECASE)

    for plats, op in history_matches:
        # Clean up the platform list
        plats_clean = plats.strip().replace(' & ', ', ')
        if op not in operator_platforms:
            operator_platforms[op] = f"Platforms {plats_clean}"

    # Strategy 2: Parse Services table for route-platform mappings
    if not operator_platforms:
        route_platform_map = build_route_platform_map(station_data)

        # Group routes by operator and collect their platforms
        operator_route_platforms = {}

        for route_code, platforms in route_platform_map.items():
            # Determine operator from route number
            route_num = int(route_code[1:])  # Remove 'R' prefix
            operator = _guess_operator_from_route(route_num, content)

            if operator:
                if operator not in operator_route_platforms:
                    operator_route_platforms[operator] = set()
                # Add all platforms for this route
                operator_route_platforms[operator].update(platforms)

        # Convert to readable format
        for operator, platform_set in operator_route_platforms.items():
            platforms_sorted = sorted(platform_set, key=lambda x: int(x.split('-')[0]))
            operator_platforms[operator] = f"Platforms {', '.join(platforms_sorted)}"

    # Strategy 3: Parse individual platform listings in station layout
    if not operator_platforms:
        platforms = get_platform_assignments(station_data)
        temp_platforms = {}

        # Group platforms by operator
        for plat_info in platforms:
            services = plat_info['services']
            plat_num = plat_info['platform']

            # Find operators mentioned
            operators = ['Waterline', 'Stepford Connect', 'Stepford Express', 'Metro', 'AirLink']
            for op in operators:
                if op in services:
                    if op not in temp_platforms:
                        temp_platforms[op] = []
                    temp_platforms[op].append(plat_num)

        # Convert to readable format
        for op, plats in temp_platforms.items():
            # Remove duplicates and sort
            unique_plats = sorted(set(plats), key=lambda x: int(x.split('-')[0]))
            operator_platforms[op] = f"Platform{'s' if len(unique_plats) > 1 else ''} {', '.join(unique_plats)}"

    return operator_platforms


def _guess_operator_from_route(route_num, content):
    """Helper function to guess operator from route number and content."""
    if 75 <= route_num <= 99:
        return 'Stepford Express'
    elif 50 <= route_num <= 60:
        return 'AirLink'
    elif 100 <= route_num <= 199:
        # Check content for operator mentions
        for op in ['Stepford Connect', 'Metro', 'Stepford Express']:
            if op in content[:3000]:
                return op
        return 'Stepford Connect'  # Default for R100+
    else:
        # R001-R049: Check content
        for op in ['Waterline', 'Metro', 'Stepford Connect']:
            if op in content[:3000]:
                return op
        return 'Stepford Connect'  # Default


def build_route_platform_map(station_data):
    """
    Build a mapping of route codes to their specific platforms at a station.

    Returns a dictionary: {'R001': ['1', '4'], 'R003': ['2', '3'], ...}

    IMPROVED: Better wiki table parsing for Services section
    """
    content = station_data['full_content']
    route_platform_map = {}

    # Parse Services section - IMPROVED TABLE PARSING
    services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)',
                                content, re.DOTALL | re.IGNORECASE)
    if not services_section:
        return route_platform_map

    services_text = services_section.group(1)

    # Parse table - handle both single-line and multi-line formats
    # Split by platform numbers to segment the table
    platform_segments = re.split(r'\s+(\d+(?:-\d+)?)\s+', services_text)

    # After split: [before_first_platform, platform1, content1, platform2, content2, ...]
    for i in range(1, len(platform_segments), 2):
        if i + 1 < len(platform_segments):
            platform_num = platform_segments[i]
            content = platform_segments[i + 1]

            # Skip table headers
            if 'Platform' in content or 'Previous' in content:
                continue

            # Extract all route codes from this platform's content
            routes = re.findall(r'R\d+', content)
            for route in routes:
                if route not in route_platform_map:
                    route_platform_map[route] = []
                if platform_num not in route_platform_map[route]:
                    route_platform_map[route].append(platform_num)

    return route_platform_map


def build_directional_platform_map(station_data):
    """
    Build a mapping of (route, destination) to platforms for directional accuracy.

    Returns a dictionary: {('R083', 'Llyn-by-the-Sea'): ['1-2'], ('R083', 'Newry'): ['2-3'], ...}

    IMPROVED v3.3: Handles wiki table format where multiple routes share one destination
    Example: "R010 R013 to Greenslade" → both R010 and R013 map to Greenslade
    """
    content = station_data['full_content']
    directional_map = {}

    # Parse Services section
    services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)',
                                content, re.DOTALL | re.IGNORECASE)
    if not services_section:
        return directional_map

    services_text = services_section.group(1)

    # Parse table rows
    # Format: "Platform(s) Previous station Route Next station"
    # NOTE: Wiki tables may be on ONE line or multiple lines

    # Strategy: Find all occurrences of platform numbers followed by route patterns
    # Pattern: "1 Station R### ... 2-3 Station R###" etc.
    # Split by platform number patterns to segment the line

    # Split services_text into segments by platform numbers
    # Pattern to split: digit(s) or digit-digit at start of segment (after whitespace)
    platform_segments = re.split(r'\s+(\d+(?:-\d+)?)\s+', services_text)

    # After split: [before_first_platform, platform1, content1, platform2, content2, ...]
    # Process pairs: (platform_num, content)
    for i in range(1, len(platform_segments), 2):
        if i + 1 < len(platform_segments):
            platform_num = platform_segments[i]
            content = platform_segments[i + 1]

            # Skip table headers
            if 'Platform' in content or 'Previous' in content or 'Route' in content or 'Next station' in content:
                continue

            # Extract route->destination pairs from this platform's content
            _extract_route_destinations(content, platform_num, directional_map)

    return directional_map


def _extract_route_destinations(line, platform, directional_map):
    """
    Helper to extract (route, destination) pairs from a Services table line.

    Handles formats like:
    - "R010 R013 to Greenslade Morganstown Docks" → (R010, Greenslade), (R013, Greenslade)
    - "R013 R015 to Benton" → (R013, Benton), (R015, Benton)
    - "R002 to Stepford Central Terminus" → (R002, Stepford Central)
    """
    # Find patterns: "R### R### ... to Destination"
    # Pattern captures: (route codes) + "to" + (destination text)
    pattern = r'((?:R\d+\s+)+)to\s+([A-Z][\w\s\-]+?)(?=\s+R\d+|\s+Terminus|\s+\(|$)'

    matches = re.finditer(pattern, line)

    for match in matches:
        routes_text = match.group(1).strip()
        destination = match.group(2).strip()

        # Extract all route codes from the routes_text
        routes = re.findall(r'R\d+', routes_text)

        # Clean destination: Remove extra words from "Next station" column
        # Intelligently extract station name (most are 1-2 words, some are 3)
        dest_words = destination.split()

        # If first word is a common multi-word station prefix, take 2-3 words
        if dest_words and dest_words[0] in ['St', 'Airport', 'Upper', 'West', 'East', 'New', 'Port', 'Stepford']:
            if len(dest_words) > 3:
                destination_clean = ' '.join(dest_words[:3])
            else:
                destination_clean = destination
        # Otherwise, take first word only (safest to avoid capturing next station column)
        elif dest_words:
            destination_clean = dest_words[0]
        else:
            continue  # Skip if no words

        if len(destination_clean) < 2:  # Skip very short destinations
            continue

        # Map all routes to this destination
        for route in routes:
            key = (route, destination_clean)
            if key not in directional_map:
                directional_map[key] = []
            if platform not in directional_map[key]:
                directional_map[key].append(platform)


def _load_route_terminals(csv_path="rail_routes.csv"):
    """
    Load route terminal information from rail_routes.csv.
    Returns dict: {route_code: {'origin': station, 'destination': station, 'stops': [ordered list]}}
    """
    import csv
    import os

    routes = {}

    # Try multiple possible paths for the CSV
    possible_paths = [
        csv_path,
        f"/mnt/data/{csv_path}",
        os.path.join(os.path.dirname(__file__), csv_path)
    ]

    csv_content = None
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                csv_content = f.read()
            break
        except:
            continue

    if not csv_content:
        return routes

    # Parse CSV
    reader = csv.DictReader(csv_content.strip().split('\n'))
    for row in reader:
        route_code = row['line']
        origin = row['route_origin']
        destination = row['route_destination']
        from_station = row['from_station']
        to_station = row['to_station']

        if route_code not in routes:
            routes[route_code] = {
                'origin': origin,
                'destination': destination,
                'stops': []
            }

        # Build ordered stop list
        if from_station not in routes[route_code]['stops']:
            routes[route_code]['stops'].append(from_station)
        if to_station not in routes[route_code]['stops']:
            routes[route_code]['stops'].append(to_station)

    return routes


def _get_terminal_for_direction(route_code, current_station, next_station, csv_path="rail_routes.csv"):
    """
    Determine which terminal station (origin or destination) the train is heading toward.

    Args:
        route_code: Route code (e.g., "R045")
        current_station: Current station name (e.g., "Benton Bridge" or "Benton Bridge (Station)")
        next_station: Next station name (e.g., "Benton")
        csv_path: Path to rail_routes.csv

    Returns:
        Terminal station name (e.g., "Stepford Victoria") or None
    """
    routes = _load_route_terminals(csv_path)

    if route_code not in routes:
        return None

    route_info = routes[route_code]
    stops = route_info['stops']
    origin = route_info['origin']
    destination = route_info['destination']

    # Helper function to normalize station names (strip "(Station)" suffix)
    def normalize_name(name):
        return name.replace(' (Station)', '').strip()

    # Normalize station names for comparison
    current_normalized = normalize_name(current_station).lower()
    next_normalized = normalize_name(next_station).lower()

    # Find positions in stop list
    current_idx = None
    next_idx = None

    for i, stop in enumerate(stops):
        stop_normalized = normalize_name(stop).lower()

        if current_idx is None and stop_normalized == current_normalized:
            current_idx = i

        if next_idx is None and stop_normalized == next_normalized:
            next_idx = i

        # Early exit if both found
        if current_idx is not None and next_idx is not None:
            break

    # If exact matches fail, return None
    if current_idx is None or next_idx is None:
        return None

    # Determine direction
    if next_idx < current_idx:
        # Going backward toward origin
        return origin
    elif next_idx > current_idx:
        # Going forward toward destination
        return destination
    else:
        # Same station (shouldn't happen)
        return None


def get_route_platform(station_data, route_code, next_station=None, csv_path="rail_routes.csv"):
    """
    Get the specific platform(s) for a route at this station.

    Args:
        station_data: Station data dict from get_station_details()
        route_code: Route code (e.g., "R001", "R078")
        next_station: Optional next station name for directional lookup (e.g., "Llyn-by-the-Sea")
        csv_path: Path to rail_routes.csv (for terminal detection)

    Returns:
        String like "Platform 1", "Platforms 1, 4", or "Platforms 4-7" or None if not found

    Examples:
        # Non-directional (may return multiple platforms for bidirectional routes)
        get_route_platform(benton, "R083")  # → "Platforms 1-2, 2-3"

        # Directional (returns specific platform for direction)
        get_route_platform(benton, "R083", "Llyn-by-the-Sea")  # → "Platforms 1-2"
        get_route_platform(benton, "R083", "Newry")  # → "Platforms 2-3"

        # Intermediate station (uses terminal detection)
        get_route_platform(benton_bridge, "R045", "Benton")  # → "Platform 3" (toward Stepford Victoria)
    """
    # PRIORITY 1: Try directional lookup if next_station provided
    if next_station:
        directional_map = build_directional_platform_map(station_data)

        # Try exact match first
        key = (route_code, next_station)
        if key in directional_map:
            platforms = directional_map[key]
            return _format_platform_list(platforms)

        # Try fuzzy match (in case station names don't match exactly)
        next_station_lower = next_station.lower()
        for (route, dest), plats in directional_map.items():
            dest_lower = dest.lower()
            if route == route_code and (next_station_lower in dest_lower or dest_lower in next_station_lower):
                return _format_platform_list(plats)

        # PRIORITY 1.5: Try terminal detection for intermediate stations
        # If next_station not in directional_map, it might be an intermediate stop
        # Find the terminal in that direction and use that for lookup
        current_station = station_data['name']
        terminal = _get_terminal_for_direction(route_code, current_station, next_station, csv_path)

        if terminal:
            # Try exact terminal match
            key = (route_code, terminal)
            if key in directional_map:
                platforms = directional_map[key]
                return _format_platform_list(platforms) + f" (toward {terminal})"

            # Try fuzzy terminal match
            terminal_lower = terminal.lower()
            for (route, dest), plats in directional_map.items():
                dest_lower = dest.lower()
                if route == route_code and (terminal_lower in dest_lower or dest_lower in terminal_lower):
                    return _format_platform_list(plats) + f" (toward {dest})"

    # PRIORITY 2: Fall back to non-directional route lookup
    route_platform_map = build_route_platform_map(station_data)

    if route_code in route_platform_map:
        platforms = route_platform_map[route_code]
        return _format_platform_list(platforms)

    return None


def _format_platform_list(platforms):
    """Helper function to format a list of platform numbers/ranges into a readable string."""
    # Sort platforms/ranges by their starting number
    def sort_key(p):
        # Extract first number from range (e.g., "4-7" → 4, "11" → 11)
        return int(p.split('-')[0])

    platforms_sorted = sorted(platforms, key=sort_key)

    if len(platforms_sorted) == 1:
        plat = platforms_sorted[0]
        # Check if it's a range (contains hyphen) or single platform
        if '-' in plat:
            return f"Platforms {plat}"
        else:
            return f"Platform {plat}"
    else:
        return f"Platforms {', '.join(platforms_sorted)}"


def get_route_context(station_name, operator_name, stations_dict, route_code=None, next_station=None):
    """
    Get ONLY route-relevant context for a station.
    Selective loading for route planning queries.

    Args:
        station_name: Name of the station
        operator_name: Operator being used (e.g., "Stepford Express")
        stations_dict: Dictionary of all stations
        route_code: Optional specific route code (e.g., "R001") for route-specific platforms
        next_station: Optional next station in journey for directional platform lookup

    Returns:
        Dictionary with minimal route-relevant info:
        - platforms: Total platform count
        - zone: Station zone
        - departure_platforms: Platform numbers (directional > route-specific > operator-level)
        - accessibility: Brief accessibility info

    Priority levels for platform lookup:
        1. Directional (route + next_station): "R083 to Llyn → Platform 1-2"
        2. Route-specific (route only): "R083 → Platforms 1-2, 2-3"
        3. Operator-level (fallback): "Stepford Express → Platforms 7-10"

    Skips: History, trivia, full layout details
    """
    station = get_station_details(station_name, stations_dict)
    if not station:
        return None

    info = extract_station_info(station)

    context = {
        'platforms': info.get('platforms'),
        'tracks': info.get('tracks'),
        'zone': info.get('zone'),
        'accessibility': info.get('accessibility')
    }

    # PRIORITY 1: Get directional platform if route_code AND next_station provided
    if route_code:
        # Try terminal detection with CSV path (v3.4)
        # Use just the filename - _load_route_terminals() will try multiple paths
        # including /mnt/data/ (Custom GPT) and local paths
        csv_path = "rail_routes.csv"
        route_platform = get_route_platform(station, route_code, next_station, csv_path=csv_path)
        if route_platform:
            context['departure_platforms'] = route_platform
            return context

    # PRIORITY 2: Fall back to operator-level platforms
    platform_summary = get_platform_summary(station)
    if operator_name in platform_summary:
        context['departure_platforms'] = platform_summary[operator_name]
    else:
        context['departure_platforms'] = None

    return context


def get_history_context(station_name, stations_dict):
    """
    Get ONLY historical context for a station.
    Selective loading for historical queries.

    Args:
        station_name: Name of the station
        stations_dict: Dictionary of all stations

    Returns:
        Dictionary with:
        - name: Station name
        - history: Historical timeline
        - url: Wiki link for more info

    Skips: Platform details, current operators, trivia
    """
    station = get_station_details(station_name, stations_dict)
    if not station:
        return None

    return {
        'name': station['name'],
        'history': get_station_history(station),
        'url': station['url']
    }


def get_platform_context(station_name, operator_filter=None, stations_dict=None):
    """
    Get ONLY platform assignments.
    Selective loading for platform-specific queries.

    Args:
        station_name: Name of the station
        operator_filter: Optional - return platforms for specific operator only
        stations_dict: Dictionary of all stations

    Returns:
        If operator_filter specified:
            {'operator': 'Name', 'platforms': 'Platform numbers'}
        Otherwise:
            Full platform summary dictionary

    Skips: History, trivia, full station details
    """
    station = get_station_details(station_name, stations_dict)
    if not station:
        return None

    summary = get_platform_summary(station)

    if operator_filter:
        # Return only platforms for this operator
        return {
            'operator': operator_filter,
            'platforms': summary.get(operator_filter, 'Not available at this station')
        }
    else:
        # Return all platform assignments
        return summary


def get_comprehensive_context(station_name, stations_dict):
    """
    Get FULL context for comprehensive "tell me about X" queries.

    Args:
        station_name: Name of the station
        stations_dict: Dictionary of all stations

    Returns:
        Dictionary with everything:
        - info: Full station info (platforms, tracks, zone, etc.)
        - history: Historical timeline
        - trivia: Interesting facts
        - platforms: Platform assignments by operator
        - summary: Brief description

    Use this for: "Tell me about", "Information about" queries
    """
    station = get_station_details(station_name, stations_dict)
    if not station:
        return None

    return {
        'info': extract_station_info(station),
        'history': get_station_history(station),
        'trivia': get_station_trivia(station),
        'platforms': get_platform_summary(station),
        'summary': station['summary'],
        'url': station['url']
    }


# Example usage
if __name__ == "__main__":
    # Load all station data from both parts
    stations = load_station_knowledge()
    print(f"Loaded {len(stations)} stations")

    # Get details for a specific station
    benton = get_station_details("Benton", stations)
    if benton:
        print(f"\nStation: {benton['name']}")
        print(f"Summary: {benton['summary']}")

        # Extract structured info
        info = extract_station_info(benton)
        print(f"Platforms: {info.get('platforms', 'Unknown')}")
        print(f"Tracks: {info.get('tracks', 'Unknown')}")

    # Search for content
    print("\n--- Stations mentioning 'Airport' ---")
    results = search_station_content("Airport", stations)
    for station, count in results[:5]:
        print(f"{station}: {count} mentions")
