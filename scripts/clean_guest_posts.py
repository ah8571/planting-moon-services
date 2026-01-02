import json
from difflib import SequenceMatcher
import re

# Load guest posts data
with open('data/guest-posts.json', 'r') as f:
    data = json.load(f)

guest_posts = data['guestPosts']

print(f"Starting with {len(guest_posts)} entries")

# Step 1: Remove entries that ONLY have amazeinstitute.co.in as source
before_removal = len(guest_posts)
guest_posts = [post for post in guest_posts if not (
    post.get('listedOn') and 
    len(post['listedOn']) == 1 and 
    post['listedOn'][0] == 'amazeinstitute.co.in'
)]
print(f"Removed {before_removal - len(guest_posts)} entries with only amazeinstitute.co.in")

# Step 2: Normalize names for duplicate detection
def normalize_name(name):
    """Normalize name for comparison"""
    name = name.lower().strip()
    # Remove common variations
    name = re.sub(r'\.com|\.org|\.net|\.co\.uk', '', name)
    name = re.sub(r'\s+', ' ', name)  # Normalize whitespace
    name = re.sub(r'[®™]', '', name)  # Remove symbols
    return name

# Step 3: Find and merge duplicates
def similar(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a, b).ratio()

# Group by normalized name
name_groups = {}
for post in guest_posts:
    norm_name = normalize_name(post['name'])
    if norm_name not in name_groups:
        name_groups[norm_name] = []
    name_groups[norm_name].append(post)

# Merge duplicates
merged_posts = []
processed_indices = set()

for norm_name, posts_group in name_groups.items():
    if len(posts_group) == 1:
        merged_posts.append(posts_group[0])
    else:
        # Merge multiple entries
        print(f"\nMerging {len(posts_group)} entries for: {norm_name}")
        for i, post in enumerate(posts_group):
            print(f"  {i+1}. {post['name']} (DR: {post.get('dr', 'No DR')}, Sources: {', '.join(post.get('listedOn', []))})")
        
        # Use the entry with highest DR as base
        base_post = max(posts_group, key=lambda x: x.get('dr') or -1)
        
        # Merge all sources from all duplicates
        all_sources = set()
        for post in posts_group:
            all_sources.update(post.get('listedOn', []))
        
        # Merge niches
        all_niches = set()
        for post in posts_group:
            all_niches.update(post.get('niche', []))
        
        # Create merged entry
        merged = base_post.copy()
        merged['listedOn'] = sorted(list(all_sources))
        merged['niche'] = sorted(list(all_niches)) if all_niches else base_post.get('niche', [])
        
        print(f"  → Merged as: {merged['name']} (DR: {merged.get('dr', 'No DR')}, Sources: {len(merged['listedOn'])})")
        
        merged_posts.append(merged)

print(f"\nAfter merging: {len(merged_posts)} entries (removed {len(guest_posts) - len(merged_posts)} duplicates)")

# Step 4: Remove amazeinstitute.co.in from all source lists (keep other sources)
for post in merged_posts:
    if 'listedOn' in post and post['listedOn']:
        post['listedOn'] = [s for s in post['listedOn'] if s != 'amazeinstitute.co.in']

# Sort by DR
merged_posts.sort(key=lambda x: x.get('dr') or -1, reverse=True)

# Update data
data['guestPosts'] = merged_posts

# Save cleaned data
with open('data/guest-posts.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Cleaned guest posts saved!")
print(f"Final count: {len(merged_posts)} unique entries")

# Stats
with_amazeinstitute = len([p for p in merged_posts if 'amazeinstitute.co.in' in p.get('listedOn', [])])
print(f"Entries still containing amazeinstitute.co.in (with other sources): {with_amazeinstitute}")
