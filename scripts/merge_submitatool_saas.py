#!/usr/bin/env python3
"""
Script to merge Submit a Tool top SaaS directories into directories.json
This is the top 75 SaaS directories from submitatool.com/dir/saas
"""

import json
import re

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

# Top SaaS Directories from Submit a Tool
SUBMITATOOL_SAAS = """
Product Hunt
Hacker News
BetaList
Indie Hackers
SaaS Hub
Capterra
G2
GetApp
AlternativeTo
SaaSworthy
DiscoverCloud
Startup Stash
Launching Next
Beta Page
Startup Ranking
Killer Startups
Startup Lift
Tech Pluto
Crunchbase
AngelList
F6S
SaaS Directory
Software Suggest
AppSumo
Stack Share
SaaS Genius
MicroStartups
Startup Buffer
SaaS Mag
CloudWays
SaaS Boomi
Pitchwall
Startup Tracker
Early Stage
The Startup Pitch
Startup Collections
Launch Lister
Startup Beat
NextBigWhat
EU-Startups
Startup Xplore
Startup Inspire
Side Projectors
Startup Resources
The Startup INC
Startup Radar
Get Worm
My Startup Tool
Launched
StartupBlink
Software World
SaaS Venture
GrowthHackers
Remote Tools
Startup Grind
SaaS Scout
Wellfound
Startup List
Bizz.dev
SaaS AI Tools
Startups.fyi
Tech Directory
Tiny Startups
WebWiki
Slant
Museum of Websites
All Top Startups
StartupBase
Startup Ideas
YourStory
TechCrunch
VentureBeat
The Next Web
SaaS Review
"""

def name_to_id(name):
    """Convert name to ID"""
    name_lower = name.lower().strip()
    id_str = re.sub(r'[^a-z0-9]', '-', name_lower)
    id_str = re.sub(r'-+', '-', id_str)
    id_str = id_str.strip('-')
    return id_str[:50]

def load_existing():
    """Load existing directories.json"""
    with open(DIRS_PATH, 'r') as f:
        return json.load(f)

def find_matching_entry(name, existing_data):
    """Find if this entry already exists by name"""
    name_lower = name.lower()
    for d in existing_data['directories']:
        if d['name'].lower() == name_lower:
            return d
    return None

def create_new_entry(name):
    """Create a new directory entry from Submit a Tool SaaS data"""
    return {
        "id": name_to_id(name),
        "name": name,
        "url": "",
        "description": "",
        "type": "Software Directory",
        "domainRating": "unknown",
        "submissionType": "unknown",
        "followType": "unknown",
        "listedOn": ["submitatool.com"],
        "notes": "Top SaaS directory from SubmitATool.com. URL and other details not available from source."
    }

def main():
    print("Parsing Submit a Tool top SaaS directories...")
    saas_names = [line.strip() for line in SUBMITATOOL_SAAS.strip().split('\n') if line.strip()]
    print(f"Parsed {len(saas_names)} directory names")
    
    print("Loading existing directories...")
    data = load_existing()
    print(f"Currently have {len(data['directories'])} directories")
    
    new_count = 0
    updated_count = 0
    already_had = 0
    
    print("\nProcessing entries...")
    for name in saas_names:
        existing = find_matching_entry(name, data)
        
        if existing:
            already_had += 1
            # Update listedOn if not already there
            if "submitatool.com" not in existing['listedOn']:
                existing['listedOn'].append("submitatool.com")
                updated_count += 1
        else:
            # Add new entry
            new_entry = create_new_entry(name)
            data['directories'].append(new_entry)
            new_count += 1
    
    print(f"\n=== Results ===")
    print(f"Already in database: {already_had}")
    print(f"New entries added: {new_count}")
    print(f"Existing entries updated (source): {updated_count}")
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nUpdated directories.json!")
    print(f"Total directories now: {len(data['directories'])}")
    
    # Show newly added
    if new_count > 0:
        print(f"\n=== New directories added ===")
        # Find the new ones
        new_names = [n for n in saas_names if not find_matching_entry(n, load_existing())]
        for name in new_names[:10]:
            print(f"  - {name}")
        if len(new_names) > 10:
            print(f"  ... and {len(new_names) - 10} more")

if __name__ == "__main__":
    main()
