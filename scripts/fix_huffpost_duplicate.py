#!/usr/bin/env python3
"""
Fix duplicate HuffPost entries by consolidating into one.
"""

import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data"

with open(data_dir / "guest-posts-bloggingjoy.json") as f:
    data = json.load(f)

posts = data["guestPosts"]

# Find and consolidate HuffPost duplicates
huffpost_entries = [p for p in posts if p["url"] == "https://www.huffpost.com"]
print(f"Found {len(huffpost_entries)} entries for HuffPost")

if len(huffpost_entries) == 2:
    # Keep the one from bloggingjoy (originally from that source)
    # Add rhinorank.com to its sources
    huffpost_bloggingjoy = next((p for p in huffpost_entries if "bloggingjoy.com" in p["listedOn"]), None)
    huffpost_rhinorank = next((p for p in huffpost_entries if "rhinorank.com" in p["listedOn"]), None)
    
    if huffpost_bloggingjoy and huffpost_rhinorank:
        # Merge sources
        if "rhinorank.com" not in huffpost_bloggingjoy["listedOn"]:
            huffpost_bloggingjoy["listedOn"].append("rhinorank.com")
        
        # Remove the rhinorank duplicate
        posts.remove(huffpost_rhinorank)
        
        print(f"✓ Consolidated HuffPost:")
        print(f"  Kept: {huffpost_bloggingjoy['name']} (ID: {huffpost_bloggingjoy['id']})")
        print(f"  Merged sources: {huffpost_bloggingjoy['listedOn']}")
        print(f"  Removed: {huffpost_rhinorank['name']} (ID: {huffpost_rhinorank['id']})")

# Save back
data["guestPosts"] = posts
with open(data_dir / "guest-posts-bloggingjoy.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"\nFile saved. New total: {len(posts)} entries")
