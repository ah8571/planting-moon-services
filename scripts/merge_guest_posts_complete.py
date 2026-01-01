#!/usr/bin/env python3
"""
Merge guest post sources (bloggingjoy and rhinorank) into one master file.
Consolidates duplicates by adding sources to listedOn array.
"""

import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data"

# Load existing sources
with open(data_dir / "guest-posts-bloggingjoy.json") as f:
    bloggingjoy_data = json.load(f)

with open(data_dir / "guest-posts-rhinorank.json") as f:
    rhinorank_data = json.load(f)

# Create map for quick ID lookups
merged_map = {}
for item in bloggingjoy_data["guestPosts"]:
    merged_map[item["id"]] = item

# Merge rhinorank entries
duplicates_found = 0
new_entries = 0

for rhinorank_item in rhinorank_data["guestPosts"]:
    item_id = rhinorank_item["id"]
    
    if item_id in merged_map:
        # Duplicate found - add rhinorank to listedOn if not already there
        if "rhinorank.com" not in merged_map[item_id]["listedOn"]:
            merged_map[item_id]["listedOn"].append("rhinorank.com")
            duplicates_found += 1
            print(f"✓ Updated '{merged_map[item_id]['name']}' - added rhinorank.com to sources")
    else:
        # New entry
        merged_map[item_id] = rhinorank_item
        new_entries += 1
        print(f"✓ Added new entry: '{rhinorank_item['name']}'")

# Convert map back to sorted list
merged_posts = sorted(merged_map.values(), key=lambda x: x.get("dr", 0), reverse=True)

# Create merged data structure
merged_data = {
    "guestPosts": merged_posts,
    "niches": bloggingjoy_data.get("niches", [])
}

# Update niches from rhinorank if they have different ones
if "niches" in rhinorank_data:
    for niche in rhinorank_data["niches"]:
        if niche not in merged_data["niches"]:
            merged_data["niches"].append(niche)
merged_data["niches"].sort()

# Save to bloggingjoy file (replacing it)
output_file = data_dir / "guest-posts-bloggingjoy.json"
with open(output_file, "w") as f:
    json.dump(merged_data, f, indent=2)

print(f"\n=== Merge Summary ===")
print(f"Total entries: {len(merged_posts)}")
print(f"Duplicates consolidated: {duplicates_found}")
print(f"New entries added: {new_entries}")
print(f"Total niches: {len(merged_data['niches'])}")
print(f"\nMerged file saved to: {output_file}")

# Delete rhinorank file since it's now merged
rhinorank_file = data_dir / "guest-posts-rhinorank.json"
if rhinorank_file.exists():
    rhinorank_file.unlink()
    print(f"Deleted separate rhinorank file: {rhinorank_file}")
