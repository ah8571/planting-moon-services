#!/usr/bin/env python3
"""
Script to check for duplicate directories in directories.json
Checks by name, URL, and ID
"""

import json

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

def main():
    print("Loading directories...")
    with open(DIRS_PATH, 'r') as f:
        data = json.load(f)
    
    dirs = data['directories']
    print(f"Total entries: {len(dirs)}\n")
    
    # Check for duplicate names (case-insensitive)
    print("=== Checking for duplicate names ===")
    name_map = {}
    name_duplicates = []
    for d in dirs:
        name_lower = d['name'].lower()
        if name_lower in name_map:
            name_duplicates.append((name_lower, name_map[name_lower], d['id']))
        else:
            name_map[name_lower] = d['id']
    
    if name_duplicates:
        print(f"Found {len(name_duplicates)} duplicate names:\n")
        for name, first_id, dup_id in name_duplicates:
            print(f"  - '{name}'")
            print(f"    IDs: {first_id} vs {dup_id}")
    else:
        print("✓ No duplicate names found\n")
    
    # Check for duplicate URLs (excluding empty ones)
    print("=== Checking for duplicate URLs ===")
    url_map = {}
    url_duplicates = []
    for d in dirs:
        url = d.get('url', '').strip()
        if url and url != "":
            url_lower = url.lower()
            if url_lower in url_map:
                url_duplicates.append((url_lower, url_map[url_lower], d['name']))
            else:
                url_map[url_lower] = d['name']
    
    if url_duplicates:
        print(f"Found {len(url_duplicates)} duplicate URLs:\n")
        for url, first_name, dup_name in url_duplicates:
            print(f"  - {url}")
            print(f"    Names: {first_name} vs {dup_name}")
    else:
        print("✓ No duplicate URLs found\n")
    
    # Check for duplicate IDs (should never happen)
    print("=== Checking for duplicate IDs ===")
    id_map = {}
    id_duplicates = []
    for d in dirs:
        entry_id = d['id']
        if entry_id in id_map:
            id_duplicates.append((entry_id, id_map[entry_id], d['name']))
        else:
            id_map[entry_id] = d['name']
    
    if id_duplicates:
        print(f"Found {len(id_duplicates)} duplicate IDs:\n")
        for eid, first_name, dup_name in id_duplicates:
            print(f"  - ID: {eid}")
            print(f"    Names: {first_name} vs {dup_name}")
    else:
        print("✓ No duplicate IDs found\n")
    
    # Show entries with empty URLs
    print("=== Entries with empty URLs ===")
    empty_url_count = 0
    for d in dirs:
        if not d.get('url') or d.get('url').strip() == "":
            empty_url_count += 1
    
    print(f"Entries with no URL: {empty_url_count} / {len(dirs)}")
    print(f"Percentage: {empty_url_count/len(dirs)*100:.1f}%\n")
    
    # Summary
    print("=== SUMMARY ===")
    print(f"Total entries: {len(dirs)}")
    print(f"Name duplicates: {len(name_duplicates)}")
    print(f"URL duplicates: {len(url_duplicates)}")
    print(f"ID duplicates: {len(id_duplicates)}")
    print(f"Entries with no URL: {empty_url_count}")
    
    if not name_duplicates and not url_duplicates and not id_duplicates:
        print("\n✓ No duplicates detected!")
    
    return len(name_duplicates) + len(url_duplicates) + len(id_duplicates)

if __name__ == "__main__":
    duplicates_found = main()
    exit(duplicates_found)
