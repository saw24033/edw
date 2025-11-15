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
