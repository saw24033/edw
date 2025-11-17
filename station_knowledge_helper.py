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

    # Extract common fields using regex
    patterns = {
        'platforms': r'Platforms?\s+(\d+)',
        'tracks': r'Tracks?\s+(\d+)',
        'zone': r'Zone\s+([^\n]+)',
        'location': r'Location\s+([^\n]+?)(?:\s+Zone|$)',
        'station_code': r'Station code\s+([A-Z]{2,4})',
        'operator': r'(?:Served by|Operated by|Managed by)\s+([^\n]+)',
        'accessibility': r'Accessibility\s+([^\n]+)',
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info[field] = match.group(1).strip()

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
        'Stepford Express': 'Platforms 6-9'
    }
    """
    platforms = get_platform_assignments(station_data)
    operator_platforms = {}

    # Group platforms by operator
    for plat_info in platforms:
        services = plat_info['services']
        plat_num = plat_info['platform']

        # Find operators mentioned
        operators = ['Waterline', 'Stepford Connect', 'Stepford Express', 'Metro', 'AirLink']
        for op in operators:
            if op in services:
                if op not in operator_platforms:
                    operator_platforms[op] = []
                operator_platforms[op].append(plat_num)

    # Convert to ranges
    summary = {}
    for op, plats in operator_platforms.items():
        # Remove duplicates and sort
        unique_plats = sorted(set(plats), key=lambda x: int(x.split('-')[0]))
        summary[op] = f"Platform{'s' if len(unique_plats) > 1 else ''} {', '.join(unique_plats)}"

    return summary


def get_route_context(station_name, operator_name, stations_dict):
    """
    Get ONLY route-relevant context for a station.
    Selective loading for route planning queries.

    Args:
        station_name: Name of the station
        operator_name: Operator being used (e.g., "Stepford Express")
        stations_dict: Dictionary of all stations

    Returns:
        Dictionary with minimal route-relevant info:
        - platforms: Total platform count
        - zone: Station zone
        - departure_platforms: Platform numbers for the specific operator
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

    # Get platform assignments for THIS operator only
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
