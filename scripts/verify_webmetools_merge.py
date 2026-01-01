#!/usr/bin/env python3
"""
Verify webmetools merge - check for duplicates and data quality.
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
urls = defaultdict(list)
for post in posts:
    url_norm = post["url"].lower().rstrip("/")
    urls[url_norm].append(post)

duplicates = {url: posts for url, posts in urls.items() if len(posts) > 1}
if duplicates:
    print(f"⚠️  Found {len(duplicates)} duplicate URLs:")
    for url, post_list in list(duplicates.items())[:3]:
        print(f"  URL: {url}")
        for p in post_list:
            print(f"    - {p['name']} (Sources: {p['listedOn']})")
else:
    print("✓ No duplicate URLs found")

# Check multi-source entries with webmetools
multi_source = [p for p in posts if len(p.get("listedOn", [])) > 1]
print(f"\n✓ Multi-source entries: {len(multi_source)}")

webmetools_multi = [p for p in multi_source if "webmetools.com" in p.get("listedOn", [])]
print(f"  With webmetools.com: {len(webmetools_multi)}")
if webmetools_multi:
    print(f"  Examples: {', '.join(p['name'] for p in webmetools_multi[:5])}")

# Check webmetools entries
webmetools_entries = [p for p in posts if p.get("listedOn") == ["webmetools.com"]]
print(f"\nWebmeTools-only entries: {len(webmetools_entries)}")

# Data quality
missing_fields = []
for post in posts:
    required = ["id", "name", "url", "dr", "niche", "submissionType", "listedOn"]
    if not all(k in post for k in required):
        missing_fields.append(post["name"])

if missing_fields:
    print(f"\n⚠️  Entries with missing required fields: {len(missing_fields)}")
    print(f"  Examples: {', '.join(missing_fields[:3])}")
else:
    print(f"\n✓ All entries have required fields")

# DR statistics
drs = [p.get("dr", 0) for p in posts]
print(f"\nDR Statistics:")
print(f"  Min: {min(drs)}")
print(f"  Max: {max(drs)}")
print(f"  Avg: {sum(drs) / len(drs):.1f}")

# Entries by source
sources = defaultdict(int)
for post in posts:
    for source in post.get("listedOn", []):
        sources[source] += 1

print(f"\nSources by entry count:")
for source in sorted(sources.keys(), key=lambda x: sources[x], reverse=True)[:5]:
    print(f"  {source}: {sources[source]}")
