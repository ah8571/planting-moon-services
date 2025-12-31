#!/usr/bin/env python3
"""
Script to merge SaaSPedia directories into directories.json
"""

import json
import re

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

# SaaSPedia directories
SAASPEDIA_DATA = """
Quora	A platform for asking questions and sharing knowledge.
Startup Europe	A network for supporting and connecting European startups.
Site Like	A directory for discovering and adding similar websites.
G2	A peer-to-peer review site for software and services.
Sprout24	A platform to submit and discover marketing and tech tools.
SaaSworthy	A resource for finding and reviewing SaaS products.
Viesearch	A human-edited search engine and directory.
AffordHunt	A directory for finding affordable products and services.
SaaSHub	A community-driven SaaS comparison site.
Product Hunt	A platform to discover new products and startups.
Web3Canvas	A submission platform for web3 tools and resources.
Free Listing	A free business directory listing site.
PitchWall	A platform for showcasing and discovering startup pitches.
SaaSGenius	A review site for SaaS products and services.
Serchen	A marketplace for business software and services.
10 Words	A concise review platform for apps and tools.
9Sites	A directory for adding and discovering new websites.
Software Advice	A platform for software recommendations and reviews.
GetApp	A service for discovering and comparing business software.
BetaList	A place to find and get early access to new startups.
TechPluto	A site for submitting and reading about tech startups.
Startup Buffer	A platform to promote and discover new startups.
App Marketing Plus	A service for free app reviews and marketing.
CoStartup	A directory and resource platform for startups.
Active Search Results	A search engine and directory submission site.
Devpost	A community for developers to showcase their projects and participate in hackathons.
American Inno	A platform for posting and reading about local startups.
Ecommerce Stack	A resource for discovering e-commerce tools and platforms.
GrowthHackers	A community for growth hacking and marketing strategies.
Indie Hackers	A forum for independent developers and entrepreneurs.
Hot Scripts	A directory for finding and submitting web scripts and software.
Uneed Best	A platform for discovering and submitting useful tools.
Pinterest	A visual discovery engine for finding and sharing ideas.
A2Z AI Tools	A directory for AI tools and submissions.
F6S	A network for founders to get free deals, resources, and funding.
Pandia	A search engine and directory platform.
AI Top Picks	A site for discovering and submitting top AI tools.
Appiod	A submission platform for app reviews and features.
Apps400	A site to submit and review mobile applications.
Startup Tracker	A crowdsourced directory for tracking startups.
List.ly	A platform for creating and sharing lists.
Tally	A form-building tool for creating and managing surveys and forms.
Webwiki	A website directory and review platform.
AI Tools Directory	A directory for submitting and discovering AI tools.
Growth Junkie	A platform for adding and finding marketing tools.
No Code Devs	A community for no-code development and tools.
Find Us Here	A global business directory.
Startup Guys	A platform for startup news and submissions.
Paggu	A resource site for entrepreneurs and startups.
AI Finder	A directory for AI tools and submissions.
AI Tool Bee	A platform for submitting and discovering AI tools.
Once Tools	A directory for useful tools and software.
SaaS Directory	A directory for SaaS products and tools.
Interested in AI	A platform for submitting and discovering AI tools.
Inside AI	A site for submitting and finding AI tools.
Side Projectors	A marketplace for buying and selling side projects.
SiliconANGLE	A news site covering technology and startups.
Silicon Allee	A community for startups and tech in Berlin.
New Startups	A platform for submitting and discovering new startups.
AppsListo	A submission site for app reviews and features.
AI Tool UK	A platform for submitting AI tools.
AppsThunder	A site for submitting and reviewing mobile applications.
Sonic Run	A site for music promotion and submissions.
StackShare	A platform to see and share software stacks.
StartupBlink	A global startup ecosystem map and research center.
Business Software	A resource for finding and comparing business software.
Startup Collections	A site for submitting and discovering startup products.
Startup Hero	A platform for startups to get visibility and support.
Startup Ranking	A directory ranking startups based on various metrics.
Startup Roulette	A platform for startups to connect with investors.
Reviews Consumer Reports	A review site for products and services.
Startup ANZ	A platform for startups in Australia and New Zealand.
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

def create_new_entry(name, description):
    """Create a new directory entry from SaaSPedia data"""
    notes = f'Description from SaaSPedia: "{description}"\nURL and other details not available from source.'
    return {
        "id": name_to_id(name),
        "name": name,
        "url": "",
        "description": description,
        "type": "Software Directory",
        "domainRating": "unknown",
        "submissionType": "unknown",
        "followType": "unknown",
        "listedOn": ["saaspedia.io"],
        "notes": notes
    }

def parse_saaspedia():
    """Parse SaaSPedia data"""
    entries = []
    for line in SAASPEDIA_DATA.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Split by tab
        parts = line.split('\t')
        if len(parts) >= 2:
            name = parts[0].strip()
            description = parts[1].strip()
            if name:
                entries.append({'name': name, 'description': description})
    
    return entries

def main():
    print("Parsing SaaSPedia directories...")
    saaspedia_entries = parse_saaspedia()
    print(f"Parsed {len(saaspedia_entries)} entries")
    
    print("Loading existing directories...")
    data = load_existing()
    print(f"Currently have {len(data['directories'])} directories")
    
    new_count = 0
    updated_count = 0
    already_had = 0
    
    print("\nProcessing entries...")
    for entry in saaspedia_entries:
        existing = find_matching_entry(entry['name'], data)
        
        if existing:
            already_had += 1
            # Update listedOn if not already there
            if "saaspedia.io" not in existing['listedOn']:
                existing['listedOn'].append("saaspedia.io")
                updated_count += 1
            # Update description if empty and we have one
            if not existing['description'] and entry['description']:
                existing['description'] = entry['description']
        else:
            # Add new entry
            new_entry = create_new_entry(entry['name'], entry['description'])
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

if __name__ == "__main__":
    main()
