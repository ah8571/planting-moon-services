#!/usr/bin/env python3
"""
Merge outreachmonks.com guest posting sites with DR values into guest-posts.json
Handles duplicate URL consolidation with source attribution.
"""

import json
from pathlib import Path
from urllib.parse import urlparse

data_dir = Path(__file__).parent.parent / "data"

# Load existing guest posts
with open(data_dir / "guest-posts.json") as f:
    main_data = json.load(f)

main_posts = main_data["guestPosts"]
print(f"Main file: {len(main_posts)} entries")

# Outreachmonks.com sites with DR values
outreachmonks_entries = [
    {"name": "ClickUp", "url": "https://clickup.com", "dr": 87, "niche": ["Productivity", "Project Management"]},
    {"name": "MobileAppDaily", "url": "https://www.mobileappdaily.com", "dr": 73, "niche": ["Mobile Apps", "Technology"]},
    {"name": "Entrepreneur", "url": "https://www.entrepreneur.com", "dr": 91, "niche": ["Entrepreneurship", "Business"]},
    {"name": "Techopedia", "url": "https://www.techopedia.com", "dr": 88, "niche": ["Technology", "IT"]},
    {"name": "OpenSource", "url": "https://opensource.com", "dr": 83, "niche": ["Open Source", "Technology"]},
    {"name": "Outbrain", "url": "https://www.outbrain.com", "dr": 92, "niche": ["Content Marketing", "Advertising"]},
    {"name": "Wakelet", "url": "https://wakelet.com", "dr": 85, "niche": ["Content Curation", "Social Media"]},
    {"name": "Edutopia", "url": "https://www.edutopia.org", "dr": 84, "niche": ["Education", "Teaching"]},
    {"name": "Clutch", "url": "https://clutch.co", "dr": 90, "niche": ["B2B", "Agencies"]},
    {"name": "HackerNoon", "url": "https://hackernoon.com", "dr": 88, "niche": ["Technology", "Programming"]},
    {"name": "YourStory", "url": "https://yourstory.com", "dr": 86, "niche": ["Startups", "Entrepreneurship"]},
    {"name": "Cloudways", "url": "https://www.cloudways.com", "dr": 90, "niche": ["Web Hosting", "Technology"]},
    {"name": "DataScienceCentral", "url": "https://www.datasciencecentral.com", "dr": 76, "niche": ["Data Science", "AI"]},
    {"name": "Fylehq", "url": "https://www.fylehq.com", "dr": 71, "niche": ["Expense Management", "SaaS"]},
    {"name": "PageFly", "url": "https://pagefly.io", "dr": 78, "niche": ["Shopify", "eCommerce"]},
    {"name": "Learn.g2", "url": "https://learn.g2.com", "dr": 91, "niche": ["Learning", "Software"]},
    {"name": "FinancesOnline", "url": "https://financesonline.com", "dr": 87, "niche": ["Finance", "SaaS Reviews"]},
    {"name": "Keyhole", "url": "https://keyhole.co", "dr": 78, "niche": ["Social Media", "Analytics"]},
    {"name": "SurveySparrow", "url": "https://www.surveysparrow.com", "dr": 80, "niche": ["Surveys", "Marketing"]},
    {"name": "Visme", "url": "https://www.visme.co", "dr": 86, "niche": ["Design", "Infographics"]},
    {"name": "ColibriWP", "url": "https://colibri.wp.com", "dr": 91, "niche": ["WordPress", "Web Design"]},
    {"name": "Mashable", "url": "https://mashable.com", "dr": 91, "niche": ["Technology", "Culture"]},
    {"name": "DZone", "url": "https://dzone.com", "dr": 84, "niche": ["Technology", "Development"]},
    {"name": "Recruitee", "url": "https://recruitee.com", "dr": 88, "niche": ["HR Tech", "Recruiting"]},
    {"name": "WPExplorer", "url": "https://www.wpexplorer.com", "dr": 83, "niche": ["WordPress", "Themes"]},
    {"name": "Mitel", "url": "https://www.mitel.com", "dr": 79, "niche": ["Telecommunications", "Business"]},
    {"name": "DevriX", "url": "https://devrix.com", "dr": 76, "niche": ["WordPress", "Development"]},
    {"name": "Front", "url": "https://frontapp.com", "dr": 80, "niche": ["Collaboration", "Messaging"]},
    {"name": "Broadcom", "url": "https://www.broadcom.com", "dr": 90, "niche": ["Technology", "Infrastructure"]},
    {"name": "Flock", "url": "https://flock.com", "dr": 77, "niche": ["Team Communication", "Messaging"]},
]

print(f"Outreachmonks entries: {len(outreachmonks_entries)}\n")

# Create map of existing posts by normalized URL
def normalize_url(url):
    return url.lower().rstrip("/")

url_map = {}
for post in main_posts:
    url_norm = normalize_url(post["url"])
    url_map[url_norm] = post

# Merge outreachmonks entries
duplicates_found = 0
new_entries = 0
updated_entries = []
duplicate_list = []

for om_entry in outreachmonks_entries:
    url_norm = normalize_url(om_entry["url"])
    
    if url_norm in url_map:
        # Duplicate found - add source to existing entry
        existing_post = url_map[url_norm]
        
        # Update DR if new entry has higher DR
        if om_entry["dr"] and (existing_post.get("dr") is None or om_entry["dr"] > existing_post.get("dr", 0)):
            existing_post["dr"] = om_entry["dr"]
        
        # Add source if not already there
        if "outreachmonks.com" not in existing_post["listedOn"]:
            existing_post["listedOn"].append("outreachmonks.com")
            duplicates_found += 1
            updated_entries.append((existing_post["name"], existing_post["dr"]))
            duplicate_list.append(f"{om_entry['name']} → {existing_post['name']}")
    else:
        # New entry - create JSON object with proper structure
        new_post = {
            "id": om_entry["name"].lower().replace(" ", "-").replace(".", ""),
            "name": om_entry["name"],
            "url": om_entry["url"],
            "dr": om_entry["dr"],
            "description": f"Guest posting opportunity from outreachmonks.com.",
            "niche": om_entry["niche"],
            "submissionType": "free",
            "listedOn": ["outreachmonks.com"],
            "notes": ""
        }
        main_posts.append(new_post)
        url_map[url_norm] = new_post
        new_entries += 1

# Sort by DR descending
main_posts.sort(key=lambda x: (x.get("dr") is None, -x.get("dr", 0) if x.get("dr") else 0))

# Save back
main_data["guestPosts"] = main_posts
with open(data_dir / "guest-posts.json", "w") as f:
    json.dump(main_data, f, indent=2)

print(f"=== Merge Summary ===")
print(f"Total entries: {len(main_posts)}")
print(f"Duplicates consolidated: {duplicates_found}")
if duplicate_list:
    print(f"  Consolidated sites:")
    for dup in duplicate_list:
        print(f"    • {dup}")
print(f"New entries added: {new_entries}")
print(f"\nFile saved to: {data_dir / 'guest-posts.json'}")
