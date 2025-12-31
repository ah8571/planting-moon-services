#!/usr/bin/env python3
"""
Script to fix all submissionType from 'free' to 'unknown' for unverified entries
This applies to AMRYTT, TopSaaS, and LeadWave entries
"""

import json

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

def main():
    print("Loading directories...")
    with open(DIRS_PATH, 'r') as f:
        data = json.load(f)
    
    fixed = 0
    sources_to_fix = ["amrytt.com", "topsaasdirectories.com", "leadwave.io"]
    
    print("Fixing submissionType to 'unknown' for unverified sources...")
    for d in data['directories']:
        # Check if any of the unverified sources are in listedOn
        has_unverified_source = any(source in d['listedOn'] for source in sources_to_fix)
        
        # If it only has unverified sources and submissionType is 'free', fix it
        if has_unverified_source and d['submissionType'] == 'free':
            d['submissionType'] = 'unknown'
            fixed += 1
    
    print(f"Fixed {fixed} entries")
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Updated directories.json!")
    print(f"Total directories: {len(data['directories'])}")

if __name__ == "__main__":
    main()
