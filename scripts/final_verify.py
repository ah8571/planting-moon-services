#!/usr/bin/env python3
import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / "data"
with open(data_dir / "guest-posts.json") as f:
    d = json.load(f)

posts = d["guestPosts"]
print(f'Total entries: {len(posts)}')

multi = [p for p in posts if len(p.get("listedOn", [])) > 1]
print(f'Multi-source entries: {len(multi)}')

sources = {}
for p in posts:
    for s in p.get("listedOn", []):
        sources[s] = sources.get(s, 0) + 1

print(f'\nSources ranking:')
for s in sorted(sources.keys(), key=lambda x: sources[x], reverse=True):
    print(f'  {s}: {sources[s]}')

# Count entries by DR status
with_dr = [p for p in posts if p.get("dr") is not None]
without_dr = [p for p in posts if p.get("dr") is None]
print(f'\nDR Status:')
print(f'  Entries with DR: {len(with_dr)}')
print(f'  Entries without DR (webseotrends): {len(without_dr)}')

# Show some multi-source examples
print(f'\nMulti-source entries (sample):')
for p in multi[:10]:
    print(f'  • {p["name"]} (DR {p.get("dr", "N/A")}): {p["listedOn"]}')

# Count multi-source by source
webseotrends_multi = [p for p in posts if "webseotrends.com" in p.get("listedOn", []) and len(p.get("listedOn", [])) > 1]
print(f'\nWebseotrends multi-source entries: {len(webseotrends_multi)}')
if webseotrends_multi:
    print(f'  Examples:')
    for p in webseotrends_multi[:5]:
        print(f'    • {p["name"]}: {p["listedOn"]}')
