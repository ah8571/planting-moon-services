#!/usr/bin/env python3
"""
Consolidate 265 niche categories into 15 master categories
Applies mapping to both guest-posts.json and directories.json
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Define the consolidation mapping
NICHE_MAPPING = {
    # Education (14 items)
    'e-learning': 'Education',
    'elearning': 'Education',
    'online learning': 'Education',
    'online education': 'Education',
    'course creation': 'Education',
    'teaching': 'Education',
    'learning': 'Education',
    'training': 'Education',
    'technology training': 'Education',
    'university rankings': 'Education',
    'quizzes': 'Education',
    'reading': 'Education',
    'research': 'Education',
    'thought leadership': 'Education',
    'knowledge': 'Education',
    
    # Development (16 items)
    'programming': 'Development',
    'web development': 'Development',
    'software development': 'Development',
    'coding': 'Development',
    '.net': 'Development',
    'devops': 'Development',
    'no code': 'Development',
    'cloud': 'Development',
    'vpn': 'Development',
    'web': 'Development',
    'website builder': 'Development',
    'website building': 'Development',
    'wordpress': 'Development',
    'ai': 'Development',
    'machine learning': 'Development',
    'automation': 'Development',
    
    # Design (8 items)
    'web design': 'Design',
    'ux design': 'Design',
    'graphic design': 'Design',
    'interior design': 'Design',
    'logo': 'Design',
    'icons': 'Design',
    'diagramming': 'Design',
    'themes': 'Design',
    
    # Marketing (11 items)
    'marketing': 'Marketing',
    'digital marketing': 'Marketing',
    'content marketing': 'Marketing',
    'email marketing': 'Marketing',
    'affiliate marketing': 'Marketing',
    'marketing automation': 'Marketing',
    'sem': 'Marketing',
    'seo': 'Marketing',
    'growth hacking': 'Marketing',
    'influencer marketing': 'Marketing',
    'lead generation': 'Marketing',
    
    # Social Media (11 items)
    'social media': 'Social Media',
    'social media marketing': 'Social Media',
    'instagram': 'Social Media',
    'twitter': 'Social Media',
    'linkedin': 'Social Media',
    'tiktok': 'Social Media',
    'youtube': 'Social Media',
    'facebook': 'Social Media',
    'social networking': 'Social Media',
    'bookmarking': 'Social Media',
    
    # E-Commerce (4 items)
    'ecommerce': 'E-Commerce',
    'shopping': 'E-Commerce',
    'retail': 'E-Commerce',
    'dropshipping': 'E-Commerce',
    
    # Finance (6 items)
    'finance': 'Finance',
    'accounting': 'Finance',
    'business finance': 'Finance',
    'investment': 'Finance',
    'cryptocurrency': 'Finance',
    'payments': 'Finance',
    
    # Health & Wellness (10 items)
    'health': 'Health & Wellness',
    'wellness': 'Health & Wellness',
    'fitness': 'Health & Wellness',
    'mental health': 'Health & Wellness',
    'nutrition': 'Health & Wellness',
    'recipe': 'Health & Wellness',
    'relationship': 'Health & Wellness',
    'spirituality': 'Health & Wellness',
    'sports': 'Health & Wellness',
    'travel': 'Health & Wellness',
    
    # Creative (5 items)
    'creative': 'Creative',
    'photography': 'Creative',
    'illustration': 'Creative',
    'stock images': 'Creative',
    'visual': 'Creative',
    
    # Open Source (2 items)
    'open source': 'Open Source',
    'wiki': 'Open Source',
    
    # Home Improvement (4 items)
    'home decor': 'Home Improvement',
    'home improvement': 'Home Improvement',
    'hosting': 'Home Improvement',
    
    # Business (16 items)
    'business': 'Business',
    'entrepreneurship': 'Business',
    'startups': 'Business',
    'management': 'Business',
    'project management': 'Business',
    'team building': 'Business',
    'team communication': 'Business',
    'assessment': 'Business',
    'appointments': 'Business',
    'innovation': 'Business',
    'outreach': 'Business',
    'remote work': 'Business',
    'reviews': 'Business',
    'portfolio': 'Business',
    'domains': 'Business',
    'surveys': 'Business',
    
    # Standalone (3 items)
    'nonprofit': 'Nonprofit',
    'directory': 'Directory',
    'automobiles': 'Automobiles',
}

def normalize_niche(niche):
    """Normalize niche name for mapping lookup"""
    return niche.strip().lower()

def consolidate_niches(niches_list):
    """Consolidate a list of niches into master categories"""
    if not niches_list:
        return []
    
    consolidated = set()
    unmapped = []
    
    for niche in niches_list:
        normalized = normalize_niche(niche)
        if normalized in NICHE_MAPPING:
            consolidated.add(NICHE_MAPPING[normalized])
        else:
            # If not in mapping, check if it should be removed (General, Success, etc.)
            if normalized not in ['general', 'success', 'documents', 'collections', 'alternatives']:
                unmapped.append(niche)
    
    # Combine consolidated categories with any unmapped ones that aren't in the removal list
    result = list(consolidated) + unmapped
    return sorted(result)

def process_file(filepath):
    """Process a JSON file and consolidate niches"""
    print(f"\nProcessing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Determine if this is guest-posts or directories format
    if 'guestPosts' in data:
        items = data['guestPosts']
    elif 'directories' in data:
        items = data['directories']
    elif 'saasdirectories' in data:
        items = data['saasdirectories']
    else:
        # Assume it's a list of items
        items = data if isinstance(data, list) else []
    
    consolidation_stats = defaultdict(int)
    unchanged_count = 0
    
    for item in items:
        if 'niche' in item and item['niche']:
            original_niches = item['niche'].copy() if isinstance(item['niche'], list) else [item['niche']]
            consolidated = consolidate_niches(original_niches)
            
            if consolidated != original_niches:
                consolidation_stats[f"{len(original_niches)} → {len(consolidated)}"] += 1
            else:
                unchanged_count += 1
            
            item['niche'] = consolidated
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  Total items processed: {len(items)}")
    print(f"  Items with unchanged niches: {unchanged_count}")
    print(f"  Consolidation patterns:")
    for pattern, count in sorted(consolidation_stats.items()):
        print(f"    {pattern}: {count} items")
    
    return len(items), unchanged_count

def main():
    base_path = Path(__file__).parent.parent
    
    files_to_process = [
        base_path / 'data' / 'guest-posts.json',
        base_path / 'public' / 'data' / 'guest-posts.json',
        base_path / 'data' / 'directories.json',
        base_path / 'public' / 'data' / 'directories.json',
    ]
    
    print("=" * 60)
    print("NICHE CONSOLIDATION: 265 categories → 15 master categories")
    print("=" * 60)
    
    total_items = 0
    total_unchanged = 0
    
    for filepath in files_to_process:
        if filepath.exists():
            items, unchanged = process_file(filepath)
            total_items += items
            total_unchanged += unchanged
        else:
            print(f"\nSkipping (not found): {filepath}")
    
    print("\n" + "=" * 60)
    print("CONSOLIDATION COMPLETE")
    print("=" * 60)
    print(f"Total items processed: {total_items}")
    print(f"Master categories now: 15")
    print(f"  - Education")
    print(f"  - Development")
    print(f"  - Design")
    print(f"  - Marketing")
    print(f"  - Social Media")
    print(f"  - E-Commerce")
    print(f"  - Finance")
    print(f"  - Health & Wellness")
    print(f"  - Creative")
    print(f"  - Open Source")
    print(f"  - Home Improvement")
    print(f"  - Business")
    print(f"  - Nonprofit")
    print(f"  - Directory")
    print(f"  - Automobiles")

if __name__ == '__main__':
    main()
