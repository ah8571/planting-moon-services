import json
import re
from pathlib import Path

# Load existing guest posts database
with open('data/guest-posts.json', 'r') as f:
    db_data = json.load(f)
    main_db = db_data['guestPosts']

# Read and parse instalinko_raw.json
instalinko_data = []
with open('data/instalinko_raw.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('instalinko') or line == '':
            continue
        
        # Parse format: "Site Name | Action | Ahrefs Rank: X | DR: Y"
        # Extract site name and DR
        try:
            # Extract DR value
            dr_match = re.search(r'DR:\s*(\d+)', line)
            dr = int(dr_match.group(1)) if dr_match else None
            
            # Extract site name (everything before the first |)
            parts = line.split('|')
            if parts:
                name = parts[0].strip()
                
                # Build URL from name
                url = 'https://' + name.lower().replace(' ', '').replace('.', '') + '.com'
                # Handle common domains
                if 'content' in name.lower() and 'marketing' in name.lower():
                    url = 'https://contentmarketinginstitute.com'
                elif 'blog' in name.lower() and 'herald' in name.lower():
                    url = 'https://theblogherald.com'
                elif 'hubspot' in name.lower():
                    url = 'https://hubspot.com'
                elif 'sitepoint' in name.lower():
                    url = 'https://sitepoint.com'
                else:
                    # Try to construct URL from name
                    url_base = name.lower().replace(' ', '').replace('.', '')
                    if url_base.startswith('www'):
                        url_base = url_base[3:]
                    url = 'https://www.' + url_base + '.com' if ' ' not in name else 'https://' + url_base + '.com'
                
                if name and dr:
                    instalinko_data.append({
                        'name': name,
                        'url': url,
                        'dr': dr,
                        'niche': ['Guest Posting']
                    })
        except (ValueError, IndexError):
            continue

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

# Process instalinko entries
for ins_entry in instalinko_data:
    normalized = normalize_url(ins_entry['url'])
    
    if normalized in existing_urls:
        # Duplicate found
        duplicates_found += 1
        existing_entry = existing_urls[normalized]
        
        # Add instalinko to sources if not already there
        if 'instalinko' not in existing_entry['listedOn']:
            existing_entry['listedOn'].append('instalinko')
        
        # Upgrade DR if instalinko has higher value
        ins_dr = ins_entry.get('dr')
        existing_dr = existing_entry.get('dr')
        
        if ins_dr and (not existing_dr or ins_dr > existing_dr):
            old_dr = existing_dr
            existing_entry['dr'] = ins_dr
            dr_upgrades += 1
            upgraded_entries.append({
                'name': existing_entry['name'],
                'old_dr': old_dr,
                'new_dr': ins_dr
            })
    else:
        # New entry
        new_entry = {
            'id': re.sub(r'[^a-z0-9]+', '-', ins_entry['name'].lower()).strip('-'),
            'name': ins_entry['name'],
            'url': ins_entry['url'],
            'dr': ins_entry.get('dr'),
            'description': f"Guest posting opportunity from {ins_entry['name']}",
            'niche': ins_entry.get('niche', []),
            'submissionType': 'free',
            'listedOn': ['instalinko'],
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
print(f"INSTALINKO MERGE")
print(f"Source file entries: {len(instalinko_data)}")
print(f"Duplicates found: {duplicates_found}")
if dr_upgrades > 0:
    print(f"  DR updates: {dr_upgrades}")
    for entry in upgraded_entries[:10]:
        print(f"    • {entry['name']} (DR {entry['new_dr']} updated from {entry['old_dr']})")
    if len(upgraded_entries) > 10:
        print(f"    ... and {len(upgraded_entries) - 10} more")
print(f"New entries added: {new_entries}")
print(f"Database now at: {len(main_db)} entries")
