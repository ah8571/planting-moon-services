import json

# Load cleaned guest posts data
with open('data/guest-posts.json', 'r') as f:
    data = json.load(f)

guest_posts = data['guestPosts']

print(f"Starting with {len(guest_posts)} entries\n")

# Manual duplicate mappings (list of lists - entries to merge)
duplicate_groups = [
    # Gimmio variations
    ["Gimm.io Blog", "Gimmio Blog", "Gimmio.in"],
    # GetResponse variations
    ["GetResponse", "GetResponse Blog"],
    # Geek Estate variations
    ["Geek Estate Blog", "GeekEstateBlog.com"],
    # Linkody variations
    ["Linkody", "Linkody Blog"],
    # Make a Living Writing variations
    ["Make a Living Writing", "MakeALivingWriting.com"],
    # Oil Price variations
    ["Oil Price", "OilPrice.com"],
    # MarketingTech variations
    ["MarketingTech", "MarketingTechNews", "MarTech Series", "MarTech Today"],
    # Politico variations
    ["Politico", "POLITICO Magazine"],
    # OpenDemocracy variations
    ["open Democracy", "OpenDemocracy"],
    # Omniconvert variations
    ["Omniconvert", "Omniconvert blog"],
    # Serpstat variations
    ["Serpstat Blog", "SerpStat.com"],
    # Sociable Blog variations
    ["Sociable Blog", "Sociableblog.com"],
    # SoftwareWorld variations
    ["SoftwareWorld", "SoftwareWorld.co"],
    # Startup Info variations
    ["Startup Info", "Startup.info"],
]

def normalize_for_matching(name):
    """Normalize name for matching"""
    import re
    name = name.lower().strip()
    name = re.sub(r'\.com|\.co|\.in|\.info', '', name)
    name = re.sub(r'\s+', '', name)  # Remove all whitespace
    return name

# Build a map of normalized names to actual entries
name_to_entries = {}
for post in guest_posts:
    norm = normalize_for_matching(post['name'])
    if norm not in name_to_entries:
        name_to_entries[norm] = []
    name_to_entries[norm].append(post)

# Merge duplicates
merged_posts = []
processed_posts = set()

for group in duplicate_groups:
    # Find all entries matching this group
    entries_in_group = []
    for variant_name in group:
        norm = normalize_for_matching(variant_name)
        if norm in name_to_entries:
            for entry in name_to_entries[norm]:
                entry_id = id(entry)
                if entry_id not in processed_posts:
                    entries_in_group.append(entry)
                    processed_posts.add(entry_id)
    
    if len(entries_in_group) > 1:
        print(f"Merging {len(entries_in_group)} entries for: {group[0]}")
        for i, entry in enumerate(entries_in_group):
            print(f"  {i+1}. {entry['name']} (DR: {entry.get('dr', 'No DR')}, Sources: {', '.join(entry.get('listedOn', []))})")
        
        # Use the entry with highest DR as base
        base_post = max(entries_in_group, key=lambda x: x.get('dr') or -1)
        
        # Merge all sources
        all_sources = set()
        for post in entries_in_group:
            all_sources.update(post.get('listedOn', []))
        
        # Merge niches
        all_niches = set()
        for post in entries_in_group:
            all_niches.update(post.get('niche', []))
        
        # Create merged entry
        merged = base_post.copy()
        merged['listedOn'] = sorted(list(all_sources))
        merged['niche'] = sorted(list(all_niches)) if all_niches else base_post.get('niche', [])
        
        print(f"  Merged as: {merged['name']} (DR: {merged.get('dr', 'No DR')}, Sources: {len(merged['listedOn'])})\n")
        
        merged_posts.append(merged)

# Add all remaining posts that weren't merged
for post in guest_posts:
    if id(post) not in processed_posts:
        merged_posts.append(post)

# Sort by DR
merged_posts.sort(key=lambda x: x.get('dr') or -1, reverse=True)

print(f"After merging: {len(merged_posts)} entries (removed {len(guest_posts) - len(merged_posts)} more duplicates)\n")

# Update data
data['guestPosts'] = merged_posts

# Save cleaned data
with open('data/guest-posts.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Cleaned guest posts saved!")
print(f"Final count: {len(merged_posts)} unique entries")
