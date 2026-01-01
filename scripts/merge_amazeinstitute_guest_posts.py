import json
import re
from pathlib import Path

# Load existing guest posts database
with open('data/guest-posts.json', 'r') as f:
    db_data = json.load(f)
    main_db = db_data['guestPosts']

# Read and parse amazeinstitute.co.in_raw.json (tab-separated format)
amazeinstitute_data = []
with open('data/amazeinstitute.co.in_raw.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines[1:]:  # Skip the header line
        line = line.strip()
        if not line or line.startswith('ok this is'):
            continue
        
        # Parse tab-separated: number \t url \t dr
        parts = line.split('\t')
        if len(parts) >= 2:
            try:
                url = parts[1].strip()
                dr_str = parts[2].strip() if len(parts) > 2 else None
                
                if url and url.startswith('http'):
                    dr = int(dr_str) if dr_str and dr_str.isdigit() else None
                    
                    # Extract name from URL
                    name_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
                    name = name_match.group(1).replace('www.', '') if name_match else url
                    name = ' '.join(word.capitalize() for word in name.split('.')[0].split('-'))
                    
                    amazeinstitute_data.append({
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

# Process amazeinstitute entries
for ai_entry in amazeinstitute_data:
    normalized = normalize_url(ai_entry['url'])
    
    if normalized in existing_urls:
        # Duplicate found
        duplicates_found += 1
        existing_entry = existing_urls[normalized]
        
        # Add amazeinstitute.co.in to sources if not already there
        if 'amazeinstitute.co.in' not in existing_entry['listedOn']:
            existing_entry['listedOn'].append('amazeinstitute.co.in')
        
        # Upgrade DR if amazeinstitute has higher value
        ai_dr = ai_entry.get('dr')
        existing_dr = existing_entry.get('dr')
        
        if ai_dr and (not existing_dr or ai_dr > existing_dr):
            old_dr = existing_dr
            existing_entry['dr'] = ai_dr
            dr_upgrades += 1
            upgraded_entries.append({
                'name': existing_entry['name'],
                'old_dr': old_dr,
                'new_dr': ai_dr
            })
    else:
        # New entry
        new_entry = {
            'id': re.sub(r'[^a-z0-9]+', '-', ai_entry['name'].lower()).strip('-'),
            'name': ai_entry['name'],
            'url': ai_entry['url'],
            'dr': ai_entry.get('dr'),
            'description': f"Guest posting opportunity from {ai_entry['name']}",
            'niche': ai_entry.get('niche', []),
            'submissionType': 'free',
            'listedOn': ['amazeinstitute.co.in'],
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
print(f"AMAZEINSTITUTE.CO.IN MERGE")
print(f"Source file entries: {len(amazeinstitute_data)}")
print(f"Duplicates found: {duplicates_found}")
if dr_upgrades > 0:
    print(f"  DR updates: {dr_upgrades}")
    for entry in upgraded_entries[:10]:
        print(f"    • {entry['name']} (DR {entry['new_dr']} updated from {entry['old_dr']})")
    if len(upgraded_entries) > 10:
        print(f"    ... and {len(upgraded_entries) - 10} more")
print(f"New entries added: {new_entries}")
print(f"Database now at: {len(main_db)} entries")
