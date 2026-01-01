#!/usr/bin/env python3
"""
Merge linkbuilder.io guest posting sites with DR values into guest-posts.json
Handles duplicate URL consolidation with source attribution.
"""

import json
from pathlib import Path
from urllib.parse import urlparse

data_dir = Path(__file__).parent.parent / "data"

# Load existing guest posts
with open(data_dir / "guest-posts.json") as f:
    main_data = json.load(f)

main_posts = main_data["guestPosts"]
print(f"Main file: {len(main_posts)} entries")

# Linkbuilder.io sites with DR values
linkbuilder_entries = [
    # First batch from list
    {"name": "ColibriWP", "url": "https://colibri.wp.com", "dr": 91, "niche": ["WordPress", "Web Design"]},
    {"name": "Entrepreneur", "url": "https://entrepreneur.com", "dr": 91, "niche": ["Entrepreneurship", "Business"]},
    {"name": "Mashable", "url": "https://mashable.com", "dr": 91, "niche": ["Technology", "Culture"]},
    {"name": "DZone", "url": "https://dzone.com", "dr": 85, "niche": ["Technology", "Development"]},
    {"name": "Recruitee", "url": "https://recruitee.com", "dr": 88, "niche": ["HR Tech", "Recruiting"]},
    {"name": "WPExplorer", "url": "https://wpexplorer.com", "dr": 85, "niche": ["WordPress", "Themes"]},
    {"name": "MarTech Today", "url": "https://martechtoday.com", "dr": 83, "niche": ["Marketing Technology"]},
    {"name": "Bplans", "url": "https://bplans.com", "dr": 80, "niche": ["Business", "Planning"]},
    {"name": "PureVPN", "url": "https://purevpn.com", "dr": 80, "niche": ["VPN", "Security"]},
    {"name": "Mitel", "url": "https://mitel.com", "dr": 79, "niche": ["Telecommunications", "Business"]},
    {"name": "Flock", "url": "https://flock.com", "dr": 78, "niche": ["Team Communication", "Messaging"]},
    {"name": "MotoCMS", "url": "https://motocms.com", "dr": 79, "niche": ["Website Builder", "CMS"]},
    {"name": "ClickUp", "url": "https://clickup.com", "dr": 87, "niche": ["Productivity", "Project Management"]},
    {"name": "Techopedia", "url": "https://techopedia.com", "dr": 88, "niche": ["Technology", "IT"]},
    {"name": "OpenSource", "url": "https://opensource.com", "dr": 83, "niche": ["Open Source", "Technology"]},
    {"name": "Outbrain", "url": "https://outbrain.com", "dr": 92, "niche": ["Content Marketing", "Advertising"]},
    {"name": "Wakelet", "url": "https://wakelet.com", "dr": 85, "niche": ["Content Curation", "Social Media"]},
    # Detailed entries from second part
    {"name": "DevriX", "url": "https://devrix.com", "dr": 78, "niche": ["WordPress", "Development"]},
    {"name": "Front App", "url": "https://frontapp.com", "dr": 77, "niche": ["Business", "Marketing"]},
    {"name": "Carbon Black", "url": "https://www.carbonblack.com", "dr": 75, "niche": ["Tech", "Security"]},
    {"name": "Small Biz Daily", "url": "https://www.smallbizdaily.com", "dr": 76, "niche": ["Business"]},
    {"name": "Stackify", "url": "https://stackify.com", "dr": 75, "niche": ["SaaS", "Tech"]},
    {"name": "Technology Networks", "url": "https://www.technologynetworks.com", "dr": 78, "niche": ["Tech"]},
    {"name": "Recruiter", "url": "https://www.recruiter.com", "dr": 77, "niche": ["SaaS", "Business"]},
    {"name": "ProofHub", "url": "https://blog.proofhub.com", "dr": 78, "niche": ["SaaS", "Productivity"]},
    {"name": "JaxEnter", "url": "https://jaxenter.com", "dr": 73, "niche": ["Tech"]},
    {"name": "Astra Security", "url": "https://www.getastra.com", "dr": 79, "niche": ["Tech", "Security"]},
    {"name": "Geekflare", "url": "https://geekflare.com", "dr": 79, "niche": ["Tech"]},
    {"name": "Software Suggest", "url": "https://www.softwaresuggest.com", "dr": 77, "niche": ["Tech", "Software"]},
    {"name": "Paymo", "url": "https://www.paymoapp.com", "dr": 73, "niche": ["SaaS", "Productivity"]},
    {"name": "Survicate", "url": "https://survicate.com", "dr": 78, "niche": ["Tech"]},
    {"name": "Payments Journal", "url": "https://www.paymentsjournal.com", "dr": 78, "niche": ["Finance", "Payments"]},
    {"name": "InsideBIGDATA", "url": "https://insidebigdata.com", "dr": 76, "niche": ["Tech", "Data"]},
    {"name": "Level Up Coding", "url": "https://levelup.gitconnected.com", "dr": 78, "niche": ["Tech", "Programming"]},
    {"name": "LivePlan", "url": "https://www.liveplan.com", "dr": 75, "niche": ["SaaS", "Business"]},
    {"name": "SmartData Collective", "url": "https://www.smartdatacollective.com", "dr": 71, "niche": ["Tech", "Data"]},
    {"name": "CMS2CMS", "url": "https://cms2cms.com", "dr": 71, "niche": ["Tech", "CMS"]},
    {"name": "Appuals", "url": "https://appuals.com", "dr": 72, "niche": ["Tech"]},
    {"name": "IFSEC Global", "url": "https://www.ifsecglobal.com", "dr": 74, "niche": ["Security", "Tech"]},
    {"name": "Simple Programmer", "url": "https://simpleprogrammer.com", "dr": 71, "niche": ["Tech", "Programming"]},
    {"name": "Paldesk", "url": "https://www.paldesk.com", "dr": 70, "niche": ["SaaS", "Marketing"]},
    {"name": "Blog2Social", "url": "https://www.blog2social.com", "dr": 72, "niche": ["Marketing"]},
    {"name": "60 Second Marketer", "url": "https://60secondmarketer.com", "dr": 71, "niche": ["Marketing"]},
    {"name": "Sticky Password", "url": "https://www.stickypassword.com", "dr": 70, "niche": ["Tech", "Security"]},
    {"name": "DeskTime", "url": "https://desktime.com", "dr": 73, "niche": ["SaaS", "Productivity"]},
    {"name": "Sage HR", "url": "https://blog.sage.hr", "dr": 72, "niche": ["Accounting", "Finance"]},
    {"name": "WP Blog", "url": "https://www.wpblog.com", "dr": 66, "niche": ["Tech", "WordPress"]},
    {"name": "Impero", "url": "https://blog.netop.com", "dr": 64, "niche": ["SaaS", "Tech"]},
    {"name": "Kisi", "url": "https://www.getkisi.com", "dr": 70, "niche": ["SaaS", "Productivity"]},
    {"name": "Business West", "url": "https://www.businesswest.co.uk", "dr": 67, "niche": ["Business"]},
    {"name": "Bits and Pieces", "url": "https://blog.bitsrc.io", "dr": 72, "niche": ["Tech"]},
    {"name": "Codility", "url": "https://www.codility.com", "dr": 70, "niche": ["SaaS", "Tech"]},
    {"name": "SmartBiz Loans", "url": "https://www.smartbizloans.com", "dr": 70, "niche": ["Finance", "Business"]},
    {"name": "GooseChase", "url": "https://www.goosechase.com", "dr": 69, "niche": ["SaaS", "Team Building"]},
    {"name": "Magneto IT Solutions", "url": "https://magnetoitsolutions.com", "dr": 71, "niche": ["Tech"]},
    {"name": "Tallyfy", "url": "https://tallyfy.com", "dr": 66, "niche": ["SaaS", "Business"]},
    {"name": "FitWP", "url": "https://fitwp.com", "dr": 66, "niche": ["Tech", "WordPress"]},
    {"name": "SpecOps Software", "url": "https://specopssoft.com", "dr": 68, "niche": ["SaaS", "Security"]},
    {"name": "Blogging Tips", "url": "https://www.successfulblogging.com", "dr": 58, "niche": ["Marketing", "Blogging"]},
    {"name": "Innovation & Tech Today", "url": "https://innotechtoday.com", "dr": 68, "niche": ["Tech"]},
    {"name": "Sparkbay", "url": "https://sparkbay.com", "dr": 67, "niche": ["SaaS", "HR"]},
    {"name": "Viima", "url": "https://www.viima.com", "dr": 60, "niche": ["SaaS", "Innovation"]},
    {"name": "Our Code World", "url": "https://ourcodeworld.com", "dr": 64, "niche": ["Tech", "Coding"]},
    {"name": "Credibly", "url": "https://www.credibly.com", "dr": 63, "niche": ["Finance"]},
    {"name": "Insights for Professionals", "url": "https://www.insightsforprofessionals.com", "dr": 67, "niche": ["Business"]},
    {"name": "PaymentCloud", "url": "https://paymentcloudinc.com", "dr": 70, "niche": ["SaaS", "Finance"]},
    {"name": "Jason Fox", "url": "https://www.jasonfox.me", "dr": 56, "niche": ["Real Estate", "Marketing"]},
    {"name": "Scam Detector", "url": "https://www.scam-detector.com", "dr": 65, "niche": ["Security", "Tech"]},
    {"name": "Tricky Enough", "url": "https://www.trickyenough.com", "dr": 62, "niche": ["Tech"]},
    {"name": "Yoh", "url": "https://www.yoh.com", "dr": 57, "niche": ["Tech"]},
    {"name": "NicheMarket", "url": "https://www.nichemarket.co.za", "dr": 54, "niche": ["Business"]},
    {"name": "Diana Kelly Levey", "url": "https://dianakelly.com", "dr": 45, "niche": ["Freelance", "Writing"]},
    {"name": "Company Bug", "url": "https://www.companybug.com", "dr": 44, "niche": ["Business", "Finance"]},
    {"name": "StartUp Mindset", "url": "https://startupmindset.com", "dr": 44, "niche": ["Business", "Startups"]},
    {"name": "Cloverleaf", "url": "https://cloverleaf.me", "dr": 61, "niche": ["SaaS", "Productivity"]},
    {"name": "Reputation Rhino", "url": "https://www.reputationrhino.com", "dr": 52, "niche": ["Marketing"]},
]

print(f"Linkbuilder.io entries: {len(linkbuilder_entries)}\n")

# Create map of existing posts by normalized URL
def normalize_url(url):
    return url.lower().rstrip("/")

url_map = {}
for post in main_posts:
    url_norm = normalize_url(post["url"])
    url_map[url_norm] = post

# Merge linkbuilder entries
duplicates_found = 0
new_entries = 0
updated_entries = []
duplicate_list = []

for lb_entry in linkbuilder_entries:
    url_norm = normalize_url(lb_entry["url"])
    
    if url_norm in url_map:
        # Duplicate found - add/update source
        existing_post = url_map[url_norm]
        
        # Update DR if new entry has higher DR
        if lb_entry["dr"] and (existing_post.get("dr") is None or lb_entry["dr"] > existing_post.get("dr", 0)):
            old_dr = existing_post.get("dr")
            existing_post["dr"] = lb_entry["dr"]
            if old_dr and old_dr != lb_entry["dr"]:
                duplicate_list.append(f"{lb_entry['name']} (DR {lb_entry['dr']} updated from {old_dr})")
        
        # Add source if not already there
        if "linkbuilder.io" not in existing_post["listedOn"]:
            existing_post["listedOn"].append("linkbuilder.io")
            duplicates_found += 1
    else:
        # New entry
        new_post = {
            "id": lb_entry["name"].lower().replace(" ", "-").replace(".", "").replace("&", "and"),
            "name": lb_entry["name"],
            "url": lb_entry["url"],
            "dr": lb_entry["dr"],
            "description": f"Guest posting opportunity from linkbuilder.io.",
            "niche": lb_entry["niche"],
            "submissionType": "free",
            "listedOn": ["linkbuilder.io"],
            "notes": ""
        }
        main_posts.append(new_post)
        url_map[url_norm] = new_post
        new_entries += 1

# Sort by DR descending
main_posts.sort(key=lambda x: (x.get("dr") is None, -x.get("dr", 0) if x.get("dr") else 0))

# Save back
main_data["guestPosts"] = main_posts
with open(data_dir / "guest-posts.json", "w") as f:
    json.dump(main_data, f, indent=2)

print(f"=== Merge Summary ===")
print(f"Total entries: {len(main_posts)}")
print(f"Duplicates found: {duplicates_found}")
if duplicate_list:
    print(f"  DR updates/consolidations: {len(duplicate_list)}")
    for dup in duplicate_list[:10]:
        print(f"    • {dup}")
    if len(duplicate_list) > 10:
        print(f"    ... and {len(duplicate_list) - 10} more")
print(f"New entries added: {new_entries}")
print(f"\nFile saved to: {data_dir / 'guest-posts.json'}")
