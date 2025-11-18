#!/usr/bin/env python3
"""
Test script for improved platform parser in station_knowledge_helper.py v3.3

Verifies that directional platform extraction works correctly.
"""

import sys
sys.path.append('C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload')

import importlib
import station_knowledge_helper as skh

# Debug: Print which file was loaded
print(f"DEBUG: Loaded station_knowledge_helper from: {skh.__file__}")
print(f"DEBUG: Available attributes: {[a for a in dir(skh) if 'build' in a.lower()]}")

# Force reload to get latest version
skh = importlib.reload(skh)
print(f"DEBUG: After reload, available attributes: {[a for a in dir(skh) if 'build' in a.lower()]}")

def test_port_benton_directional_platforms():
    """Test that Port Benton R013 directional platforms are extracted correctly."""

    print("=" * 70)
    print("Testing Port Benton Directional Platform Extraction")
    print("=" * 70)

    # Load station knowledge
    part1 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part1.md"
    part2 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part2.md"

    print("\n1. Loading station knowledge files...")
    stations = skh.load_station_knowledge(part1, part2)

    if "Port Benton" not in stations:
        print("[ERROR] Port Benton not found in stations dictionary")
        return

    print("[OK] Port Benton loaded successfully")

    # Get Port Benton data
    port_benton = stations["Port Benton"]

    # Build directional_map by calling the parser function
    print("\n2. Building directional_map using build_directional_platform_map()...")
    try:
        directional_map = skh.build_directional_platform_map(port_benton)
    except Exception as e:
        print(f"   [ERROR] Exception while building map: {e}")
        import traceback
        traceback.print_exc()
        directional_map = None

    print(f"   DEBUG: directional_map type: {type(directional_map)}, len: {len(directional_map) if directional_map else 0}")

    if directional_map:
        print(f"[OK] directional_map built with {len(directional_map)} entries")

        # Look for R013 entries
        r013_entries = {k: v for k, v in directional_map.items() if k[0] == 'R013'}

        if r013_entries:
            print(f"\n3. Found {len(r013_entries)} R013 directional entries:")
            for (route, destination), platforms in r013_entries.items():
                print(f"   {route} -> {destination}: Platforms {', '.join(platforms)}")

            # Verify expected mappings
            print("\n4. Verification:")

            # Check R013 to Benton (should be Platforms 2-3)
            found_benton = False
            for (route, dest), platforms in r013_entries.items():
                if 'Benton' in dest and dest.strip() == 'Benton':
                    found_benton = True
                    if '2-3' in platforms:
                        print(f"   [OK] R013 -> Benton: Platforms {', '.join(platforms)} (CORRECT)")
                    else:
                        print(f"   [FAIL] R013 -> Benton: Platforms {', '.join(platforms)} (EXPECTED: 2-3)")

            if not found_benton:
                print("   [FAIL] R013 -> Benton not found in directional_map")

            # Check R013 to Greenslade (should be Platform 1)
            found_greenslade = False
            for (route, dest), platforms in r013_entries.items():
                if 'Greenslade' in dest:
                    found_greenslade = True
                    if '1' in platforms:
                        print(f"   [OK] R013 -> Greenslade: Platforms {', '.join(platforms)} (CORRECT)")
                    else:
                        print(f"   [FAIL] R013 -> Greenslade: Platforms {', '.join(platforms)} (EXPECTED: 1)")

            if not found_greenslade:
                print("   [FAIL] R013 -> Greenslade not found in directional_map")

        else:
            print("   [FAIL] No R013 entries found in directional_map")
    else:
        print("   [FAIL] Failed to build directional_map")

    # Test get_route_context with directional info
    print("\n5. Testing get_route_context() with next_station parameter...")

    # Test R013 to Benton (eastbound - should be Platforms 2-3)
    context_eastbound = skh.get_route_context(
        "Port Benton",
        "Stepford Connect",  # R013 is Stepford Connect
        stations,
        route_code="R013",
        next_station="Benton"
    )

    print("\n   R013 -> Benton (eastbound):")
    if 'departure_platforms' in context_eastbound:
        platform_info = context_eastbound['departure_platforms']
        print(f"   Departure platform info: {platform_info}")
        if '2-3' in str(platform_info):
            print(f"   [OK] Correct directional platform!")
        else:
            print(f"   [FAIL] Platform info incorrect (expected: Platforms 2-3)")
    else:
        print(f"   [FAIL] No departure_platforms in context. Keys: {list(context_eastbound.keys())}")

    # Test R013 to Greenslade (westbound - should be Platform 1)
    context_westbound = skh.get_route_context(
        "Port Benton",
        "Stepford Connect",
        stations,
        route_code="R013",
        next_station="Morganstown Docks"  # Next stop westbound
    )

    print("\n   R013 -> Morganstown Docks (westbound):")
    if 'departure_platforms' in context_westbound:
        platform_info = context_westbound['departure_platforms']
        print(f"   Departure platform info: {platform_info}")
        if '1' in str(platform_info):
            print(f"   [OK] Correct directional platform!")
        else:
            print(f"   [WARN] Platform info might be incorrect (expected: Platform 1)")
    else:
        print(f"   [FAIL] No departure_platforms in context. Keys: {list(context_westbound.keys())}")

    print("\n" + "=" * 70)
    print("Test Complete")
    print("=" * 70)

if __name__ == "__main__":
    test_port_benton_directional_platforms()
