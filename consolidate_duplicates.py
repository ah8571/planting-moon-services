#!/usr/bin/env python3
"""
Script to clean and consolidate duplicates in directories.json
Removes specific entries and merges duplicate listings
"""

import json
import os

# Load the JSON file
filepath = 'public/data/directories.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

directories = data['directories']

# Entries to remove completely
remove_ids = [
    'betalists',
    'reddit-small-business',
    'reddit-startups',
    'reddit-entrepreneur',
    'reddit-saas'
]

# Duplicate pairs to consolidate (keep first, merge sources from second)
consolidations = [
    # (keep_id, remove_id, new_name_if_different)
    ('10-words', '10words', None),
    ('afford-hunt', 'affordhunt', None),
    ('ctrl-alt', 'ctrlalt-cc', None),
    ('eu-startups', 'eu-startups-com', None),
    ('future-tools', 'futuretools', None),
    ('g2', 'g2-stack', None),
    ('geek-wire', 'geekwire', None),
    ('growth-hackers', 'growthhackers', None),
    ('hacker-news', 'hackernews', None),
    ('indie-hackers', 'indie-hacker-projects', None),
    ('killer-startups', 'killerstartups-com', None),
    ('make-rs', 'makers', None),
    ('neil-patel-ai-tools', 'ai-tools-neil-patel', None),
    ('peerlist-io', 'peerlist-launchpad', None),
    ('promote-project', 'promoteproject', None),
    ('saas-hub', 'saas-hub-directory', None),
    ('side-projectors', 'sideprojectors-com', None),
    ('uneed-lemonsqueezy-com', 'uneed-best', None),
]

# Build maps for easier lookup
id_to_index = {d['id']: i for i, d in enumerate(directories)}
name_to_id = {d['name']: d['id'] for d in directories}

# Step 1: Remove entries
print(f"Removing {len(remove_ids)} entries...")
for entry_id in remove_ids:
    if entry_id in id_to_index:
        idx = id_to_index[entry_id]
        removed_name = directories[idx]['name']
        print(f"  - Removing: {removed_name} ({entry_id})")
        del directories[idx]
        # Update map
        id_to_index = {d['id']: i for i, d in enumerate(directories)}

# Step 2: Consolidate duplicates
print(f"\nConsolidating {len(consolidations)} duplicate pairs...")
for keep_id, remove_id, new_name in consolidations:
    if keep_id not in id_to_index or remove_id not in id_to_index:
        if keep_id not in id_to_index:
            print(f"  WARNING: Keep ID '{keep_id}' not found")
        if remove_id not in id_to_index:
            print(f"  WARNING: Remove ID '{remove_id}' not found")
        continue
    
    keep_idx = id_to_index[keep_id]
    remove_idx = id_to_index[remove_id]
    
    keep_entry = directories[keep_idx]
    remove_entry = directories[remove_idx]
    
    print(f"  - Consolidating: '{remove_entry['name']}' into '{keep_entry['name']}'")
    
    # Merge listedOn sources
    existing_sources = set(keep_entry.get('listedOn', []))
    new_sources = set(remove_entry.get('listedOn', []))
    merged_sources = sorted(list(existing_sources | new_sources))
    keep_entry['listedOn'] = merged_sources
    
    # Keep higher DR value
    keep_dr = keep_entry.get('domainRating', 'unknown')
    remove_dr = remove_entry.get('domainRating', 'unknown')
    
    if keep_dr == 'unknown' and remove_dr != 'unknown':
        keep_entry['domainRating'] = remove_dr
    elif isinstance(keep_dr, (int, float)) and isinstance(remove_dr, (int, float)):
        keep_entry['domainRating'] = max(keep_dr, remove_dr)
    
    # Remove duplicate entry
    del directories[remove_idx]
    # Update map
    id_to_index = {d['id']: i for i, d in enumerate(directories)}

# Save updated JSON
print(f"\nSaving consolidated file...")
output_data = {'directories': directories}
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"\nComplete! Total directories: {len(directories)}")
print(f"Removed: {len(remove_ids)}")
print(f"Consolidated: {len(consolidations)} pairs")
