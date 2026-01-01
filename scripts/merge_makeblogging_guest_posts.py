import json
import re
from pathlib import Path

# Load existing guest posts database
with open('data/guest-posts.json', 'r') as f:
    db_data = json.load(f)
    main_db = db_data['guestPosts']

# Load makeblogging data
with open('data/makeblogging_raw.json', 'r') as f:
    makeblogging_data = json.load(f)

def normalize_url(url):
    """Normalize URL for comparison"""
    url = url.lower().strip()
    if not url.startswith('http'):
        url = 'https://' + url
    url = url.rstrip('/')
    # Extract domain for comparison
    match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return match.group(1) if match else url

# Create URL mapping for existing database
existing_urls = {}
for entry in main_db:
    normalized = normalize_url(entry['url'])
    existing_urls[normalized] = entry

# Track changes
duplicates_found = 0
new_entries = 0
dr_upgrades = 0
upgraded_entries = []

# Process makeblogging entries
for makeblog_entry in makeblogging_data:
    normalized = normalize_url(makeblog_entry['url'])
    
    if normalized in existing_urls:
        # Duplicate found
        duplicates_found += 1
        existing_entry = existing_urls[normalized]
        
        # Add makeblogging to sources if not already there
        if 'makeblogging' not in existing_entry['listedOn']:
            existing_entry['listedOn'].append('makeblogging')
        
        # Upgrade DR if makeblogging has higher value
        makeblog_dr = makeblog_entry.get('dr')
        existing_dr = existing_entry.get('dr')
        
        if makeblog_dr and (not existing_dr or makeblog_dr > existing_dr):
            old_dr = existing_dr
            existing_entry['dr'] = makeblog_dr
            dr_upgrades += 1
            upgraded_entries.append({
                'name': existing_entry['name'],
                'old_dr': old_dr,
                'new_dr': makeblog_dr
            })
    else:
        # New entry
        new_entry = {
            'id': re.sub(r'[^a-z0-9]+', '-', makeblog_entry['name'].lower()).strip('-'),
            'name': makeblog_entry['name'],
            'url': makeblog_entry['url'],
            'dr': makeblog_entry.get('dr'),
            'description': f"Guest posting opportunity from {makeblog_entry['name']}",
            'niche': makeblog_entry.get('niche', []),
            'submissionType': 'free',
            'listedOn': ['makeblogging'],
            'notes': ''
        }
        main_db.append(new_entry)
        new_entries += 1

# Sort by DR (descending, None at end)
main_db.sort(key=lambda x: (x.get('dr') is None, -x.get('dr') if x.get('dr') else 0))

# Save updated database
db_data['guestPosts'] = main_db
with open('data/guest-posts.json', 'w') as f:
    json.dump(db_data, f, indent=2)

# Print summary
print(f"Main file: {len(main_db) - new_entries} entries")
print(f"Makeblogging entries: {len(makeblogging_data)}")
print()
print("=== Merge Summary ===")
print(f"Total entries: {len(main_db)}")
print(f"Duplicates found: {duplicates_found}")
if dr_upgrades > 0:
    print(f"  DR updates/consolidations: {dr_upgrades}")
    for entry in upgraded_entries:
        print(f"    • {entry['name']} (DR {entry['new_dr']} updated from {entry['old_dr']})")
print(f"New entries added: {new_entries}")
print()
print(f"File saved to: {Path('data/guest-posts.json').absolute()}")
