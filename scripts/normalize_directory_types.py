#!/usr/bin/env python3
"""
Fix directories.json to ensure:
1. All types are arrays
2. Review-related directories include "Review Directory" tag
3. Preserve all existing type information
"""

import json

def load_directories():
    """Load the directories.json file."""
    with open('data/directories.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_type(type_val):
    """Convert type to array format and ensure it's normalized."""
    if isinstance(type_val, list):
        return type_val
    elif isinstance(type_val, str):
        return [type_val] if type_val and type_val.strip() else []
    else:
        return []

def should_include_review_directory(directory):
    """Check if directory should be tagged as Review Directory."""
    review_keywords = [
        'review', 'comparison', 'compare', 'comparison', 'ratings',
        'peer-to-peer', 'peer review'
    ]
    
    text_to_check = (
        directory.get('name', '').lower() + ' ' +
        directory.get('description', '').lower() + ' ' +
        directory.get('notes', '').lower()
    )
    
    # Check if any review keyword is in the text
    for keyword in review_keywords:
        if keyword in text_to_check:
            return True
    
    # Also check if it's already tagged as Review Directory
    types = normalize_type(directory.get('type'))
    if 'Review Directory' in types:
        return True
    
    return False

def main():
    """Main function to fix directories."""
    data = load_directories()
    
    updates_made = []
    
    for entry in data['directories']:
        original_type = entry.get('type')
        
        # Normalize type to array
        types = normalize_type(original_type)
        
        # Check if should include Review Directory
        if should_include_review_directory(entry):
            if 'Review Directory' not in types:
                types.append('Review Directory')
        
        # Update the entry
        entry['type'] = types if types else ['SaaS Directory']  # Default if empty
        
        # Track changes
        if original_type != entry['type']:
            updates_made.append({
                'name': entry.get('name'),
                'id': entry.get('id'),
                'original': original_type,
                'new': entry['type']
            })
    
    # Save updated data
    with open('data/directories.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Print results
    print(f"\n{'='*80}")
    print(f"NORMALIZED DIRECTORY TYPES")
    print(f"{'='*80}\n")
    print(f"Total entries updated: {len(updates_made)}")
    print(f"\nSample updates (first 20):")
    print()
    
    for i, update in enumerate(updates_made[:20]):
        print(f"{i+1}. {update['name']}")
        print(f"   ID: {update['id']}")
        print(f"   From: {update['original']}")
        print(f"   To: {update['new']}")
        print()
    
    if len(updates_made) > 20:
        print(f"... and {len(updates_made) - 20} more entries updated")

if __name__ == '__main__':
    main()
