import json
from collections import Counter

# Load both files
guest_posts = json.load(open('data/guest-posts.json'))['guestPosts']
directories = json.load(open('data/directories.json'))['directories']

# Collect all niches
all_niches = []
for item in guest_posts:
    all_niches.extend(item.get('niche', []))
for item in directories:
    all_niches.extend(item.get('niche', []))

# Count and sort
niche_counts = Counter(all_niches)
sorted_niches = sorted(niche_counts.items(), key=lambda x: x[1], reverse=True)

print(f"Total unique niches remaining: {len(niche_counts)}\n")
print("All categories (sorted by frequency):")
for niche, count in sorted_niches:
    print(f"  {niche}: {count}")
