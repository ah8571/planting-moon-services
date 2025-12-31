#!/usr/bin/env python3
"""
Script to add new AMRYTT entries to directories.json
"""

import json
import re

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

# AMRYTT entries (just the new ones we found)
NEW_ENTRIES_RAW = """
1	www.patreon.com/	93
3	gumroad.com	91
4	www.deviantart.com/	91
5	www.producthunt.com/	91
8	www.gartner.com/en/digital-markets/claim-profile	91
10	news.ycombinator.com/	90
11	dev.to/	90
12	hackernoon.com/	88
13	uneed.lemonsqueezy.com/	87
14	www.scoop.it	86
16	www.f6s.com/	83
17	media-index.kochava.com/	81
18	www.indiehackers.com/	80
20	onepagelove.com/	80
21	technologyadvice.com/	79
22	list.ly/	78
23	www.eu-startups.com/	77
24	www.softwaresuggest.com/	77
25	crozdesk.com/	75
26	www.killerstartups.com/	74
27	www.saasworthy.com/	73
29	saasworthy.com	73
30	www.startus.cc/	72
31	land-book.com/	72
33	alternative.me/	72
34	www.webdesign-inspiration.com/	71
35	dynamicbusiness.com/	71
36	www.sideprojectors.com/	70
37	www.serchen.com/	70
38	www.bunity.com/	69
39	www.peerspot.com/	67
40	startupstash.com/	67
41	www.startupranking.com/	67
42	pitchwall.co/	65
43	peerlist.io/	65
44	webdesignernews.com/	64
45	indiepa.ge/discover	62
46	www.ebool.com/	61
47	toolfinder.co/	61
48	www.saasgenius.com/	59
49	devhunt.org/	58
50	fazier.com/	58
51	getmakerlog.com/	57
52	supertools.therundown.ai	57
53	www.shno.co/	57
54	www.startupguys.net/	57
55	www.spotsaas.com/	55
56	wip.co/	55
57	famewall.io/landing-tools-directory/	55
58	www.curated.design/	53
59	nocodefounders.com/	52
60	app.innmind.com/	51
61	www.alistdirectory.com/	51
62	www.launchingnext.com/submit/	48
63	cuspera.com	48
64	www.techpluto.com/	48
65	www.tinystartups.com/	47
66	www.toools.design/	45
67	nocodelist.co/	43
68	microlaunch.net/	43
69	seotoolbelt.co/	42
70	startuptracker.io/	42
"""

def url_to_id(url):
    """Convert URL to ID"""
    url = url.lower().strip()
    if url.endswith('/'):
        url = url[:-1]
    if url.startswith('www.'):
        url = url[4:]
    # Replace special chars with hyphens
    id_str = re.sub(r'[^a-z0-9]', '-', url)
    # Remove multiple hyphens
    id_str = re.sub(r'-+', '-', id_str)
    # Remove leading/trailing hyphens
    id_str = id_str.strip('-')
    return id_str[:50]  # Limit length

def url_to_name(url):
    """Convert URL to friendly name"""
    url = url.lower().strip()
    if url.endswith('/'):
        url = url[:-1]
    if url.startswith('www.'):
        url = url[4:]
    
    # Take first part before dot or slash
    name = re.split(r'[./]', url)[0]
    # Capitalize
    name = name.replace('-', ' ').title()
    return name

def guess_type(name_lower, url_lower):
    """Guess directory type based on URL"""
    if 'ycombinator' in url_lower or 'hacker' in url_lower or 'indie' in url_lower:
        return 'Community'
    if 'dev' in url_lower or 'devhunt' in url_lower:
        return 'Developer Tools'
    if 'patreon' in url_lower or 'gumroad' in url_lower:
        return 'SaaS Marketplace'
    if 'artstation' in url_lower or 'deviantart' in url_lower:
        return 'Design Directory'
    if 'producthunt' in url_lower:
        return 'Launch Platform'
    if 'gartner' in url_lower:
        return 'Review Directory'
    return 'Software Directory'

def load_existing():
    """Load existing directories.json"""
    with open(DIRS_PATH, 'r') as f:
        return json.load(f)

def create_new_entry(url, dr, num):
    """Create a new directory entry"""
    name = url_to_name(url)
    entry_id = url_to_id(url)
    url_clean = url.strip()
    if not url_clean.startswith('http'):
        url_clean = 'https://' + url_clean
    
    name_lower = name.lower()
    url_lower = url_clean.lower()
    entry_type = guess_type(name_lower, url_lower)
    
    return {
        "id": entry_id,
        "name": name,
        "url": url_clean,
        "description": f"{name} directory for SaaS and software discovery.",
        "type": entry_type,
        "domainRating": dr,
        "submissionType": "unknown",
        "followType": "unknown",
        "listedOn": ["amrytt.com"],
        "notes": "Submission type and follow type not specified in source"
    }

def main():
    print("Loading existing directories...")
    data = load_existing()
    existing_urls = {d['url'].lower() for d in data['directories']}
    
    print("Parsing new entries from AMRYTT...")
    new_entries = []
    duplicates = 0
    
    for line in NEW_ENTRIES_RAW.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 3:
            try:
                num = int(parts[0])
                url = parts[1].strip()
                dr = float(parts[2])
                
                url_clean = url if url.startswith('http') else 'https://' + url
                if url_clean.lower() not in existing_urls:
                    new_entries.append(create_new_entry(url, dr, num))
                else:
                    duplicates += 1
            except Exception as e:
                print(f"Error parsing line: {line} - {e}")
    
    print(f"\nFound {len(new_entries)} new entries to add")
    print(f"Skipped {duplicates} duplicates")
    
    # Add to JSON
    data['directories'].extend(new_entries)
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nUpdated directories.json!")
    print(f"Total directories now: {len(data['directories'])}")
    
    # Show sample
    print(f"\n=== Sample of added entries ===")
    for entry in new_entries[:5]:
        print(f"{entry['name']:30s} DR: {entry['domainRating']:6.1f} Type: {entry['type']}")

if __name__ == "__main__":
    main()
