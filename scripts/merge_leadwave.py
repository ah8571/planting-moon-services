#!/usr/bin/env python3
"""
Script to merge LeadWave CSV data into directories.json
Handles both new entries and updating existing ones
Also fixes submissionType from 'free' to 'unknown' for unverified entries
"""

import json
import csv
import re

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"
LEADWAVE_CSV = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\SaaS Directories by LeadWave 🌊.csv"

def name_to_id(name):
    """Convert name to ID"""
    name_lower = name.lower().strip()
    id_str = re.sub(r'[^a-z0-9]', '-', name_lower)
    id_str = re.sub(r'-+', '-', id_str)
    id_str = id_str.strip('-')
    return id_str[:50]

def map_leadwave_type(leadwave_type):
    """Map LeadWave type emoji to our type system"""
    type_map = {
        "🚀 Startup Directory": "Startup Directory",
        "⭐️ Review Directory": "Review Directory",
        "🧩 SaaS Marketplace": "SaaS Marketplace",
        "👥 Community": "Community",
        "💫 Other": "Directory",
        "🔧 Developer Tools": "Developer Tools",
    }
    return type_map.get(leadwave_type, "Directory")

def extract_domain(website_str):
    """Extract clean domain from website column"""
    if not website_str:
        return ""
    # Handle URLs like "https://..." or just "domain.com"
    if "http" in website_str.lower():
        match = re.search(r'https?://([^/]+)', website_str)
        if match:
            return match.group(1)
    # Otherwise just clean it up
    clean = website_str.strip().strip('/')
    if clean and not clean.startswith('http'):
        return clean
    return ""

def load_existing():
    """Load existing directories.json"""
    with open(DIRS_PATH, 'r') as f:
        return json.load(f)

def find_matching_entry(name, website, existing_data):
    """Find if this entry already exists"""
    name_lower = name.lower()
    for d in existing_data['directories']:
        if d['name'].lower() == name_lower:
            return d
        # Also check by website
        if website and d['url'] and website.lower() in d['url'].lower():
            return d
    return None

def create_new_entry(name, website, type_str):
    """Create a new directory entry from LeadWave data"""
    domain = extract_domain(website)
    
    return {
        "id": name_to_id(name),
        "name": name,
        "url": f"https://{domain}" if domain else "",
        "description": "",
        "type": type_str,
        "domainRating": "unknown",
        "submissionType": "unknown",
        "followType": "unknown",
        "listedOn": ["leadwave.io"],
        "notes": "URL format, DR, and submission type not specified in source"
    }

def load_leadwave_csv():
    """Load LeadWave CSV data - using strict quoting since Logo column has URLs"""
    entries = []
    try:
        # Open with utf-8-sig to handle BOM
        with open(LEADWAVE_CSV, 'r', encoding='utf-8-sig') as f:
            # Use strict quoting to handle the URL-laden Logo field
            reader = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if row and row.get('Name'):
                    name = row.get('Name', '').strip()
                    website = row.get('Website', '').strip()
                    type_str = row.get('Type', '').strip()
                    
                    if name and type_str:
                        entries.append({
                            'name': name,
                            'website': website,
                            'type': type_str,
                        })
    except Exception as e:
        print(f"CSV Error: {e}, trying manual parse...")
        entries = parse_leadwave_csv_manual()
    return entries

def parse_leadwave_csv_manual():
    """Manual parsing of LeadWave CSV to handle complex formatting"""
    entries = []
    with open(LEADWAVE_CSV, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        if not line or line.startswith('Name'):
            continue
        
        # Split by comma, but need to be careful with URLs
        # Format: Name,Website,Logo(url),Type
        parts = []
        current = ""
        in_url = False
        
        for char in line:
            if char == ',' and not in_url:
                parts.append(current)
                current = ""
            else:
                if 'http' in current.lower()[-5:] or 'http' in char:
                    in_url = True
                elif in_url and char == ')':
                    in_url = False
                current += char
        
        if current:
            parts.append(current)
        
        # Extract fields - should be at least 4 parts
        if len(parts) >= 4:
            name = parts[0].strip()
            website = parts[1].strip()
            type_str = parts[3].strip()
            
            if name and type_str:
                entries.append({
                    'name': name,
                    'website': website,
                    'type': type_str,
                })
    
    return entries

def fix_submission_types(data):
    """Fix submissionType from 'free' to 'unknown' for unverified entries"""
    fixed = 0
    for d in data['directories']:
        # Fix entries from AMRYTT and TopSaaS that were marked as 'free'
        if d['submissionType'] == 'free' and 'unknown' in str(d.get('notes', '')).lower():
            d['submissionType'] = 'unknown'
            fixed += 1
        # Also fix entries without DR that were marked free (these are likely guesses)
        if d['submissionType'] == 'free' and d['domainRating'] == 'unknown':
            d['submissionType'] = 'unknown'
            fixed += 1
    return fixed

def main():
    print("Loading LeadWave CSV...")
    leadwave_entries = load_leadwave_csv()
    print(f"Parsed {len(leadwave_entries)} entries from LeadWave")
    
    print("Loading existing directories...")
    data = load_existing()
    print(f"Currently have {len(data['directories'])} directories")
    
    # First, fix existing submissionType entries
    print("\nFixing submissionType for unverified entries...")
    fixed = fix_submission_types(data)
    print(f"Fixed {fixed} entries")
    
    # Now merge LeadWave data
    print("\nProcessing LeadWave entries...")
    new_count = 0
    updated_count = 0
    
    for entry in leadwave_entries:
        existing = find_matching_entry(entry['name'], entry['website'], data)
        mapped_type = map_leadwave_type(entry['type'])
        
        if existing:
            # Update listedOn
            if "leadwave.io" not in existing['listedOn']:
                existing['listedOn'].append("leadwave.io")
                updated_count += 1
        else:
            # Add new entry
            new_entry = create_new_entry(entry['name'], entry['website'], mapped_type)
            data['directories'].append(new_entry)
            new_count += 1
    
    print(f"\n=== Results ===")
    print(f"New entries added: {new_count}")
    print(f"Existing entries updated: {updated_count}")
    print(f"Existing entries fixed: {fixed}")
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nTotal directories now: {len(data['directories'])}")

if __name__ == "__main__":
    main()
