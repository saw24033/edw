"""
Station Knowledge Helper - Parse scr_stations_part1.md and scr_stations_part2.md for detailed station info
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

    # Strategy 2: Look in Services table for platform assignments
    # Format: "Platform(s) ... 0-6 Terminus R077 R080..." or "7-11 R024 to..."
    # Extract platform ranges and route codes from Services section
    if not operator_platforms:
        services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)', content, re.DOTALL | re.IGNORECASE)
        if services_section:
            services_text = services_section.group(1)

            # Find platform ranges with route codes
            # Services section often has format: "0-6 Terminus R077... 7-11 R024..." (all on one line)
            platform_route_map = {}

            # Split by platform range patterns using lookahead
            # This finds sections like "0-6 ... " or "7-11 ... " up to the next platform range
            # Pattern: digit-digit followed by space, capture everything until next digit-digit or end
            segments = re.split(r'\s+(?=\d+-\d+\s)', services_text)

            for segment in segments:
                # Extract platform range from start of segment
                plat_match = re.match(r'^(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\s+', segment)
                if plat_match:
                    plat_range = plat_match.group(1).strip()

                    # Extract all route codes from this segment
                    route_codes = re.findall(r'R\d+', segment)

                    if route_codes and len(plat_range) <= 10:  # Sanity check: platform ranges shouldn't be long
                        if plat_range not in platform_route_map:
                            platform_route_map[plat_range] = set()
                        platform_route_map[plat_range].update(route_codes)

            # Map route codes to operators using route number heuristics and content checking
            # Route number ranges (strong heuristics):
            # R001-R050: Stepford Connect, Metro, Waterline
            # R075-R099: Stepford Express
            # R100+: Various operators
            for plat_range, routes in platform_route_map.items():
                # Use route number heuristics as primary signal
                sample_routes = list(routes)[:5]  # Check more routes for better accuracy
                operator_votes = {}

                for route in sample_routes:
                    # Extract route number
                    route_num = int(route[1:])  # Remove 'R' prefix

                    # Strong heuristic based on route number ranges
                    if 75 <= route_num <= 99:
                        # Express routes
                        operator_votes['Stepford Express'] = operator_votes.get('Stepford Express', 0) + 3
                    elif 1 <= route_num <= 50:
                        # Connect/Metro/Waterline routes - check content for specifics
                        # Check which operator is mentioned with this route
                        for op in ['Stepford Connect', 'Metro', 'Waterline']:
                            pattern = rf'{op}.{{0,150}}{route}|{route}.{{0,150}}{op}'
                            if re.search(pattern, content[:5000]):
                                operator_votes[op] = operator_votes.get(op, 0) + 2
                                break
                        else:
                            # Default to Connect for R001-R050 range
                            operator_votes['Stepford Connect'] = operator_votes.get('Stepford Connect', 0) + 1
                    elif route_num >= 100:
                        # Various operators - check content
                        for op in ['Stepford Express', 'Stepford Connect', 'Waterline', 'Metro', 'AirLink']:
                            pattern = rf'{op}.{{0,150}}{route}|{route}.{{0,150}}{op}'
                            if re.search(pattern, content[:5000]):
                                operator_votes[op] = operator_votes.get(op, 0) + 2

                # Assign to operator with most votes
                if operator_votes:
                    best_operator = max(operator_votes, key=operator_votes.get)
                    # Allow multiple platform ranges per operator
                    if best_operator in operator_platforms:
                        # Append to existing range
                        operator_platforms[best_operator] += f", {plat_range}"
                    else:
                        operator_platforms[best_operator] = f"Platforms {plat_range}"

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


def build_route_platform_map(station_data):
    """
    Build a mapping of route codes to their specific platforms at a station.

    Returns a dictionary: {'R001': ['1', '4'], 'R003': ['2', '3'], ...}

    This provides route-specific platform information (more granular than operator-level).
    Example: At Benton Bridge, airport routes (R001, R046) use platforms 1 & 4,
    while other Connect routes use platforms 2 & 3.
    """
    content = station_data['full_content']
    route_platform_map = {}

    # Parse Services section for route-platform assignments
    services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)', content, re.DOTALL | re.IGNORECASE)
    if services_section:
        services_text = services_section.group(1)

        # Split by platform numbers/ranges (format: "1-2 West Benton R010...", "4-7 Coxly R001...")
        # Use lookahead to split before each platform number/range followed by station name
        segments = re.split(r'\s+(?=\d+(?:-\d+)?\s+[A-Z])', services_text)

        for segment in segments:
            # Extract platform number or range from start of segment
            # Matches: "1", "2", "1-2", "4-7", "11-13", etc.
            plat_match = re.match(r'^(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\s+', segment)
            if plat_match:
                platform_range = plat_match.group(1).strip()

                # Extract all route codes from this segment
                routes = re.findall(r'R\d+', segment)

                # Map each route to this platform/range
                for route in routes:
                    if route not in route_platform_map:
                        route_platform_map[route] = []
                    if platform_range not in route_platform_map[route]:
                        route_platform_map[route].append(platform_range)

    return route_platform_map


def build_directional_platform_map(station_data):
    """
    Build a mapping of (route, destination) to platforms for directional accuracy.

    Returns a dictionary: {('R083', 'Llyn-by-the-Sea'): ['1-2'], ('R083', 'Newry'): ['2-3'], ...}

    This handles bidirectional tracks where the same route uses different platforms
    depending on direction. Example at Benton:
    - R083 TO Llyn-by-the-Sea → Platforms 1-2
    - R083 TO Newry → Platforms 2-3
    """
    content = station_data['full_content']
    directional_map = {}

    # Parse Services section
    services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)', content, re.DOTALL | re.IGNORECASE)
    if services_section:
        services_text = services_section.group(1)

        # Split by platform ranges
        segments = re.split(r'\s+(?=\d+(?:-\d+)?\s+[A-Z])', services_text)

        for segment in segments:
            # Extract platform range from start
            plat_match = re.match(r'^(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\s+', segment)
            if plat_match:
                platform_range = plat_match.group(1).strip()

                # Find all "Route to Destination" patterns
                # Format: "R083 to Llyn-by-the-Sea Morganstown R084..."
                # where "Morganstown" is the previous station for the next service R084
                # Pattern: R### to [destination] stopping before [station name] R### or end of segment
                route_dest_pattern = r'(R\d+)\s+to\s+([\w\s\-]+?)(?=\s+\w+\s+R\d+|$)'
                matches = re.findall(route_dest_pattern, segment)

                for route_code, destination in matches:
                    destination_clean = destination.strip()
                    key = (route_code, destination_clean)

                    if key not in directional_map:
                        directional_map[key] = []
                    if platform_range not in directional_map[key]:
                        directional_map[key].append(platform_range)

    return directional_map


def get_route_platform(station_data, route_code, next_station=None):
    """
    Get the specific platform(s) for a route at this station.

    Args:
        station_data: Station data dict from get_station_details()
        route_code: Route code (e.g., "R001", "R078")
        next_station: Optional next station name for directional lookup (e.g., "Llyn-by-the-Sea")

    Returns:
        String like "Platform 1", "Platforms 1, 4", or "Platforms 4-7" or None if not found

    Examples:
        # Non-directional (may return multiple platforms for bidirectional routes)
        get_route_platform(benton, "R083")  # → "Platforms 1-2, 2-3"

        # Directional (returns specific platform for direction)
        get_route_platform(benton, "R083", "Llyn-by-the-Sea")  # → "Platforms 1-2"
        get_route_platform(benton, "R083", "Newry")  # → "Platforms 2-3"
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
            if route == route_code and next_station_lower in dest.lower():
                return _format_platform_list(plats)

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
        route_platform = get_route_platform(station, route_code, next_station)
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
