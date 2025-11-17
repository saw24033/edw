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

        # Split by platform numbers (format: "1 Benton R001 R005...", "2 R003 R039...")
        # Use lookahead to split before each platform number followed by station/route
        segments = re.split(r'\s+(?=\d+\s+(?:[A-Z][a-z]+|R\d+))', services_text)

        for segment in segments:
            # Extract platform number from start of segment
            plat_match = re.match(r'^(\d+)\s+', segment)
            if plat_match:
                platform = plat_match.group(1)

                # Extract all route codes from this segment
                routes = re.findall(r'R\d+', segment)

                # Map each route to this platform
                for route in routes:
                    if route not in route_platform_map:
                        route_platform_map[route] = []
                    if platform not in route_platform_map[route]:
                        route_platform_map[route].append(platform)

    return route_platform_map


def get_route_platform(station_data, route_code):
    """
    Get the specific platform(s) for a route at this station.

    Args:
        station_data: Station data dict from get_station_details()
        route_code: Route code (e.g., "R001", "R078")

    Returns:
        String like "Platform 1" or "Platforms 1, 4" or None if not found
    """
    route_platform_map = build_route_platform_map(station_data)

    if route_code in route_platform_map:
        platforms = sorted(route_platform_map[route_code], key=int)
        if len(platforms) == 1:
            return f"Platform {platforms[0]}"
        else:
            return f"Platforms {', '.join(platforms)}"

    return None


def get_route_context(station_name, operator_name, stations_dict, route_code=None):
    """
    Get ONLY route-relevant context for a station.
    Selective loading for route planning queries.

    Args:
        station_name: Name of the station
        operator_name: Operator being used (e.g., "Stepford Express")
        stations_dict: Dictionary of all stations
        route_code: Optional specific route code (e.g., "R001") for route-specific platforms

    Returns:
        Dictionary with minimal route-relevant info:
        - platforms: Total platform count
        - zone: Station zone
        - departure_platforms: Platform numbers (route-specific if route_code provided, else operator-level)
        - accessibility: Brief accessibility info

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

    # PRIORITY 1: Get route-specific platform if route_code provided
    if route_code:
        route_platform = get_route_platform(station, route_code)
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
