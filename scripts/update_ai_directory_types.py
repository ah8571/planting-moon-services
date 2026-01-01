#!/usr/bin/env python3
"""
Update directories.json to support multiple types and add AI Directory tag.
"""

import json
from pathlib import Path

# Entries to update - from submitatool.com source
ENTRIES_TO_UPDATE = {
    'sourceforge': 'Source Forge',
    'ai-tools-neil-patel': 'AI Tools Neil Patel',
    'ai-infinity': 'AI Infinity',
    'startup88': 'Startup88',
    'financesonline': 'FinancesOnline',
    'f6s-com': 'F6S',
    'your-story': 'Your Story',
    'alternativeto': 'AlternativeTo',
    'crunchbase': 'Crunchbase',
    'stackshare': 'Stackshare',
    'webwiki': 'Webwiki',
    'alternative-me': 'Alternative',
    'digital-agency-network': 'Digital Agency Network',
    'eu-startups': 'EU Startups',
    'software-world': 'Software World',
    'product-hunt': 'Product Hunt',
    'saasworthy': 'SaasWorthy',
    'getlatka': 'Getlatka',
    'sitelike': 'Sitelike',
    'beta-list': 'Beta List',
    'saashub': 'SaaS Hub',
    'sideprojectors': 'SideProjectors',
    'startup-ranking': 'Startup Ranking',
    'pitchwall': 'Pitchwall',
    'submission-web-directory': 'Submission Web Directory',
    'somuch': 'SoMuch',
    'marketing-internet-directory': 'Marketing Internet Directory',
    'gpts-hunter': 'GPTs Hunter',
    'kitploit': 'KitPloit',
    'afford-hunt': 'Afford Hunt',
    'business-software': 'Business Software',
    'aitools': 'AITOOLS',
    'fivetaco': 'FiveTaco',
    'uneed': 'uneed',
    'tool-pilot': 'Tool Pilot',
    'launching-next': 'Launching Next',
    'startup-base': 'Startup Base',
    'techpluto': 'TechPluto',
    'ezweb-directory': 'EZWeb Directory',
    'ismailblogger': 'Ismailblogger',
    'future-tools': 'Future Tools',
    'hacker-news': 'Hacker News',
    'startuptracker': 'StartupTracker',
    'tiny-startups': 'Tiny Startups',
    '100l5': '100L5',
    'insidr-ai': 'Insidr AI',
}

def load_directories():
    """Load the directories.json file."""
    with open('data/directories.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def update_entry_type(entry, entry_id):
    """Convert type to array format and add AI Directory if applicable."""
    current_type = entry.get('type', '')
    
    # Convert single string to array
    if isinstance(current_type, str):
        types = [current_type] if current_type else []
    else:
        types = list(current_type) if current_type else []
    
    # Add AI Directory if not already present
    if 'AI Directory' not in types:
        types.append('AI Directory')
    
    # Update the entry
    entry['type'] = types
    
    return entry

def main():
    """Main function to update directories."""
    data = load_directories()
    
    updates_made = []
    not_found = []
    
    for entry in data['directories']:
        entry_id = entry.get('id', '').lower()
        entry_name = entry.get('name', '')
        
        # Check if this entry should be updated
        if entry_id in ENTRIES_TO_UPDATE:
            original_type = entry.get('type')
            original_submission = entry.get('submissionType')
            
            # Ensure submission type is free
            if entry.get('submissionType') != 'free':
                entry['submissionType'] = 'free'
            
            # Update type to include AI Directory
            update_entry_type(entry, entry_id)
            
            new_type = entry.get('type')
            
            updates_made.append({
                'id': entry_id,
                'name': entry_name,
                'original_type': original_type,
                'new_type': new_type,
                'submission_type': entry.get('submissionType')
            })
    
    # Save updated data
    with open('data/directories.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Print results
    print(f"\n{'='*80}")
    print(f"UPDATED {len(updates_made)} ENTRIES")
    print(f"{'='*80}\n")
    
    for update in updates_made:
        print(f"✓ {update['name']}")
        print(f"  ID: {update['id']}")
        print(f"  Original type: {update['original_type']}")
        print(f"  New type: {update['new_type']}")
        print(f"  Submission Type: {update['submission_type']}")
        print()
    
    if not_found:
        print(f"\n{'='*80}")
        print(f"NOT FOUND IN DIRECTORIES.JSON ({len(not_found)}):")
        print(f"{'='*80}\n")
        for entry_id in not_found:
            print(f"  - {entry_id}")

if __name__ == '__main__':
    main()
