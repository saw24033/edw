"""
Plotting helpers for Stepford County Railway network visualization
To be used with matplotlib in Code Interpreter environment
"""

import csv
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple


def load_station_coords(path="station_coords.csv") -> Dict[str, Tuple[float, float]]:
    """
    Load station coordinates from CSV.

    Args:
        path: Path to station_coords.csv

    Returns:
        Dict mapping station name to (x, y) tuple
    """
    coords = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            station = row["station"]
            x = float(row["x"])
            y = float(row["y"])
            coords[station] = (x, y)

    return coords


def plot_operator_network(graph: Dict, operator_name: str, station_coords: Dict = None):
    """
    Plot the network map for a specific operator.

    Args:
        graph: Network graph from rail_helpers.load_rail_network()
        operator_name: Name of the operator to visualize
        station_coords: Dict of station -> (x, y) coordinates (optional)
    """
    # Import helper to get edges
    import rail_helpers

    edges = rail_helpers.edges_for_operator(graph, operator_name)

    if not edges:
        print(f"No routes found for operator: {operator_name}")
        return

    # Load coordinates if not provided
    if station_coords is None:
        try:
            station_coords = load_station_coords()
        except FileNotFoundError:
            print("Warning: station_coords.csv not found. Cannot plot network.")
            return

    # Create the plot
    plt.figure(figsize=(14, 10))

    # Plot all edges for this operator
    for edge in edges:
        from_station = edge["from"]
        to_station = edge["to"]

        if from_station not in station_coords or to_station not in station_coords:
            continue

        x1, y1 = station_coords[from_station]
        x2, y2 = station_coords[to_station]

        plt.plot([x1, x2], [y1, y2], 'b-', alpha=0.3, linewidth=1.5)

    # Plot all stations served by this operator
    stations_on_network = set()
    for edge in edges:
        stations_on_network.add(edge["from"])
        stations_on_network.add(edge["to"])

    for station in stations_on_network:
        if station in station_coords:
            x, y = station_coords[station]
            plt.scatter([x], [y], s=100, c='red', zorder=5)
            plt.text(x + 0.2, y + 0.2, station, fontsize=7, zorder=6)

    plt.title(f"Rail Network – {operator_name}", fontsize=16, fontweight='bold')
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.axis("equal")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()


def plot_line_network(graph: Dict, line_id: str, station_coords: Dict = None):
    """
    Plot the network map for a specific line/route.

    Args:
        graph: Network graph from rail_helpers.load_rail_network()
        line_id: Line identifier (e.g., "R001")
        station_coords: Dict of station -> (x, y) coordinates (optional)
    """
    import rail_helpers

    edges = rail_helpers.edges_for_line(graph, line_id)

    if not edges:
        print(f"No edges found for line: {line_id}")
        return

    # Load coordinates if not provided
    if station_coords is None:
        try:
            station_coords = load_station_coords()
        except FileNotFoundError:
            print("Warning: station_coords.csv not found. Cannot plot network.")
            return

    # Create the plot
    plt.figure(figsize=(12, 8))

    # Plot edges
    for edge in edges:
        from_station = edge["from"]
        to_station = edge["to"]

        if from_station not in station_coords or to_station not in station_coords:
            continue

        x1, y1 = station_coords[from_station]
        x2, y2 = station_coords[to_station]

        plt.plot([x1, x2], [y1, y2], 'g-', alpha=0.5, linewidth=2)

    # Plot stations
    stations_on_line = set()
    for edge in edges:
        stations_on_line.add(edge["from"])
        stations_on_line.add(edge["to"])

    for station in stations_on_line:
        if station in station_coords:
            x, y = station_coords[station]
            plt.scatter([x], [y], s=120, c='darkgreen', zorder=5)
            plt.text(x + 0.2, y + 0.2, station, fontsize=8, zorder=6)

    operator = edges[0]["operator"] if edges else "Unknown"
    service_type = edges[0]["service_type"] if edges else ""

    plt.title(f"Line {line_id} – {operator} ({service_type})", fontsize=14, fontweight='bold')
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.axis("equal")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()


def plot_full_network(graph: Dict, station_coords: Dict = None):
    """
    Plot the entire Stepford County Railway network.

    Args:
        graph: Network graph from rail_helpers.load_rail_network()
        station_coords: Dict of station -> (x, y) coordinates (optional)
    """
    # Load coordinates if not provided
    if station_coords is None:
        try:
            station_coords = load_station_coords()
        except FileNotFoundError:
            print("Warning: station_coords.csv not found. Cannot plot network.")
            return

    plt.figure(figsize=(16, 12))

    # Plot all edges (deduplicated)
    seen = set()
    for station, edges in graph.items():
        for edge in edges:
            from_station = station
            to_station = edge["to"]

            # Avoid duplicates
            key = tuple(sorted([from_station, to_station]))
            if key in seen:
                continue
            seen.add(key)

            if from_station not in station_coords or to_station not in station_coords:
                continue

            x1, y1 = station_coords[from_station]
            x2, y2 = station_coords[to_station]

            plt.plot([x1, x2], [y1, y2], 'gray', alpha=0.2, linewidth=0.8)

    # Plot all stations
    for station, (x, y) in station_coords.items():
        plt.scatter([x], [y], s=50, c='blue', zorder=5)
        plt.text(x + 0.15, y + 0.15, station, fontsize=6, alpha=0.7, zorder=6)

    plt.title("Stepford County Railway – Full Network Map", fontsize=18, fontweight='bold')
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.axis("equal")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    import rail_helpers

    print("Loading network and coordinates...")
    graph, operators, lines = rail_helpers.load_rail_network("rail_routes.csv")
    coords = load_station_coords("station_coords.csv")

    print(f"✅ Loaded {len(graph)} stations and {len(coords)} coordinates")

    print("\nGenerating sample plot for AirLink operator...")
    plot_operator_network(graph, "AirLink", coords)
