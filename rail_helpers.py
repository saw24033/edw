"""
Stepford County Railway Network Helper Functions
=================================================
These functions are designed to run inside a Custom GPT with Code Interpreter.
They provide train network analysis for the Stepford County Railway system.

Usage in GPT Python environment:
    import rail_helpers
    graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
    rail_helpers.operators_at_station(graph, "Stepford Central")
"""

import csv
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional


def load_rail_network(path="rail_routes.csv") -> Tuple[Dict, List[str], List[str]]:
    """
    Load the rail network from CSV into a graph structure.

    Args:
        path: Path to the rail_routes.csv file

    Returns:
        Tuple of (graph, operators, lines) where:
        - graph: dict mapping station -> list of edge dicts
        - operators: sorted list of all operators
        - lines: sorted list of all line IDs
    """
    graph = defaultdict(list)  # station -> list of edges
    operators = set()
    lines = set()

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            operator = row["operator"]
            line = row["line"]
            u = row["from_station"]
            v = row["to_station"]
            time = float(row["travel_time_min"])
            service_type = row.get("service_type", "")
            route_origin = row.get("route_origin", "")
            route_destination = row.get("route_destination", "")

            # Create edge from u to v
            edge_uv = {
                "to": v,
                "operator": operator,
                "line": line,
                "time": time,
                "service_type": service_type,
                "route_origin": route_origin,
                "route_destination": route_destination,
            }

            # Create reverse edge from v to u (bidirectional)
            edge_vu = {
                "to": u,
                "operator": operator,
                "line": line,
                "time": time,
                "service_type": service_type,
                "route_origin": route_origin,
                "route_destination": route_destination,
            }

            graph[u].append(edge_uv)
            graph[v].append(edge_vu)
            operators.add(operator)
            lines.add(line)

    return dict(graph), sorted(operators), sorted(lines)


def operators_at_station(graph: Dict, station: str) -> List[str]:
    """
    Find which operators serve a given station.

    Args:
        graph: Network graph from load_rail_network()
        station: Station name

    Returns:
        Sorted list of operator names
    """
    if station not in graph:
        return []

    ops = {edge["operator"] for edge in graph[station]}
    return sorted(ops)


def lines_at_station(graph: Dict, station: str) -> List[str]:
    """
    Find which lines serve a given station.

    Args:
        graph: Network graph from load_rail_network()
        station: Station name

    Returns:
        Sorted list of line IDs
    """
    if station not in graph:
        return []

    line_ids = {edge["line"] for edge in graph[station]}
    return sorted(line_ids)


def direct_services_between(graph: Dict, station_a: str, station_b: str) -> List[Dict]:
    """
    Find all direct train services between two stations (no changes required).

    Args:
        graph: Network graph from load_rail_network()
        station_a: Starting station
        station_b: Destination station

    Returns:
        List of service dicts with operator, line, time, service_type
    """
    if station_a not in graph:
        return []

    services = []
    for edge in graph[station_a]:
        if edge["to"] == station_b:
            services.append({
                "operator": edge["operator"],
                "line": edge["line"],
                "time": edge["time"],
                "service_type": edge["service_type"],
                "route_origin": edge.get("route_origin", ""),
                "route_destination": edge.get("route_destination", ""),
            })

    return services


def edges_for_operator(graph: Dict, operator_name: str) -> List[Dict]:
    """
    Get all unique edges (station pairs) operated by a specific operator.

    Args:
        graph: Network graph from load_rail_network()
        operator_name: Name of the operator

    Returns:
        List of edge dicts with from, to, line, time, service_type
    """
    seen = set()
    edges = []

    for u, edge_list in graph.items():
        for e in edge_list:
            if e["operator"] != operator_name:
                continue

            v = e["to"]
            # Use sorted tuple to avoid duplicates (A-B vs B-A)
            key = tuple(sorted([u, v]))

            if key in seen:
                continue

            seen.add(key)
            edges.append({
                "from": u,
                "to": v,
                "line": e["line"],
                "time": e["time"],
                "service_type": e["service_type"],
            })

    return edges


def edges_for_line(graph: Dict, line_id: str) -> List[Dict]:
    """
    Get all edges for a specific line/route.

    Args:
        graph: Network graph from load_rail_network()
        line_id: Line identifier (e.g., "R001")

    Returns:
        List of edge dicts with from, to, operator, time, service_type
    """
    seen = set()
    edges = []

    for u, edge_list in graph.items():
        for e in edge_list:
            if e["line"] != line_id:
                continue

            v = e["to"]
            key = tuple(sorted([u, v]))

            if key in seen:
                continue

            seen.add(key)
            edges.append({
                "from": u,
                "to": v,
                "operator": e["operator"],
                "time": e["time"],
                "service_type": e["service_type"],
            })

    return edges


def all_stations(graph: Dict) -> List[str]:
    """
    Get all station names in the network.

    Args:
        graph: Network graph from load_rail_network()

    Returns:
        Sorted list of station names
    """
    return sorted(graph.keys())


def station_connections(graph: Dict, station: str) -> List[str]:
    """
    Get all stations directly connected to the given station.

    Args:
        graph: Network graph from load_rail_network()
        station: Station name

    Returns:
        Sorted list of connected station names
    """
    if station not in graph:
        return []

    connected = {edge["to"] for edge in graph[station]}
    return sorted(connected)


def search_stations(graph: Dict, query: str) -> List[str]:
    """
    Search for stations matching a query string (case-insensitive fuzzy search).

    Args:
        graph: Network graph from load_rail_network()
        query: Search string

    Returns:
        List of matching station names
    """
    query_lower = query.lower()
    stations = all_stations(graph)

    # Exact match
    exact_matches = [s for s in stations if s.lower() == query_lower]
    if exact_matches:
        return exact_matches

    # Contains match
    contains_matches = [s for s in stations if query_lower in s.lower()]
    if contains_matches:
        return contains_matches

    # Word-based match
    query_words = query_lower.split()
    word_matches = []
    for station in stations:
        station_lower = station.lower()
        if all(word in station_lower for word in query_words):
            word_matches.append(station)

    return word_matches


def station_info(graph: Dict, station: str) -> Optional[Dict]:
    """
    Get comprehensive information about a station.

    Args:
        graph: Network graph from load_rail_network()
        station: Station name

    Returns:
        Dict with station info or None if not found
    """
    if station not in graph:
        return None

    operators = operators_at_station(graph, station)
    lines = lines_at_station(graph, station)
    connections = station_connections(graph, station)

    return {
        "name": station,
        "operators": operators,
        "num_operators": len(operators),
        "lines": lines,
        "num_lines": len(lines),
        "connections": connections,
        "num_connections": len(connections),
        "is_major_hub": len(lines) > 10,
    }


def services_on_same_line(graph: Dict, station_a: str, station_b: str) -> List[Dict]:
    """
    Find services where both stations are on the same line (multi-segment check).
    This checks if you can travel from A to B on the same line without changing trains.

    Args:
        graph: Network graph from load_rail_network()
        station_a: Starting station
        station_b: Destination station

    Returns:
        List of line services connecting the stations
    """
    if station_a not in graph or station_b not in graph:
        return []

    # Get all lines serving station_a
    lines_at_a = {edge["line"]: edge for edge in graph[station_a]}

    # Get all lines serving station_b
    lines_at_b = {edge["line"]: edge for edge in graph[station_b]}

    # Find common lines
    common_lines = set(lines_at_a.keys()) & set(lines_at_b.keys())

    services = []
    for line_id in common_lines:
        # For each common line, check if there's a path from A to B on that line
        edge_a = lines_at_a[line_id]

        services.append({
            'line': line_id,
            'operator': edge_a['operator'],
            'service_type': edge_a['service_type'],
            'route_origin': edge_a.get('route_origin', ''),
            'route_destination': edge_a.get('route_destination', '')
        })

    return services


def find_interchanges(graph: Dict, station_a: str, station_b: str) -> List[str]:
    """
    Find potential interchange stations between two stations.
    An interchange is a station that connects to both A and B.

    Args:
        graph: Network graph from load_rail_network()
        station_a: First station
        station_b: Second station

    Returns:
        List of potential interchange station names
    """
    if station_a not in graph or station_b not in graph:
        return []

    connections_a = set(station_connections(graph, station_a))
    connections_b = set(station_connections(graph, station_b))

    # Stations that connect to both A and B
    interchanges = connections_a & connections_b

    return sorted(interchanges)


def shortest_path(graph: Dict, start: str, end: str) -> Optional[Dict]:
    """
    Find the shortest path between two stations using Dijkstra's algorithm.
    Handles any number of interchanges automatically.

    Args:
        graph: Network graph from load_rail_network()
        start: Starting station name
        end: Destination station name

    Returns:
        Dict with path details or None if no path exists:
        {
            'stations': ['Station A', 'Station B', ...],
            'total_time': 25.5,  # minutes including interchange penalties
            'num_interchanges': 2,
            'legs': [
                {
                    'from': 'Station A',
                    'to': 'Station B',
                    'operator': 'AirLink',
                    'line': 'R001',
                    'time': 5.0,
                    'service_type': 'Express'
                },
                ...
            ]
        }
    """
    import heapq

    if start not in graph or end not in graph:
        return None

    if start == end:
        return {
            'stations': [start],
            'total_time': 0,
            'num_interchanges': 0,
            'legs': []
        }

    # Dijkstra's algorithm with priority queue
    # State: (cumulative_time, counter, current_station, path_of_stations, legs, num_changes)
    # Counter is used as tiebreaker to avoid comparing dicts/lists
    counter = 0
    pq = [(0, counter, start, [start], [], 0)]
    visited = {}  # station -> best_time_so_far

    INTERCHANGE_PENALTY = 4.0  # minutes for each interchange

    while pq:
        current_time, _, current_station, path, legs, num_changes = heapq.heappop(pq)

        # If we've reached the destination
        if current_station == end:
            return {
                'stations': path,
                'total_time': current_time,
                'num_interchanges': num_changes,
                'legs': legs
            }

        # Skip if we've already found a better path to this station
        if current_station in visited and visited[current_station] <= current_time:
            continue
        visited[current_station] = current_time

        # Explore neighbors
        for edge in graph[current_station]:
            next_station = edge["to"]
            travel_time = edge["time"]

            # Calculate interchange penalty
            # Add penalty if we're changing from a previous line
            interchange_time = 0
            if legs:  # Not the first leg
                last_line = legs[-1]["line"]
                current_line = edge["line"]
                if last_line != current_line:
                    interchange_time = INTERCHANGE_PENALTY
                    new_num_changes = num_changes + 1
                else:
                    new_num_changes = num_changes
            else:
                new_num_changes = 0

            new_time = current_time + travel_time + interchange_time
            new_path = path + [next_station]
            new_legs = legs + [{
                'from': current_station,
                'to': next_station,
                'operator': edge["operator"],
                'line': edge["line"],
                'time': travel_time,
                'service_type': edge["service_type"]
            }]

            # Only add to queue if we haven't visited or found a better route
            if next_station not in visited or visited[next_station] > new_time:
                counter += 1
                heapq.heappush(pq, (new_time, counter, next_station, new_path, new_legs, new_num_changes))

    # No path found
    return None


def format_journey(journey: Dict) -> str:
    """
    Format a journey from shortest_path() into a readable string.

    Args:
        journey: Journey dict from shortest_path()

    Returns:
        Formatted string describing the journey
    """
    if not journey:
        return "No route found."

    if journey['num_interchanges'] == 0 and len(journey['legs']) == 0:
        return "You are already at the destination."

    output = []
    output.append(f"Journey: {journey['stations'][0]} → {journey['stations'][-1]}")
    output.append(f"Total time: {journey['total_time']:.1f} minutes")
    output.append(f"Interchanges: {journey['num_interchanges']}")
    output.append("")

    current_line = None
    leg_group = []

    for i, leg in enumerate(journey['legs']):
        # Group consecutive legs on the same line
        if leg['line'] != current_line:
            # Print previous group if exists
            if leg_group:
                first_leg = leg_group[0]
                last_leg = leg_group[-1]
                total_leg_time = sum(l['time'] for l in leg_group)
                stations_on_line = [first_leg['from']] + [l['to'] for l in leg_group]

                output.append(f"• Take {first_leg['operator']} {first_leg['line']} ({first_leg['service_type']})")
                output.append(f"  From: {first_leg['from']}")
                output.append(f"  To: {last_leg['to']}")
                output.append(f"  Time: {total_leg_time:.1f} minutes")
                output.append(f"  Stops: {' → '.join(stations_on_line)}")

                if i < len(journey['legs']):  # Not the last leg
                    output.append(f"\n  ⚠️  Change trains at {last_leg['to']} (allow 4 minutes)")
                output.append("")

            # Start new group
            leg_group = [leg]
            current_line = leg['line']
        else:
            leg_group.append(leg)

    # Print final group
    if leg_group:
        first_leg = leg_group[0]
        last_leg = leg_group[-1]
        total_leg_time = sum(l['time'] for l in leg_group)
        stations_on_line = [first_leg['from']] + [l['to'] for l in leg_group]

        output.append(f"• Take {first_leg['operator']} {first_leg['line']} ({first_leg['service_type']})")
        output.append(f"  From: {first_leg['from']}")
        output.append(f"  To: {last_leg['to']}")
        output.append(f"  Time: {total_leg_time:.1f} minutes")
        output.append(f"  Stops: {' → '.join(stations_on_line)}")

    return "\n".join(output)


# Optional: Simple text-based network visualization
def print_operator_routes(graph: Dict, operator_name: str) -> None:
    """
    Print all routes for a specific operator in a readable format.

    Args:
        graph: Network graph from load_rail_network()
        operator_name: Operator name
    """
    edges = edges_for_operator(graph, operator_name)

    if not edges:
        print(f"No routes found for operator: {operator_name}")
        return

    print(f"\n{'='*60}")
    print(f"Routes operated by: {operator_name}")
    print(f"{'='*60}")

    # Group by line
    by_line = defaultdict(list)
    for edge in edges:
        by_line[edge["line"]].append(edge)

    for line_id in sorted(by_line.keys()):
        line_edges = by_line[line_id]
        print(f"\nLine {line_id} ({line_edges[0]['service_type']}):")

        for edge in line_edges:
            print(f"  {edge['from']} ↔ {edge['to']} ({edge['time']} min)")


def print_station_summary(graph: Dict, station: str) -> None:
    """
    Print a comprehensive summary of a station.

    Args:
        graph: Network graph from load_rail_network()
        station: Station name
    """
    info = station_info(graph, station)

    if info is None:
        print(f"Station not found: {station}")
        return

    print(f"\n{'='*60}")
    print(f"Station: {info['name']}")
    print(f"{'='*60}")
    print(f"Major Hub: {'Yes' if info['is_major_hub'] else 'No'}")
    print(f"Direct Connections: {info['num_connections']}")
    print(f"Operators: {info['num_operators']} - {', '.join(info['operators'])}")
    print(f"Lines: {info['num_lines']}")
    print(f"\nConnected Stations:")
    for conn in info['connections']:
        print(f"  - {conn}")


# Example usage when run directly
if __name__ == "__main__":
    print("Loading Stepford County Railway network...")
    graph, operators, lines = load_rail_network("rail_routes.csv")

    print(f"\n✅ Network loaded successfully!")
    print(f"📊 Stations: {len(all_stations(graph))}")
    print(f"📊 Operators: {len(operators)}")
    print(f"📊 Lines: {len(lines)}")

    print(f"\n🚂 Operators in network:")
    for op in operators:
        print(f"  - {op}")

    print("\n" + "="*60)
    print("Example 1: Which operators serve Stepford Central?")
    print("="*60)
    ops = operators_at_station(graph, "Stepford Central")
    print(f"Stepford Central is served by: {', '.join(ops)}")

    print("\n" + "="*60)
    print("Example 2: Direct services from Stepford Central to Benton")
    print("="*60)
    services = direct_services_between(graph, "Stepford Central", "Benton")
    if services:
        for svc in services[:3]:  # Show first 3
            print(f"  - {svc['operator']} {svc['line']}: {svc['time']} min ({svc['service_type']})")
    else:
        print("  No direct services found")

    print("\n" + "="*60)
    print("Example 3: Station info for Benton")
    print("="*60)
    print_station_summary(graph, "Benton")

    print("\n" + "="*60)
    print("Example 4: Journey planning - Benton to Llyn-by-the-Sea")
    print("="*60)
    journey = shortest_path(graph, "Benton", "Llyn-by-the-Sea")
    if journey:
        print(format_journey(journey))
    else:
        print("No route found")
