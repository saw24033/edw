#!/usr/bin/env python3
"""
Test parsing actual Port Benton Services section
"""

import sys
sys.path.append('C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload')

import station_knowledge_helper as skh
import re

# Load stations
part1 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part1.md"
part2 = "C:\\Users\\sydne\\Documents\\GitHub\\edw\\custom_gpt_upload\\scr_stations_part2.md"

print("Loading stations...")
stations = skh.load_station_knowledge(part1, part2)

if "Port Benton" not in stations:
    print("ERROR: Port Benton not found!")
    sys.exit(1)

port_benton = stations["Port Benton"]
content = port_benton['full_content']

print("\n1. Looking for Services section...")
services_section = re.search(r'Services\s*\[\s*\](.+?)(?:Station announcements|History|Trivia|$)',
                            content, re.DOTALL | re.IGNORECASE)

if not services_section:
    print("   ERROR: Services section not found!")
    print("\n   Content preview (first 500 chars):")
    print(content[:500])
else:
    services_text = services_section.group(1)
    print(f"   Found Services section ({len(services_text)} chars)")
    print(f"\n2. Services section content (first 800 chars):")
    print(services_text[:800])

    print("\n3. Testing line parsing...")
    lines = services_text.split('\n')
    print(f"   Total lines: {len(lines)}")

    for i, line in enumerate(lines[:20]):  # Show first 20 lines
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if 'Platform' in line or '---' in line:
            print(f"   Line {i}: [HEADER] {line_stripped[:60]}")
            continue

        # Check if it starts with platform number
        plat_match = re.match(r'^(\d+(?:-\d+)?)\s+', line_stripped)
        if plat_match:
            print(f"   Line {i}: [PLATFORM {plat_match.group(1)}] {line_stripped[:60]}")
        else:
            print(f"   Line {i}: [CONTINUATION] {line_stripped[:60]}")
