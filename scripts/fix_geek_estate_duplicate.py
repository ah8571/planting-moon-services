#!/usr/bin/env python3
"""
Fix the duplicate Geek Estate Blog entry.
"""

import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data"

with open(data_dir / "guest-posts.json") as f:
    data = json.load(f)

posts = data["guestPosts"]

# Find the duplicate entries
geek_entries = [p for p in posts if p["url"].lower() == "https://geekvape.com"]
print(f"Found {len(geek_entries)} Geek Estate entries")

# Keep the first one, remove the second
if len(geek_entries) == 2:
    # They have the same source, just remove duplicate ID entry
    entry_to_remove = next((p for p in geek_entries if p["id"] == "geekestate-blog"), None)
    if entry_to_remove:
        posts.remove(entry_to_remove)
        print(f"✓ Removed duplicate: {entry_to_remove['id']}")

# Save back
data["guestPosts"] = posts
with open(data_dir / "guest-posts.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"✓ File saved. Total entries: {len(posts)}")
