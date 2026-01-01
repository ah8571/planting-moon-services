#!/usr/bin/env python3
"""
Final verification of consolidated guest-posts.json
"""

import json
from pathlib import Path
from collections import defaultdict

data_dir = Path(__file__).parent.parent / "data"

with open(data_dir / "guest-posts.json") as f:
    data = json.load(f)

posts = data["guestPosts"]
print(f"Total entries: {len(posts)}\n")

# Check for duplicate URLs
url_map = defaultdict(list)
for post in posts:
    url_normalized = post["url"].lower().rstrip("/")
    url_map[url_normalized].append(post)

duplicates_by_url = {url: entries for url, entries in url_map.items() if len(entries) > 1}

if duplicates_by_url:
    print(f"⚠️  Found {len(duplicates_by_url)} duplicate URLs to consolidate:\n")
    for dup_url, entries in sorted(duplicates_by_url.items()):
        print(f"URL: {dup_url}")
        for entry in entries:
            print(f"  - ID: {entry['id']}, Name: {entry['name']}, Sources: {entry['listedOn']}")
        print()
else:
    print("✓ No duplicate URLs found")

# Check multi-source entries
multi_source = [post for post in posts if len(post.get("listedOn", [])) > 1]
print(f"\n✓ Multi-source entries: {len(multi_source)}")
for post in sorted(multi_source, key=lambda x: x.get("dr", 0), reverse=True)[:10]:
    print(f"  - {post['name']} (DR: {post['dr']}): {post['listedOn']}")
