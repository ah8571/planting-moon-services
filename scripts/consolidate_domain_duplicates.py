#!/usr/bin/env python3
"""
Consolidate entries for the same domain - merge webmetools.com entries
into existing entries and add webmetools.com to their listedOn sources.
"""

import json
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict

data_dir = Path(__file__).parent.parent / "data"

with open(data_dir / "guest-posts.json") as f:
    data = json.load(f)

posts = data["guestPosts"]
print(f"Starting with: {len(posts)} entries\n")

# Group by domain
domains = defaultdict(list)
for post in posts:
    try:
        domain = urlparse(post["url"]).netloc.lower().replace("www.", "")
        domains[domain].append(post)
    except:
        pass

# Find domains with multiple entries
consolidations = []
posts_to_remove = []

for domain, post_list in domains.items():
    if len(post_list) > 1:
        # Keep the entry with highest DR or best info
        # Handle None DR values by treating them as 0
        best = max(post_list, key=lambda p: ((p.get("dr") or 0), len(p.get("description", ""))))
        
        # Gather all sources from all entries for this domain
        all_sources = set()
        for post in post_list:
            all_sources.update(post.get("listedOn", []))
        
        # If webmetools.com is in the sources and best entry doesn't have it, add it
        if "webmetools.com" in all_sources and "webmetools.com" not in best.get("listedOn", []):
            best["listedOn"] = sorted(list(all_sources))
            consolidations.append((domain, best["name"], list(all_sources)))
            
            # Mark other entries for removal
            for post in post_list:
                if post != best:
                    posts_to_remove.append(post["id"])

# Remove duplicate entries
original_count = len(posts)
posts = [p for p in posts if p["id"] not in posts_to_remove]
removed = original_count - len(posts)

# Save back
data["guestPosts"] = posts
with open(data_dir / "guest-posts.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"=== Consolidation Summary ===")
print(f"Domains consolidated: {len(consolidations)}")
print(f"Entries removed: {removed}")
print(f"Final total: {len(posts)}")

print(f"\nExamples of consolidations:")
for domain, name, sources in consolidations[:10]:
    print(f"  • {name}: {sources}")

if len(consolidations) > 10:
    print(f"  ... and {len(consolidations) - 10} more")
