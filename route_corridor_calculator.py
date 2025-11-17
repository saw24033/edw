#!/usr/bin/env python3
"""
Stepford County Railway - Route Corridor Calculator
====================================================
Calculate the exact path a service takes through the network and identify skipped stations.

This implements proper public transport routing logic:
1. Build the station network graph (physical track connections)
2. Given a service's stop list, calculate the full corridor path
3. Identify which stations are passed but not stopped at

No hardcoded corridors - everything is calculated algorithmically.
"""

import json
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Set, Optional


class RouteCorridorCalculator:
    """
    Calculate route corridors and identify skipped stations.

    This works like a real public transport routing engine:
    - Network graph defines physical station connections
    - Service data defines which stations are actually served
    - Pathfinding calculates the corridor between consecutive stops
    """

    def __init__(self, routes_file='stepford_routes_with_segment_minutes_ai_knowledge_base.json'):
        """Load route data and build the station network graph."""
        with open(routes_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.routes = self.data.get('routes', {})
        self.stations_list = self.data.get('stations', [])

        # Build the physical station network graph
        self.network_graph = self._build_station_network()

    def _build_station_network(self) -> Dict[str, Set[str]]:
        """
        Build the station network graph showing physical track connections.

        This is NOT the service graph - it's the underlying rail infrastructure.
        Each edge represents a physical track connection between adjacent stations.

        Uses the 'connections' data which shows all physical links, including
        those used by express services that skip intermediate stations.

        Returns:
            Dict mapping station name -> set of directly connected stations
        """
        graph = defaultdict(set)

        # Use the connections data if available (more accurate)
        connections = self.data.get('connections', {})

        if connections:
            # Build from explicit connection data
            for station, links in connections.items():
                for link in links:
                    to_station = link.get('to_station')
                    if to_station:
                        # Connections are already bidirectional in the data
                        graph[station].add(to_station)
        else:
            # Fallback: Build from route stop lists
            for route_code, route_data in self.routes.items():
                # Skip removed routes
                if 'REMOVED' in route_data.get('route_type', ''):
                    continue

                stations = route_data.get('stations', [])
                if len(stations) < 2:
                    continue

                # Add edges between consecutive stations
                for i in range(len(stations) - 1):
                    station_a = stations[i]
                    station_b = stations[i + 1]

                    # Bidirectional
                    graph[station_a].add(station_b)
                    graph[station_b].add(station_a)

        return graph

    def shortest_station_path(self, start: str, end: str) -> Optional[List[str]]:
        """
        Find the shortest path between two stations in the network graph.

        Uses BFS since all track segments have equal weight for pathfinding.
        This finds the physical route a train would take.

        Args:
            start: Starting station name
            end: Destination station name

        Returns:
            List of station names from start to end, or None if no path exists
        """
        if start == end:
            return [start]

        if start not in self.network_graph or end not in self.network_graph:
            return None

        # BFS to find shortest path
        queue = deque([[start]])
        visited = {start}

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == end:
                return path

            for neighbor in self.network_graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        return None

    def _find_corridor_stations(self, start: str, end: str) -> Set[str]:
        """
        Find all stations that exist on ANY route between start and end.

        This identifies the full corridor including stations that some services skip.

        Args:
            start: Starting station
            end: Ending station

        Returns:
            Set of all station names on the corridor
        """
        corridor_stations = set()

        # Find all routes that serve both stations
        for route_code, route_data in self.routes.items():
            if 'REMOVED' in route_data.get('route_type', ''):
                continue

            stations = route_data.get('stations', [])

            # Check if this route serves both stations in order
            try:
                start_idx = stations.index(start)
                end_idx = stations.index(end)

                # Only consider if they're in the right order
                if start_idx < end_idx:
                    # Add all stations between start and end on this route
                    corridor_stations.update(stations[start_idx:end_idx + 1])
            except ValueError:
                # One or both stations not on this route
                continue

        return corridor_stations

    def calculate_route_corridor(self, route_code: str) -> Optional[Dict]:
        """
        Calculate the full corridor path for a given route.

        This uses a smarter algorithm:
        1. Get the ordered list of stops for this route
        2. For each consecutive pair of stops, find ALL stations that exist
           on ANY service between those points (the full corridor)
        3. Identify which of those corridor stations this service doesn't stop at

        This properly detects express services that skip intermediate stations.

        Args:
            route_code: Route identifier (e.g., "R026")

        Returns:
            Dict with:
                - route_code: The route code
                - operator: Operating company
                - route_type: Service type
                - stops: List of stations where the service stops
                - corridor: Full list of all stations on the corridor
                - skipped: List of stations on corridor but not stopped at
                - segment_details: Detailed info for each segment
        """
        if route_code not in self.routes:
            return None

        route = self.routes[route_code]
        stops = route.get('stations', [])

        if len(stops) < 2:
            return {
                'route_code': route_code,
                'operator': route.get('operator', 'Unknown'),
                'route_type': route.get('route_type', 'Unknown'),
                'stops': stops,
                'corridor': stops,
                'skipped': [],
                'segment_details': []
            }

        # For each segment, find all corridor stations
        all_corridor_stations = []
        segment_details = []

        for i in range(len(stops) - 1):
            origin = stops[i]
            destination = stops[i + 1]

            # Find all stations on ANY route between these points
            corridor_stations = self._find_corridor_stations(origin, destination)

            # Find which specific routes serve each station
            routes_via_station = defaultdict(list)
            for other_route_code, other_route_data in self.routes.items():
                if 'REMOVED' in other_route_data.get('route_type', ''):
                    continue

                other_stations = other_route_data.get('stations', [])
                try:
                    start_idx = other_stations.index(origin)
                    end_idx = other_stations.index(destination)

                    if start_idx < end_idx:
                        segment = other_stations[start_idx:end_idx + 1]
                        for station in segment:
                            if station not in [origin, destination]:
                                routes_via_station[station].append(other_route_code)
                except ValueError:
                    continue

            # Convert corridor stations to ordered list
            corridor_list = sorted(corridor_stations)

            segment_details.append({
                'from': origin,
                'to': destination,
                'corridor_stations': corridor_list,
                'intermediate_count': len(corridor_stations) - 2,  # Exclude origin and destination
                'routes_via_intermediate': dict(routes_via_station)
            })

            # Add to full corridor list
            if i == 0:
                all_corridor_stations.extend(corridor_list)
            else:
                # Skip the first station (already added)
                all_corridor_stations.extend([s for s in corridor_list if s != origin])

        # Remove duplicates while preserving order
        seen = set()
        corridor_ordered = []
        for station in all_corridor_stations:
            if station not in seen:
                seen.add(station)
                corridor_ordered.append(station)

        # Find skipped stations
        stops_set = set(stops)
        skipped = [station for station in corridor_ordered if station not in stops_set]

        return {
            'route_code': route_code,
            'operator': route.get('operator', 'Unknown'),
            'route_type': route.get('route_type', 'Unknown'),
            'origin': route.get('origin', stops[0]),
            'destination': route.get('destination', stops[-1]),
            'price': route.get('price', 'Unknown'),
            'travel_time': route.get('travel_time', {}),
            'stops': stops,
            'corridor': corridor_ordered,
            'skipped': skipped,
            'segment_details': segment_details
        }

    def format_corridor_report(self, corridor_data: Dict, verbose: bool = False) -> str:
        """
        Format corridor data into a human-readable report.

        Args:
            corridor_data: Output from calculate_route_corridor()
            verbose: If True, include detailed segment information

        Returns:
            Formatted string report
        """
        if not corridor_data:
            return "Route not found."

        lines = []
        lines.append(f"═══════════════════════════════════════════════════════")
        lines.append(f"Route {corridor_data['route_code']} Corridor Analysis")
        lines.append(f"═══════════════════════════════════════════════════════")
        lines.append(f"Operator: {corridor_data['operator']}")
        lines.append(f"Type: {corridor_data['route_type']}")
        lines.append(f"Origin: {corridor_data['origin']}")
        lines.append(f"Destination: {corridor_data['destination']}")
        lines.append(f"Price: {corridor_data['price']}")

        travel_time = corridor_data.get('travel_time', {})
        if travel_time:
            lines.append(f"Travel Time: Up {travel_time.get('up', 'N/A')} / Down {travel_time.get('down', 'N/A')}")

        lines.append("")
        lines.append(f"Stops at: {len(corridor_data['stops'])} stations")
        lines.append(f"Passes through: {len(corridor_data['corridor'])} stations total")
        lines.append(f"Skips: {len(corridor_data['skipped'])} stations")
        lines.append("")

        # Show the stops
        lines.append("🛑 STOPS (where the service calls):")
        for i, stop in enumerate(corridor_data['stops'], 1):
            lines.append(f"  {i:2d}. {stop}")

        # Show the full corridor
        if verbose:
            lines.append("")
            lines.append("🚂 FULL CORRIDOR (all stations passed):")
            for i, station in enumerate(corridor_data['corridor'], 1):
                if station in corridor_data['stops']:
                    lines.append(f"  {i:2d}. {station} ●")
                else:
                    lines.append(f"  {i:2d}. {station} (skip)")

        # Show skipped stations
        if corridor_data['skipped']:
            lines.append("")
            lines.append("⏭️  SKIPPED STATIONS (passed but not stopped at):")
            for i, station in enumerate(corridor_data['skipped'], 1):
                # Find position in corridor
                position = corridor_data['corridor'].index(station) + 1
                lines.append(f"  {i:2d}. {station} (position #{position} in corridor)")
        else:
            lines.append("")
            lines.append("⏭️  SKIPPED STATIONS: None (all-stations service)")

        # Show segment details if verbose
        if verbose and corridor_data.get('segment_details'):
            lines.append("")
            lines.append("📍 SEGMENT DETAILS:")
            for i, segment in enumerate(corridor_data['segment_details'], 1):
                lines.append(f"\n  Segment {i}: {segment['from']} → {segment['to']}")

                intermediate = [s for s in segment['corridor_stations']
                               if s not in [segment['from'], segment['to']]]

                if intermediate:
                    lines.append(f"  Corridor stations: {' → '.join(segment['corridor_stations'])}")
                    lines.append(f"  Intermediate stations: {len(intermediate)}")

                    # Show which routes serve each intermediate station
                    for station in intermediate:
                        routes = segment.get('routes_via_intermediate', {}).get(station, [])
                        if routes:
                            lines.append(f"    • {station}: served by {', '.join(routes[:5])}")
                else:
                    lines.append(f"  Direct connection (no intermediate stations)")

        return '\n'.join(lines)

    def get_skipped_stations(self, route_code: str) -> Optional[List[str]]:
        """
        Quick function to get just the skipped stations for a route.

        Args:
            route_code: Route identifier (e.g., "R026")

        Returns:
            List of skipped station names, or None if route not found
        """
        corridor = self.calculate_route_corridor(route_code)
        if corridor:
            return corridor['skipped']
        return None

    def compare_services(self, route_code1: str, route_code2: str) -> str:
        """
        Compare two services' corridors.

        Args:
            route_code1: First route code
            route_code2: Second route code

        Returns:
            Comparison report
        """
        c1 = self.calculate_route_corridor(route_code1)
        c2 = self.calculate_route_corridor(route_code2)

        if not c1 or not c2:
            return "One or both routes not found."

        lines = []
        lines.append(f"Comparing {route_code1} vs {route_code2}")
        lines.append(f"{'='*60}")
        lines.append(f"{route_code1}: {c1['operator']} - {c1['route_type']}")
        lines.append(f"  Stops: {len(c1['stops'])} | Corridor: {len(c1['corridor'])} | Skips: {len(c1['skipped'])}")
        lines.append(f"\n{route_code2}: {c2['operator']} - {c2['route_type']}")
        lines.append(f"  Stops: {len(c2['stops'])} | Corridor: {len(c2['corridor'])} | Skips: {len(c2['skipped'])}")

        # Find common skipped stations
        common_skipped = set(c1['skipped']) & set(c2['skipped'])
        if common_skipped:
            lines.append(f"\nBoth services skip: {', '.join(sorted(common_skipped))}")

        # Find unique skips
        unique1 = set(c1['skipped']) - set(c2['skipped'])
        unique2 = set(c2['skipped']) - set(c1['skipped'])

        if unique1:
            lines.append(f"\nOnly {route_code1} skips: {', '.join(sorted(unique1))}")
        if unique2:
            lines.append(f"Only {route_code2} skips: {', '.join(sorted(unique2))}")

        return '\n'.join(lines)


# CLI Interface
if __name__ == "__main__":
    import sys

    # Create calculator
    calc = RouteCorridorCalculator()

    # Check command line arguments
    if len(sys.argv) > 1:
        route_code = sys.argv[1]
        verbose = '--verbose' in sys.argv or '-v' in sys.argv

        # Handle comparison mode
        if len(sys.argv) > 2 and sys.argv[2] not in ['--verbose', '-v']:
            route_code2 = sys.argv[2]
            print(calc.compare_services(route_code, route_code2))
        else:
            # Single route analysis
            corridor = calc.calculate_route_corridor(route_code)
            if corridor:
                print(calc.format_corridor_report(corridor, verbose=verbose))
            else:
                print(f"Route {route_code} not found.")
                print(f"\nAvailable routes: {', '.join(sorted(list(calc.routes.keys())[:20]))}...")
    else:
        # Default: Show R026 example
        print("Stepford County Railway - Route Corridor Calculator")
        print("=" * 60)
        print("\nExample: Analyzing R026 (Regional One)\n")

        corridor = calc.calculate_route_corridor('R026')
        print(calc.format_corridor_report(corridor, verbose=True))

        print("\n" + "=" * 60)
        print("\nUsage:")
        print("  python3 route_corridor_calculator.py <ROUTE_CODE>")
        print("  python3 route_corridor_calculator.py <ROUTE_CODE> --verbose")
        print("  python3 route_corridor_calculator.py <ROUTE1> <ROUTE2>  # Compare")
        print("\nExamples:")
        print("  python3 route_corridor_calculator.py R026")
        print("  python3 route_corridor_calculator.py R078 --verbose")
        print("  python3 route_corridor_calculator.py R026 R035  # Compare services")
