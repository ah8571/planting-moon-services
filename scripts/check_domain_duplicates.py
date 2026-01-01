#!/usr/bin/env python3
"""
Deep duplicate check - look for same domain but different URLs.
"""

import json
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict

data_dir = Path(__file__).parent.parent / "data"

with open(data_dir / "guest-posts.json") as f:
    data = json.load(f)

posts = data["guestPosts"]

# Group by domain
domains = defaultdict(list)
for post in posts:
    try:
        domain = urlparse(post["url"]).netloc.lower().replace("www.", "")
        domains[domain].append(post)
    except:
        pass

# Find domains with multiple entries
duplicates = {d: posts for d, posts in domains.items() if len(posts) > 1}
print(f"Domains with multiple URLs: {len(duplicates)}\n")

for domain, post_list in sorted(duplicates.items()):
    if len(post_list) <= 3:  # Only show reasonable duplicates
        sources = [p.get("listedOn", []) for p in post_list]
        all_sources = set()
        for s in sources:
            all_sources.update(s)
        
        print(f"{domain}:")
        for p in post_list:
            print(f"  • {p['name']}: {p['url']} ({p.get('listedOn', [])})")
        print()

print(f"\nTotal entries: {len(posts)}")
print(f"Unique domains: {len(domains)}")
