#!/usr/bin/env python3
"""
Merge additional collaborator.pro profile/social media sites with DR values.
These are platforms where you can add links in profiles, posts, or descriptions.
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

# Additional collaborator.pro profile/social media sites
additional_collaborator = [
    {"name": "Moz", "url": "https://moz.com", "dr": 91, "niche": ["SEO", "Marketing"]},
    {"name": "Substack", "url": "https://substack.com", "dr": 92, "niche": ["Publishing", "Newsletter"]},
    {"name": "Steemit", "url": "https://steemit.com", "dr": 88, "niche": ["Blogging", "Cryptocurrency"]},
    {"name": "Google Sites", "url": "https://sites.google.com", "dr": 96, "niche": ["Website Builder", "Google"]},
    {"name": "Instructables", "url": "https://instructables.com", "dr": 92, "niche": ["DIY", "How-to"]},
    {"name": "TypePad", "url": "https://typepad.com", "dr": 49, "niche": ["Blogging"]},
    {"name": "Biz Community", "url": "https://bizcommunity.com", "dr": 79, "niche": ["Business", "News"]},
    {"name": "Brown Book", "url": "https://brownbook.net", "dr": 62, "niche": ["Directory", "Local"]},
    {"name": "HotFrog", "url": "https://hotfrog.com", "dr": 57, "niche": ["Directory", "Local"]},
    {"name": "Local Pages", "url": "https://localpages.com", "dr": 41, "niche": ["Directory", "Local"]},
    {"name": "Link Centre", "url": "https://linkcentre.com", "dr": 50, "niche": ["Directory", "Links"]},
    {"name": "Folkd", "url": "https://folkd.com", "dr": 80, "niche": ["Social Bookmarking"]},
    {"name": "Instapaper", "url": "https://instapaper.com", "dr": 88, "niche": ["Bookmarking", "Reading"]},
    {"name": "Pearltrees", "url": "https://pearltrees.com", "dr": 84, "niche": ["Curation", "Collections"]},
    {"name": "Unsplash", "url": "https://unsplash.com", "dr": 98, "niche": ["Photography", "Stock Images"]},
    {"name": "Pinterest", "url": "https://pinterest.com", "dr": 94, "niche": ["Social Media", "Visual"]},
    {"name": "Behance", "url": "https://behance.net", "dr": 93, "niche": ["Design", "Portfolio"]},
    {"name": "Stack Overflow", "url": "https://stackoverflow.com", "dr": 92, "niche": ["Programming", "Q&A"]},
    {"name": "Ghost Forum", "url": "https://forum.ghost.org", "dr": 91, "niche": ["Community", "Blogging"]},
    {"name": "APS Sense", "url": "https://apsense.com", "dr": 75, "niche": ["Social Network", "Business"]},
    {"name": "Dev.to", "url": "https://dev.to", "dr": 83, "niche": ["Technology", "Programming"]},
    {"name": "HubPages", "url": "https://discover.hubpages.com", "dr": 85, "niche": ["Content", "Publishing"]},
    {"name": "DailyMotion", "url": "https://dailymotion.com", "dr": 95, "niche": ["Video", "Media"]},
    {"name": "TrustRadius", "url": "https://trustradius.com", "dr": 68, "niche": ["Reviews", "B2B"]},
    {"name": "Gartner", "url": "https://gartner.com", "dr": 91, "niche": ["Research", "Technology"]},
    {"name": "ProvenExpert", "url": "https://provenexpert.com", "dr": 91, "niche": ["Reviews", "Expertise"]},
    {"name": "Scribd", "url": "https://scribd.com", "dr": 94, "niche": ["Documents", "Publishing"]},
    {"name": "SlideShare", "url": "https://slideshare.net", "dr": 94, "niche": ["Presentations", "Documents"]},
    {"name": "Edocr", "url": "https://edocr.com", "dr": 74, "niche": ["Documents", "Publishing"]},
    {"name": "Reddit", "url": "https://reddit.com", "dr": 95, "niche": ["Social News", "Community"]},
    {"name": "LinkedIn", "url": "https://linkedin.com", "dr": 99, "niche": ["Social Network", "Professional"]},
    {"name": "Medium", "url": "https://medium.com", "dr": 94, "niche": ["Publishing", "Content"]},
    {"name": "YouTube", "url": "https://youtube.com", "dr": 99, "niche": ["Video", "Media"]},
    {"name": "About.me", "url": "https://about.me", "dr": 90, "niche": ["Profile", "Personal Branding"]},
    {"name": "Issue.com", "url": "https://issue.com", "dr": 93, "niche": ["Publishing", "PDFs"]},
    {"name": "Seek Logo", "url": "https://seeklogo.com", "dr": 69, "niche": ["Logo", "Branding"]},
    {"name": "Product Hunt", "url": "https://producthunt.com", "dr": 91, "niche": ["Products", "Launch"]},
    {"name": "G2", "url": "https://g2.com", "dr": 91, "niche": ["Reviews", "B2B"]},
    {"name": "AlternativeTo", "url": "https://alternativeto.net", "dr": 79, "niche": ["Reviews", "Alternatives"]},
    {"name": "Qwoted", "url": "https://qwoted.com", "dr": 73, "niche": ["Experts", "PR"]},
    {"name": "Quora", "url": "https://quora.com", "dr": 92, "niche": ["Q&A", "Community"]},
    {"name": "Vimeo", "url": "https://vimeo.com", "dr": 96, "niche": ["Video", "Media"]},
    {"name": "GitHub", "url": "https://github.com", "dr": 96, "niche": ["Programming", "Development"]},
    {"name": "Dribbble", "url": "https://dribbble.com", "dr": 93, "niche": ["Design", "Portfolio"]},
    {"name": "Vocal Media", "url": "https://vocal.media", "dr": 82, "niche": ["Publishing", "Stories"]},
]

print(f"Additional collaborator.pro entries: {len(additional_collaborator)}\n")

# Create map of existing posts by normalized URL
def normalize_url(url):
    return url.lower().rstrip("/")

url_map = {}
for post in main_posts:
    url_norm = normalize_url(post["url"])
    url_map[url_norm] = post

# Merge additional collaborator entries
duplicates_found = 0
new_entries = 0
updated_entries = []
duplicate_list = []

for col_entry in additional_collaborator:
    url_norm = normalize_url(col_entry["url"])
    
    if url_norm in url_map:
        # Duplicate found - add/update source
        existing_post = url_map[url_norm]
        
        # Update DR if new entry has higher DR
        if col_entry["dr"] and (existing_post.get("dr") is None or col_entry["dr"] > existing_post.get("dr", 0)):
            old_dr = existing_post.get("dr")
            existing_post["dr"] = col_entry["dr"]
            if old_dr:
                duplicate_list.append(f"{col_entry['name']} (DR {col_entry['dr']} updated from {old_dr})")
            else:
                duplicate_list.append(f"{col_entry['name']} (DR {col_entry['dr']} added)")
        
        # Add source if not already there
        if "collaborator.pro" not in existing_post["listedOn"]:
            existing_post["listedOn"].append("collaborator.pro")
            duplicates_found += 1
    else:
        # New entry
        new_post = {
            "id": col_entry["name"].lower().replace(" ", "-").replace(".", "").replace(",", ""),
            "name": col_entry["name"],
            "url": col_entry["url"],
            "dr": col_entry["dr"],
            "description": f"Profile/link placement opportunity from collaborator.pro.",
            "niche": col_entry["niche"],
            "submissionType": "free",
            "listedOn": ["collaborator.pro"],
            "notes": "Add link in profile, posts, descriptions, or project documentation."
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
print(f"Duplicates found: {duplicates_found}")
if duplicate_list:
    print(f"  Updates/consolidations:")
    for dup in duplicate_list[:15]:
        print(f"    • {dup}")
    if len(duplicate_list) > 15:
        print(f"    ... and {len(duplicate_list) - 15} more")
print(f"New entries added: {new_entries}")
print(f"\nFile saved to: {data_dir / 'guest-posts.json'}")
