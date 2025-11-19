import sys
sys.path.append(r'C:\Users\sydne\Documents\GitHub\edw\custom_gpt_upload')

import station_knowledge_helper as skh

stations = skh.load_station_knowledge(
    r'C:\Users\sydne\Documents\GitHub\edw\custom_gpt_upload\scr_stations_part1.md',
    r'C:\Users\sydne\Documents\GitHub\edw\custom_gpt_upload\scr_stations_part2.md'
)

print("Stations with 'Benton Bridge':")
for k in stations.keys():
    if 'Benton Bridge' in k or 'benton bridge' in k.lower():
        print(f"  '{k}'")
