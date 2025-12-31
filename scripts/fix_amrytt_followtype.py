#!/usr/bin/env python3
"""
Fix the followType for AMRYTT entries from 'dofollow' to 'unknown'
"""

import json

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

def main():
    print("Loading directories.json...")
    with open(DIRS_PATH, 'r') as f:
        data = json.load(f)
    
    updated = 0
    # Find all entries listed on amrytt.com and update their followType to unknown
    for directory in data['directories']:
        if 'amrytt.com' in directory.get('listedOn', []):
            if directory.get('followType') == 'dofollow' and directory.get('notes', '') == '':
                directory['followType'] = 'unknown'
                directory['notes'] = 'Follow type not specified in source'
                updated += 1
    
    print(f"Updated {updated} entries from dofollow to unknown")
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Saved directories.json")

if __name__ == "__main__":
    main()
