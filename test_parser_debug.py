#!/usr/bin/env python3
"""
Debug test for Services table parsing
"""

import re

# Sample line from Port Benton Services table
test_lines = [
    "1 Benton R010 R013 to Greenslade Morganstown Docks R015 R120 R137 to Morganstown",
    "2-3 Morganstown Docks R010 to Newry Benton R013 R015 to Benton R120 to Newry Harbour R137 to Stepford Victoria",
    "3 Benton R002 to Stepford Central Terminus ( Benton via loop ) R006 to Stepford Victoria R032 to Willowfield R047 to St Helens Bridge"
]

def test_extraction(line):
    print(f"\nTesting line: {line[:80]}...")

    # Better approach: Find patterns of "R### R### ... to Destination" as complete units
    # Pattern: (one or more route codes) followed by "to" followed by (destination name: 1-3 words)
    # Capture destination but stop before next route code or specific markers
    pattern = r'((?:R\d+\s+)+)to\s+([A-Z][\w\s\-]+?)(?=\s+R\d+|\s+Terminus|\s+\(|$)'

    matches = list(re.finditer(pattern, line))

    print(f"  Found {len(matches)} route->destination patterns:")
    for i, match in enumerate(matches):
        routes_text = match.group(1).strip()
        dest = match.group(2).strip()

        # Clean destination: intelligently extract station name
        # Most stations are 1-2 words, some are 3 (St Helens Bridge, Airport Terminal 2, etc.)
        dest_words = dest.split()

        # If first word is a common prefix, take 2-3 words
        if dest_words[0] in ['St', 'Airport', 'Upper', 'West', 'East', 'New', 'Port', 'Stepford']:
            if len(dest_words) > 3:
                dest_cleaned = ' '.join(dest_words[:3])
            else:
                dest_cleaned = dest
        # Otherwise, take first word only (safest guess)
        else:
            dest_cleaned = dest_words[0]

        routes = re.findall(r'R\d+', routes_text)

        print(f"    {i+1}. Routes: {routes} -> Destination: '{dest}' -> Cleaned: '{dest_cleaned}'")

for line in test_lines:
    test_extraction(line)
