#!/usr/bin/env python3
"""
Script to fix duplicate ID issues by merging entries
"""

import json

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

def main():
    print("Loading directories...")
    with open(DIRS_PATH, 'r') as f:
        data = json.load(f)
    
    dirs = data['directories']
    
    # Define the merges: keep the entry at index1, merge listedOn and remove duplicate
    merges = [
        # Find and merge these duplicates (by name pattern)
        {
            'primary_name': 'Saasworthy',
            'duplicate_names': ['Saasworthy'],  # exact duplicates
            'keep_description': True
        },
        {
            'primary_name': 'Dev to',
            'duplicate_names': ['Dev'],
            'keep_description': True
        },
        {
            'primary_name': 'Resource FYI',
            'duplicate_names': ['Resource.fyi'],
            'keep_description': True
        },
        {
            'primary_name': 'Ramen Tools',
            'duplicate_names': ['Ramen.Tools'],
            'keep_description': True
        },
        {
            'primary_name': 'Sitelike',
            'duplicate_names': ['Sitelike.org'],
            'keep_description': True
        },
        {
            'primary_name': 'Launched',
            'duplicate_names': ['Launched!'],
            'keep_description': True
        },
        {
            'primary_name': 'List.ly',
            'duplicate_names': ['List'],
            'keep_description': True
        },
    ]
    
    total_merged = 0
    
    for merge_rule in merges:
        primary_name = merge_rule['primary_name']
        dup_names = merge_rule['duplicate_names']
        
        # Find primary
        primary_idx = None
        for i, d in enumerate(dirs):
            if d['name'] == primary_name:
                primary_idx = i
                break
        
        if primary_idx is None:
            print(f"Warning: Could not find primary '{primary_name}'")
            continue
        
        # Find and merge duplicates
        indices_to_remove = []
        for dup_name in dup_names:
            for i, d in enumerate(dirs):
                if i != primary_idx and d['name'] == dup_name:
                    print(f"Merging: '{dup_name}' into '{primary_name}'")
                    
                    # Merge listedOn sources
                    for source in d['listedOn']:
                        if source not in dirs[primary_idx]['listedOn']:
                            dirs[primary_idx]['listedOn'].append(source)
                    
                    # Use better description if primary is empty
                    if not dirs[primary_idx]['description'] and d['description']:
                        dirs[primary_idx]['description'] = d['description']
                    
                    # Use better DR if primary is unknown
                    if dirs[primary_idx]['domainRating'] == 'unknown' and d['domainRating'] != 'unknown':
                        dirs[primary_idx]['domainRating'] = d['domainRating']
                    
                    indices_to_remove.append(i)
                    total_merged += 1
        
        # Remove duplicates (in reverse order to maintain indices)
        for idx in sorted(indices_to_remove, reverse=True):
            print(f"  Removing duplicate entry: {dirs[idx]['name']}")
            del dirs[idx]
    
    print(f"\n=== Results ===")
    print(f"Merged {total_merged} duplicate entries")
    print(f"Total directories now: {len(dirs)}")
    
    # Save
    data['directories'] = dirs
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Updated directories.json!")

if __name__ == "__main__":
    main()
