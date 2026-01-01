#!/usr/bin/env python3
"""
Merge guest-posts-bloggingjoy.json into guest-posts.json and consolidate duplicates.
"""

import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data"

# Load both files
with open(data_dir / "guest-posts.json") as f:
    main_data = json.load(f)

with open(data_dir / "guest-posts-bloggingjoy.json") as f:
    bloggingjoy_data = json.load(f)

main_posts = main_data["guestPosts"]
bloggingjoy_posts = bloggingjoy_data["guestPosts"]

print(f"Main file: {len(main_posts)} entries")
print(f"BloggingJoy file: {len(bloggingjoy_posts)} entries")

# Create map for quick lookups by URL
url_map = {}
for post in main_posts:
    url_normalized = post["url"].lower().rstrip("/")
    url_map[url_normalized] = post

# Merge bloggingjoy entries
duplicates_found = 0
new_entries = 0

for bj_post in bloggingjoy_posts:
    url_normalized = bj_post["url"].lower().rstrip("/")
    
    if url_normalized in url_map:
        # Duplicate found - add bloggingjoy.com to sources if not already there
        existing_post = url_map[url_normalized]
        if "bloggingjoy.com" not in existing_post["listedOn"]:
            existing_post["listedOn"].append("bloggingjoy.com")
            duplicates_found += 1
            print(f"✓ Added bloggingjoy.com to: {existing_post['name']}")
    else:
        # New entry
        main_posts.append(bj_post)
        url_map[url_normalized] = bj_post
        new_entries += 1
        print(f"✓ Added new entry: {bj_post['name']}")

# Sort by DR descending
main_posts.sort(key=lambda x: x.get("dr", 0), reverse=True)

# Consolidate niches
all_niches = set()
for post in main_posts:
    all_niches.update(post.get("niche", []))
if "niches" in bloggingjoy_data:
    all_niches.update(bloggingjoy_data["niches"])

main_data["guestPosts"] = main_posts
if all_niches:
    main_data["niches"] = sorted(list(all_niches))

# Save back to main file
with open(data_dir / "guest-posts.json", "w") as f:
    json.dump(main_data, f, indent=2)

print(f"\n=== Merge Summary ===")
print(f"Total entries in consolidated file: {len(main_posts)}")
print(f"Duplicates consolidated: {duplicates_found}")
print(f"New entries added: {new_entries}")
print(f"Consolidated file saved to: {data_dir / 'guest-posts.json'}")

# Delete separate bloggingjoy file
bloggingjoy_file = data_dir / "guest-posts-bloggingjoy.json"
if bloggingjoy_file.exists():
    bloggingjoy_file.unlink()
    print(f"Deleted separate file: {bloggingjoy_file}")
