#!/usr/bin/env python3
"""
Stepford County Railway Pathfinder - Method 3 Implementation
Use this to find optimal routes with transfers for your Custom GPT
"""

import json
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Optional

def load_routes(json_file='stepford_routes_with_segment_minutes_ai_knowledge_base.json'):
    """Load route data from JSON file"""
    with open(json_file, 'r') as f:
        return json.load(f)

class RoutePathfinder:
    def __init__(self, routes_data):
        self.routes = routes_data['routes']
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build graph of station connections"""
        graph = defaultdict(list)

        for route_code, route_data in self.routes.items():
            # Skip removed routes
            if 'REMOVED' in route_data.get('route_type', ''):
                continue

            stations = route_data.get('stations', [])
            if len(stations) < 2:
                continue

            # Parse travel time
            time_str = route_data.get('travel_time', {}).get('up', '0 minutes')
            try:
                total_time = float(time_str.split()[0])
            except:
                total_time = 0

            # Estimate time per segment
            segments = len(stations) - 1
            time_per_segment = total_time / segments if segments > 0 else 0

            # Add BIDIRECTIONAL edges for consecutive stations
            # Trains can run in both directions!
            for i in range(len(stations) - 1):
                from_station = stations[i]
                to_station = stations[i + 1]

                # Forward direction (A → B)
                graph[from_station].append({
                    'to': to_station,
                    'time': time_per_segment,
                    'route': route_code,
                    'operator': route_data['operator'],
                    'type': route_data['route_type'],
                    'price': route_data['price'],
                    'total_route_time': total_time
                })

                # Reverse direction (B → A)
                graph[to_station].append({
                    'to': from_station,
                    'time': time_per_segment,
                    'route': route_code,
                    'operator': route_data['operator'],
                    'type': route_data['route_type'],
                    'price': route_data['price'],
                    'total_route_time': total_time
                })

        return graph

    def find_routes(self, start: str, end: str, max_transfers: int = 2):
        """
        Find all routes from start to end with up to max_transfers
        Returns sorted list of routes (best first)
        """
        # BFS to find all paths with optimizations
        queue = deque([(start, [start], [], None, 0, 0.0)])  # (station, path, routes_used, current_route, transfers, time)
        all_paths = []
        visited_states = set()
        best_time_by_transfers = {}  # Track best time for each transfer count

        while queue:
            current, path, routes_used, current_route, transfers, current_time = queue.popleft()

            # Early stopping: only prune if there's a route with SAME OR FEWER transfers that's faster
            should_prune = False
            for t in range(transfers + 1):  # Check all transfer counts <= current
                if t in best_time_by_transfers and current_time > best_time_by_transfers[t] * 1.5:
                    should_prune = True
                    break
            if should_prune:
                continue

            # Create state signature to avoid revisiting same situation
            state = (current, tuple(r['route'] for r in routes_used), transfers)
            if state in visited_states:
                continue
            visited_states.add(state)

            # Found destination
            if current == end:
                total_time = sum(r['time'] for r in routes_used)
                all_paths.append({
                    'time': total_time,
                    'transfers': transfers,
                    'path': path,
                    'routes': routes_used
                })
                # Update best time for this transfer count
                if transfers not in best_time_by_transfers or total_time < best_time_by_transfers[transfers]:
                    best_time_by_transfers[transfers] = total_time
                continue

            # Stop if too many transfers or path too long or visited same station twice
            if transfers > max_transfers or len(path) > 15:
                continue

            # Avoid revisiting same station (prevents loops)
            visited_in_path = set(path)

            # Explore neighbors
            for edge in self.graph.get(current, []):
                next_station = edge['to']

                # Skip if already visited in this path
                if next_station in visited_in_path:
                    continue

                # Check if route changed (transfer)
                new_transfers = transfers
                if current_route is not None and edge['route'] != current_route:
                    new_transfers += 1

                if new_transfers <= max_transfers:
                    new_path = path + [next_station]
                    new_routes = routes_used + [edge]
                    new_time = current_time + edge['time']
                    queue.append((next_station, new_path, new_routes, edge['route'], new_transfers, new_time))

            # Limit results to prevent memory explosion
            if len(all_paths) > 1000:
                break

        # Sort: fewer transfers first, then by time
        all_paths.sort(key=lambda x: (x['transfers'], x['time']))
        return all_paths[:100]  # Return top 100 routes max

    def format_route(self, route_info: Dict, verbose: bool = False) -> str:
        """Format a route for display"""
        transfers = route_info['transfers']
        time = route_info['time']
        path = route_info['path']
        routes_used = route_info['routes']

        # Build route segments
        segments = []
        current_route = None
        segment_stations = []

        for i, edge in enumerate(routes_used):
            if edge['route'] != current_route:
                if current_route is not None:
                    segments.append({
                        'route': current_route,
                        'stations': segment_stations,
                        'operator': prev_edge['operator'],
                        'type': prev_edge['type'],
                        'price': prev_edge['price']
                    })
                current_route = edge['route']
                segment_stations = [path[i]]
            segment_stations.append(path[i + 1])
            prev_edge = edge

        if current_route is not None:
            segments.append({
                'route': current_route,
                'stations': segment_stations,
                'operator': routes_used[-1]['operator'],
                'type': routes_used[-1]['type'],
                'price': routes_used[-1]['price']
            })

        # Format output
        output = []
        transfer_text = "direct" if transfers == 0 else f"{transfers} transfer{'s' if transfers != 1 else ''}"
        output.append(f"⏱️ {time:.1f} minutes ({transfer_text})")

        for i, segment in enumerate(segments, 1):
            route_line = f"  {segment['route']} ({segment['operator']}): {' → '.join(segment['stations'])}"
            if verbose:
                route_line += f"\n     Type: {segment['type']} | Price: {segment['price']}"
            output.append(route_line)

        return '\n'.join(output)

    def get_best_routes(self, start: str, end: str, top_n: int = 5, max_transfers: int = 2) -> str:
        """Get formatted string of best routes"""
        routes = self.find_routes(start, end, max_transfers)

        if not routes:
            return f"❌ No routes found from {start} to {end}"

        output = [f"🚄 Routes from {start} to {end}:\n"]
        output.append(f"Found {len(routes)} possible routes. Showing top {min(top_n, len(routes))}:\n")

        for i, route in enumerate(routes[:top_n], 1):
            output.append(f"{i}. {self.format_route(route, verbose=True)}\n")

        return '\n'.join(output)

# CLI Interface
if __name__ == "__main__":
    import sys

    # Load data
    data = load_routes()
    pathfinder = RoutePathfinder(data)

    # Check command line arguments
    if len(sys.argv) >= 3:
        start = sys.argv[1]
        end = sys.argv[2]
        top_n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        max_transfers = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    else:
        # Default example
        start = "Benton"
        end = "Llyn-by-the-Sea"
        top_n = 5
        max_transfers = 2

    print(pathfinder.get_best_routes(start, end, top_n, max_transfers))
