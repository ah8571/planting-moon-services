#!/usr/bin/env python3
"""
Script to merge Submit a Tool AI directories into directories.json
This source has actual Domain Rating data, which is valuable
"""

import json
import re

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

# Submit a Tool data
SUBMITATOOL_DATA = """
Source Forge	92
AI Tools Neil Patel	91
AI Infinity	90
Startup88	88
FinancesOnline	87
F6S	86
Your Story	86
AlternativeTo	80
Crunchbase	80
Stackshare	79
Webwiki	77
Alternative	77
Digital Agency Network	76
EU Startups	76
Software World	75
Product Hunt	75
SaasWorthy	72
Getlatka	71
Sitelike	70
Beta List	70
SaasHub	68
SideProjectors	67
Startup Ranking	67
Pitchwall	64
Submission Web Directory	64
SoMuch	64
Marketing Internet Directory	61
GPTs Hunter	59
KitPloit	57
Afford Hunt	56
Business Software	55
AITOOLS	53
FiveTaco	53
uneed	52
Tool Pilot	51
Launching Next	51
Startup Base	50
TechPluto	47
EZWeb Directory	47
Ismailblogger	46
Future Tools	44
Hacker News	44
StartupTracker	44
Tiny Startups	44
100L5	41
Insidr AI	40
Resource fyi	39
Ben's Bites News	39
Startup Buffer	39
AlterOpen	39
Launched	38
AI Library	38
ToolsFine	38
Dockey AI	37
Paggu	35
BroUseAI	35
PromoteProject	34
Startup Lister	33
AllStartups Info	33
Anyfp	33
Saas AI Tools	33
Robingood	33
Crazy About Startups	33
That AI Collection	32
AI Tool guru	31
Open Future	31
DEV Resources	31
Mars AI directory	30
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

def create_new_entry(name, dr):
    """Create a new directory entry from Submit a Tool data"""
    return {
        "id": name_to_id(name),
        "name": name,
        "url": "",
        "description": "",
        "type": "AI Directory",
        "domainRating": dr,
        "submissionType": "unknown",
        "followType": "unknown",
        "listedOn": ["submitatool.com"],
        "notes": "AI Directory from SubmitATool.com. URL and submission type not available from source."
    }

def parse_submitatool():
    """Parse Submit a Tool data"""
    entries = []
    for line in SUBMITATOOL_DATA.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Split by tab
        parts = line.split('\t')
        if len(parts) >= 2:
            name = parts[0].strip()
            try:
                dr = int(parts[1].strip())
                if name:
                    entries.append({'name': name, 'dr': dr})
            except ValueError:
                continue
    
    return entries

def main():
    print("Parsing Submit a Tool AI directories...")
    submitatool_entries = parse_submitatool()
    print(f"Parsed {len(submitatool_entries)} entries")
    
    print("Loading existing directories...")
    data = load_existing()
    print(f"Currently have {len(data['directories'])} directories")
    
    new_count = 0
    updated_count = 0
    dr_updated_count = 0
    
    print("\nProcessing entries...")
    for entry in submitatool_entries:
        existing = find_matching_entry(entry['name'], data)
        
        if existing:
            # Update listedOn if not already there
            if "submitatool.com" not in existing['listedOn']:
                existing['listedOn'].append("submitatool.com")
                updated_count += 1
            
            # Update DR if existing had "unknown" or lower DR
            if existing['domainRating'] == "unknown" or (isinstance(existing['domainRating'], int) and existing['domainRating'] < entry['dr']):
                existing['domainRating'] = entry['dr']
                dr_updated_count += 1
        else:
            # Add new entry
            new_entry = create_new_entry(entry['name'], entry['dr'])
            data['directories'].append(new_entry)
            new_count += 1
    
    print(f"\n=== Results ===")
    print(f"New entries added: {new_count}")
    print(f"Existing entries updated (source): {updated_count}")
    print(f"DR values updated: {dr_updated_count}")
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nUpdated directories.json!")
    print(f"Total directories now: {len(data['directories'])}")

if __name__ == "__main__":
    main()
