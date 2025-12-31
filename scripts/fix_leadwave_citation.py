#!/usr/bin/env python3
"""
Script to fix leadwave.io citations to getleadwave.io
"""

import json

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

def main():
    print("Loading directories...")
    with open(DIRS_PATH, 'r') as f:
        data = json.load(f)
    
    dirs = data['directories']
    fixed = 0
    
    print("Fixing leadwave.io citations to getleadwave.io...")
    
    for d in dirs:
        if 'leadwave.io' in d['listedOn']:
            # Replace the citation
            d['listedOn'] = [s if s != 'leadwave.io' else 'getleadwave.io' for s in d['listedOn']]
            fixed += 1
    
    print(f"\nFixed {fixed} entries")
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Updated directories.json!")

if __name__ == "__main__":
    main()
