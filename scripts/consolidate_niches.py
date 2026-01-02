#!/usr/bin/env python3
"""
Consolidate niche categories to optimal master categories
Applies mapping to both guest-posts.json and directories.json
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Define the consolidation mapping
NICHE_MAPPING = {
    # Education (22 items)
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
    'education': 'Education',
    'self improvement': 'Education',
    'productivity': 'Education',
    'books': 'Education',
    'stories': 'Education',
    'college': 'Education',
    'higher education': 'Education',
    'how-to': 'Education',
    'how to': 'Education',
    'self-help': 'Education',
    'personal development': 'Education',
    'expertise': 'Education',
    'experts': 'Education',
    'presentations': 'Education',
    'planning': 'Education',
    
    # Development (28 items)
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
    'development': 'Development',
    'technology': 'Development',
    'tech': 'Development',
    'saas': 'Development',
    'it': 'Development',
    'security': 'Development',
    'web hosting': 'Development',
    'infrastructure': 'Development',
    'data science': 'Development',
    'software': 'Development',
    'crm': 'Development',
    'cms': 'Development',
    'analytics': 'Development',
    'big data': 'Development',
    'data': 'Development',
    'monitoring': 'Development',
    'technical seo': 'Development',
    'testing': 'Development',
    'qa': 'Development',
    'css': 'Development',
    'mobile': 'Development',
    'mobile apps': 'Development',
    'indie developers': 'Development',
    'shopify': 'Development',
    'data-driven': 'Development',
    'conversion': 'Development',
    'telecommunications': 'Development',
    'conversion optimization': 'Development',
    'conversion rate optimization': 'Development',
    'optimization': 'Development',
    
    # Design (9 items)
    'web design': 'Design',
    'ux design': 'Design',
    'graphic design': 'Design',
    'interior design': 'Design',
    'logo': 'Design',
    'icons': 'Design',
    'diagramming': 'Design',
    'themes': 'Design',
    'design': 'Design',
    'cro': 'Design',
    'a/b testing': 'Design',
    'uX': 'Design',
    
    # Marketing (44 items)
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
    'blogging': 'Marketing',
    'content': 'Marketing',
    'writing': 'Marketing',
    'guest posting': 'Marketing',
    'publishing': 'Marketing',
    'marketing technology': 'Marketing',
    'martech': 'Marketing',
    'digital advertising': 'Marketing',
    'advertising': 'Marketing',
    'ppc': 'Marketing',
    'product marketing': 'Marketing',
    'market research': 'Marketing',
    'link building': 'Marketing',
    'digital pr': 'Marketing',
    'pr': 'Marketing',
    'content publishing': 'Marketing',
    'content discovery': 'Marketing',
    'content curation': 'Marketing',
    'curation': 'Marketing',
    'copywriting': 'Marketing',
    'email': 'Marketing',
    'video marketing': 'Marketing',
    'branding': 'Marketing',
    'personal branding': 'Marketing',
    'news aggregation': 'Marketing',
    'journalism': 'Marketing',
    'links': 'Marketing',
    'growth': 'Marketing',
    'make money': 'Marketing',
    'make money online': 'Marketing',
    'sales': 'Marketing',
    'reseller': 'Marketing',
    'online business': 'Marketing',
    
    # Social Media (12 items)
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
    'professional': 'Social Media',
    'media': 'Social Media',
    'social network': 'Social Media',
    'social bookmarking': 'Social Media',
    'messaging': 'Social Media',
    'community development': 'Social Media',
    'collaboration': 'Social Media',
    'q&a': 'Social Media',
    
    # E-Commerce (4 items)
    'ecommerce': 'E-Commerce',
    'shopping': 'E-Commerce',
    'retail': 'E-Commerce',
    'dropshipping': 'E-Commerce',
    
    # Finance (7 items)
    'finance': 'Finance',
    'accounting': 'Finance',
    'business finance': 'Finance',
    'investment': 'Finance',
    'cryptocurrency': 'Finance',
    'payments': 'Finance',
    'personal finance': 'Finance',
    'investing': 'Finance',
    'saving': 'Finance',
    'expense management': 'Finance',
    'real estate': 'Finance',
    
    # Health & Wellness (15 items)
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
    'lifestyle': 'Health & Wellness',
    'psychology': 'Health & Wellness',
    'events': 'Health & Wellness',
    'identity': 'Health & Wellness',
    'meditation': 'Health & Wellness',
    'medical': 'Health & Wellness',
    'medicine': 'Health & Wellness',
    
    # Creative (11 items)
    'creative': 'Creative',
    'photography': 'Creative',
    'illustration': 'Creative',
    'stock images': 'Creative',
    'visual': 'Creative',
    'inspiration': 'Creative',
    'art': 'Creative',
    'arts': 'Creative',
    'creativity': 'Creative',
    'culture': 'Creative',
    'entertainment': 'Creative',
    'music': 'Creative',
    'infographics': 'Creative',
    'energy': 'Creative',
    
    # Open Source (4 items)
    'open source': 'Open Source',
    'wiki': 'Open Source',
    'software reviews': 'Open Source',
    'tech news': 'Open Source',
    
    # Home Improvement (5 items)
    'home decor': 'Home Improvement',
    'home improvement': 'Home Improvement',
    'hosting': 'Home Improvement',
    'gardening': 'Home Improvement',
    'food': 'Home Improvement',
    'diy': 'Home Improvement',
    
    # Business (36 items)
    'business': 'Business',
    'entrepreneurship': 'Business',
    'startups': 'Business',
    'management': 'Business',
    'project management': 'Business',
    'team building': 'Business',
    'team communication': 'Business',
    'assessment': 'Business',
    'appointments': 'Business',
    'appointment scheduling': 'Business',
    'innovation': 'Business',
    'outreach': 'Business',
    'remote work': 'Business',
    'reviews': 'Business',
    'portfolio': 'Business',
    'domains': 'Business',
    'surveys': 'Business',
    'community': 'Business',
    'news': 'Business',
    'video': 'Business',
    'freelance': 'Business',
    'freelance writing': 'Business',
    'customer support': 'Business',
    'customer service': 'Business',
    'customer experience': 'Business',
    'customer feedback': 'Business',
    'customer engagement': 'Business',
    'agencies': 'Business',
    'newsletters': 'Business',
    'launch': 'Business',
    'products': 'Business',
    'markets': 'Business',
    'workflow': 'Business',
    'communication': 'Business',
    'reputation': 'Business',
    'reputation management': 'Business',
    'b2b': 'Business',
    'business tools': 'Business',
    'tools': 'Business',
    'jobs': 'Business',
    'hr': 'Business',
    'recruiting': 'Business',
    'small business': 'Business',
    'career advice': 'Business',
    'policy': 'Business',
    'business process management': 'Business',
    'business tech': 'Business',
    'local': 'Business',
    
    # Legal (3 items)
    'law': 'Legal',
    'legal': 'Legal',
    'compliance': 'Legal',
    
    # Nonprofit (2 items)
    'nonprofit': 'Nonprofit',
    'charity': 'Nonprofit',
    
    # International (4 items)
    'india': 'International',
    'malaysia': 'International',
    'asia': 'International',
    'australia': 'International',
    
    # Standalone (9 items)
    'automobiles': 'Automobiles',
    'automotive': 'Automobiles',
    'politics': 'Politics',
    'directory': 'Directory',
    'classified': 'Classified',
    'fashion': 'Fashion',
    'gaming': 'Gaming',
    'military': 'Military',
    'careers': 'Careers',
    'motivation': 'Motivation',
    'science': 'Science',
    'pdfs': 'Business',
    'ux': 'Design',
    'cx': 'Design',
    'analysis': 'Business',
    'coupons': 'Marketing',
    'digital business': 'Business',
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
            # If not in mapping, check if it should be removed
            if normalized not in ['general', 'success', 'documents', 'collections', 'alternatives', 'google', 'contests']:
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
    modified_count = 0
    
    for item in items:
        if 'niche' in item and item['niche']:
            original_niches = item['niche'].copy() if isinstance(item['niche'], list) else [item['niche']]
            consolidated = consolidate_niches(original_niches)
            
            if consolidated != original_niches:
                consolidation_stats[f"{len(original_niches)} → {len(consolidated)}"] += 1
                modified_count += 1
            else:
                unchanged_count += 1
            
            item['niche'] = consolidated
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  Total items processed: {len(items)}")
    print(f"  Items modified: {modified_count}")
    print(f"  Items unchanged: {unchanged_count}")
    if consolidation_stats:
        print(f"  Consolidation patterns:")
        for pattern, count in sorted(consolidation_stats.items()):
            print(f"    {pattern}: {count} items")
    
    return len(items), modified_count

def main():
    base_path = Path(__file__).parent.parent
    
    files_to_process = [
        base_path / 'data' / 'guest-posts.json',
        base_path / 'public' / 'data' / 'guest-posts.json',
        base_path / 'data' / 'directories.json',
        base_path / 'public' / 'data' / 'directories.json',
    ]
    
    print("=" * 60)
    print("NICHE CONSOLIDATION: 171+ categories → 19 optimized categories")
    print("=" * 60)
    
    total_items = 0
    total_modified = 0
    
    for filepath in files_to_process:
        if filepath.exists():
            items, modified = process_file(filepath)
            total_items += items
            total_modified += modified
        else:
            print(f"\nSkipping (not found): {filepath}")
    
    print("\n" + "=" * 60)
    print("CONSOLIDATION COMPLETE")
    print("=" * 60)
    print(f"Total items processed: {total_items}")
    print(f"Total items modified: {total_modified}")
    print(f"\nMaster categories (13):")
    print(f"  1. Education")
    print(f"  2. Development")
    print(f"  3. Design")
    print(f"  4. Marketing")
    print(f"  5. Social Media")
    print(f"  6. E-Commerce")
    print(f"  7. Finance")
    print(f"  8. Health & Wellness")
    print(f"  9. Creative")
    print(f"  10. Open Source")
    print(f"  11. Home Improvement")
    print(f"  12. Business")
    print(f"  13. Legal")
    print(f"\nStandalone categories (6):")
    print(f"  - Automobiles")
    print(f"  - Politics")
    print(f"  - Directory")
    print(f"  - Classified")
    print(f"  - International")
    print(f"  - Nonprofit")
    print(f"\nSpecialty categories (9):")
    print(f"  - Fashion")
    print(f"  - Gaming")
    print(f"  - Military")
    print(f"  - Careers")
    print(f"  - Motivation")
    print(f"  - Science")

if __name__ == '__main__':
    main()
