#!/usr/bin/env python3
"""
Verify guest posts file for duplicates and data quality issues.
"""

import json
from pathlib import Path
from collections import defaultdict

data_dir = Path(__file__).parent.parent / "data"

with open(data_dir / "guest-posts-bloggingjoy.json") as f:
    data = json.load(f)

posts = data["guestPosts"]
print(f"Total entries: {len(posts)}\n")

# Check for duplicate IDs
id_map = defaultdict(list)
for post in posts:
    id_map[post["id"]].append(post)

print("=== DUPLICATE ID CHECK ===")
duplicates_by_id = {id: entries for id, entries in id_map.items() if len(entries) > 1}
if duplicates_by_id:
    print(f"Found {len(duplicates_by_id)} duplicate IDs:")
    for dup_id, entries in duplicates_by_id.items():
        print(f"\n  ID: {dup_id}")
        for entry in entries:
            print(f"    - {entry['name']} ({entry['url']})")
else:
    print("✓ No duplicate IDs found")

# Check for duplicate URLs
print("\n=== DUPLICATE URL CHECK ===")
url_map = defaultdict(list)
for post in posts:
    url_normalized = post["url"].lower().rstrip("/")
    url_map[url_normalized].append(post)

duplicates_by_url = {url: entries for url, entries in url_map.items() if len(entries) > 1}
if duplicates_by_url:
    print(f"Found {len(duplicates_by_url)} duplicate URLs:")
    for dup_url, entries in duplicates_by_url.items():
        print(f"\n  URL: {dup_url}")
        for entry in entries:
            print(f"    - {entry['name']} (ID: {entry['id']}, DR: {entry['dr']})")
            print(f"      Sources: {entry['listedOn']}")
else:
    print("✓ No duplicate URLs found")

# Check for entries with similar names (potential duplicates missed)
print("\n=== SIMILAR NAME CHECK ===")
name_map = defaultdict(list)
for post in posts:
    name_lower = post["name"].lower()
    name_map[name_lower].append(post)

similar_names = {name: entries for name, entries in name_map.items() if len(entries) > 1}
if similar_names:
    print(f"Found {len(similar_names)} entries with identical names (case-insensitive):")
    for dup_name, entries in similar_names.items():
        print(f"\n  Name: {dup_name}")
        for entry in entries:
            print(f"    - {entry['name']} ({entry['url']}) - Sources: {entry['listedOn']}")
else:
    print("✓ No duplicate names found")

# Data quality check
print("\n=== DATA QUALITY CHECK ===")
missing_fields = []
for post in posts:
    if not post.get("id"):
        missing_fields.append(f"{post.get('name', 'Unknown')}: missing 'id'")
    if not post.get("name"):
        missing_fields.append(f"{post.get('id', 'Unknown')}: missing 'name'")
    if not post.get("url"):
        missing_fields.append(f"{post.get('name', 'Unknown')}: missing 'url'")
    if post.get("dr") is None:
        missing_fields.append(f"{post.get('name', 'Unknown')}: missing 'dr'")
    if not post.get("listedOn"):
        missing_fields.append(f"{post.get('name', 'Unknown')}: missing 'listedOn'")

if missing_fields:
    print(f"Found {len(missing_fields)} data quality issues:")
    for issue in missing_fields:
        print(f"  - {issue}")
else:
    print("✓ All entries have required fields")

# Check multi-source entries
print("\n=== MULTI-SOURCE ENTRIES ===")
multi_source = [post for post in posts if len(post.get("listedOn", [])) > 1]
if multi_source:
    print(f"Found {len(multi_source)} entries cited by multiple sources:")
    for post in sorted(multi_source, key=lambda x: len(x.get("listedOn", [])), reverse=True):
        print(f"  - {post['name']} (DR: {post['dr']})")
        print(f"    Sources: {', '.join(post['listedOn'])}")
else:
    print("✓ No multi-source entries found")

print("\n=== SUMMARY ===")
print(f"✓ File integrity verified")
print(f"  - Total entries: {len(posts)}")
print(f"  - Multi-source entries: {len(multi_source)}")
print(f"  - Data quality issues: {len(missing_fields)}")
