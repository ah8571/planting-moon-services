#!/usr/bin/env python3
"""
Merge collaborator.pro free guest post sites with DR values into guest-posts.json
Handles duplicate URL consolidation with source attribution.
Uses first DR value when multiple metrics provided.
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

# Collaborator.pro sites with DR values (using first metric when range provided)
collaborator_entries = [
    {"name": "Serps", "url": "https://serps.com", "dr": 48, "niche": ["SEO", "Tools"]},
    {"name": "Outranking", "url": "https://outranking.io", "dr": 55, "niche": ["SEO", "Tools"]},
    {"name": "Userpilot", "url": "https://userpilot.com", "dr": 44, "niche": ["Product", "SaaS"]},
    {"name": "Jeff Bullas", "url": "https://jeffbullas.com", "dr": 79, "niche": ["Marketing", "Blogging"]},
    {"name": "MakeWebBetter", "url": "https://makewebbetter.com", "dr": 43, "niche": ["Web Development", "WordPress"]},
    {"name": "Webnus", "url": "https://webnus.net", "dr": 65, "niche": ["WordPress", "Web Design"]},
    {"name": "Clutch", "url": "https://clutch.co", "dr": 72, "niche": ["B2B", "Agencies"]},
    {"name": "Empire Flippers", "url": "https://empireflippers.com", "dr": 52, "niche": ["Digital Business", "Entrepreneurship"]},
    {"name": "Addicted2Success", "url": "https://addicted2success.com", "dr": 61, "niche": ["Entrepreneurship", "Success"]},
    {"name": "AllBusiness", "url": "https://allbusiness.com", "dr": 79, "niche": ["Business"]},
    {"name": "Entrepreneur", "url": "https://entrepreneur.com", "dr": 92, "niche": ["Entrepreneurship", "Business"]},
    {"name": "Exabytes", "url": "https://exabytes.my", "dr": 25, "niche": ["Web Hosting", "Malaysia"]},
    {"name": "Harvard Business Review", "url": "https://hbr.org", "dr": 92, "niche": ["Business", "Leadership"]},
    {"name": "Inc", "url": "https://inc.com", "dr": 91, "niche": ["Business", "Entrepreneurship"]},
    {"name": "Inc42", "url": "https://inc42.com", "dr": 78, "niche": ["Startups", "Tech", "India"]},
    {"name": "MarketingProfs", "url": "https://marketingprofs.com", "dr": 81, "niche": ["Marketing", "Content"]},
    {"name": "SoGoLytics", "url": "https://sogolytics.com", "dr": 56, "niche": ["Social Media", "Analytics"]},
    {"name": "Success.com", "url": "https://success.com", "dr": 80, "niche": ["Business", "Success"]},
    {"name": "The Ken", "url": "https://the-ken.com", "dr": 54, "niche": ["Business", "India"]},
    {"name": "WebEngage", "url": "https://webengage.com", "dr": 51, "niche": ["Marketing Automation", "CX"]},
    {"name": "ClickZ", "url": "https://clickz.com", "dr": 78, "niche": ["Digital Marketing"]},
    {"name": "HubSpot Blog", "url": "https://blog.hubspot.com", "dr": 93, "niche": ["Marketing", "Sales"]},
    {"name": "MediaPost", "url": "https://mediapost.com", "dr": 83, "niche": ["Advertising", "Marketing"]},
    {"name": "OnCrawl", "url": "https://oncrawl.com", "dr": 49, "niche": ["SEO", "Technical"]},
    {"name": "Empowerly", "url": "https://empowerly.com", "dr": 36, "niche": ["Education", "College"]},
    {"name": "EduOpinions", "url": "https://eduopinions.com", "dr": 36, "niche": ["Education", "Reviews"]},
    {"name": "Arizona State University", "url": "https://asu.edu", "dr": 91, "niche": ["Higher Education"]},
    {"name": "ASCD", "url": "https://ascd.org", "dr": 78, "niche": ["Education", "Teaching"]},
    {"name": "Edutopia", "url": "https://edutopia.org", "dr": 86, "niche": ["Education", "Teaching"]},
    {"name": "Getting Smart", "url": "https://gettingsmart.com", "dr": 74, "niche": ["Education", "Innovation"]},
    {"name": "Manning", "url": "https://manning.com", "dr": 71, "niche": ["Technology", "Books"]},
    {"name": "Top Universities", "url": "https://topuniversities.com", "dr": 85, "niche": ["Higher Education"]},
    {"name": "Benchmark Email", "url": "https://benchmarkemail.com", "dr": 64, "niche": ["Email Marketing"]},
    {"name": "GetResponse", "url": "https://getresponse.com", "dr": 84, "niche": ["Email Marketing"]},
    {"name": "Finance Alliance", "url": "https://financealliance.io", "dr": 32, "niche": ["Finance", "Technology"]},
    {"name": "Benzinga", "url": "https://benzinga.com", "dr": 88, "niche": ["Finance", "Markets"]},
    {"name": "Bigger Pockets", "url": "https://biggerpockets.com", "dr": 78, "niche": ["Real Estate", "Finance"]},
    {"name": "I Will Teach You To Be Rich", "url": "https://iwillteachyoutoberich.com", "dr": 64, "niche": ["Finance", "Personal Finance"]},
    {"name": "Investing.com", "url": "https://investing.com", "dr": 91, "niche": ["Finance", "Investing"]},
    {"name": "Money Saving Mom", "url": "https://moneysavingmom.com", "dr": 65, "niche": ["Finance", "Saving"]},
    {"name": "Oil Price", "url": "https://oilprice.com", "dr": 82, "niche": ["Finance", "Energy"]},
    {"name": "Wise Bread", "url": "https://wisebread.com", "dr": 75, "niche": ["Finance", "Personal Finance"]},
    {"name": "Above the Law", "url": "https://abovethelaw.com", "dr": 81, "niche": ["Law", "Legal"]},
    {"name": "Attorney at Work", "url": "https://attorneyatwork.com", "dr": 49, "niche": ["Law", "Legal"]},
    {"name": "Living Rich With Coupons", "url": "https://livingrichwithcoupons.com", "dr": 58, "niche": ["Finance", "Coupons"]},
    {"name": "Income Diary", "url": "https://incomediary.com", "dr": 57, "niche": ["Make Money", "Entrepreneurship"]},
    {"name": "Make a Living Writing", "url": "https://makealivingwriting.com", "dr": 52, "niche": ["Writing", "Freelance"]},
    {"name": "ChatterBuzz Media", "url": "https://chatterbuzzmedia.com", "dr": 38, "niche": ["Content", "Marketing"]},
    {"name": "Cloudways", "url": "https://cloudways.com", "dr": 72, "niche": ["Web Hosting", "Technology"]},
    {"name": "CoSchedule", "url": "https://coschedule.com", "dr": 74, "niche": ["Marketing", "Social Media"]},
    {"name": "CXL", "url": "https://cxl.com", "dr": 71, "niche": ["Marketing", "Conversion"]},
    {"name": "EZ Rankings", "url": "https://ezrankings.com", "dr": 44, "niche": ["SEO", "Tools"]},
    {"name": "MarketingTechNews", "url": "https://marketingtechnews.net", "dr": 55, "niche": ["Marketing", "Technology"]},
    {"name": "Mention", "url": "https://mention.com", "dr": 70, "niche": ["Social Media", "Monitoring"]},
    {"name": "MyCorporation", "url": "https://mycorporation.com", "dr": 57, "niche": ["Business", "Legal"]},
    {"name": "NetHunt", "url": "https://nethunt.com", "dr": 43, "niche": ["CRM", "B2B"]},
    {"name": "Omniconvert", "url": "https://omniconvert.com", "dr": 50, "niche": ["eCommerce", "CRO"]},
    {"name": "Promo", "url": "https://promo.com", "dr": 63, "niche": ["Video Marketing", "Design"]},
    {"name": "SurveySparrow", "url": "https://surveysparrow.com", "dr": 51, "niche": ["Surveys", "Marketing"]},
    {"name": "Taggbox", "url": "https://taggbox.com", "dr": 43, "niche": ["Social Media", "Curation"]},
    {"name": "Fast Company", "url": "https://fastcompany.com", "dr": 92, "niche": ["Business", "Innovation"]},
    {"name": "Forbes", "url": "https://forbes.com", "dr": 94, "niche": ["Business", "News"]},
    {"name": "ORF Online", "url": "https://orfonline.org", "dr": 66, "niche": ["News", "Analysis"]},
    {"name": "The Conversation", "url": "https://theconversation.com", "dr": 92, "niche": ["News", "Education"]},
    {"name": "The Diplomat", "url": "https://thediplomat.com", "dr": 84, "niche": ["News", "Politics"]},
    {"name": "GIJN", "url": "https://gijn.org", "dr": 68, "niche": ["Journalism", "Investigation"]},
    {"name": "The Guardian", "url": "https://theguardian.com", "dr": 95, "niche": ["News"]},
    {"name": "Mashable", "url": "https://mashable.com", "dr": 93, "niche": ["Technology", "Culture"]},
    {"name": "Wall Street Journal", "url": "https://wsj.com", "dr": 93, "niche": ["News", "Finance"]},
    {"name": "List With Clever", "url": "https://listwithclever.com", "dr": 57, "niche": ["Real Estate"]},
    {"name": "International Living", "url": "https://internationalliving.com", "dr": 69, "niche": ["Travel", "Lifestyle"]},
    {"name": "NightWatch", "url": "https://nightwatch.io", "dr": 39, "niche": ["SEO", "Monitoring"]},
    {"name": "Pearl Lemon", "url": "https://pearllemon.com", "dr": 35, "niche": ["SEO", "Digital Marketing"]},
    {"name": "Main Street Host", "url": "https://mainstreethost.com", "dr": 49, "niche": ["Web Hosting"]},
    {"name": "RankWatch", "url": "https://rankwatch.com", "dr": 45, "niche": ["SEO", "Tools"]},
    {"name": "Search Engine Land", "url": "https://searchengineland.com", "dr": 91, "niche": ["SEO", "Marketing"]},
    {"name": "Search Engine Roundtable", "url": "https://seroundtable.com", "dr": 78, "niche": ["SEO"]},
    {"name": "TechWyse", "url": "https://techwyse.com", "dr": 51, "niche": ["SEO", "Digital Marketing"]},
    {"name": "Agorapulse", "url": "https://agorapulse.com", "dr": 70, "niche": ["Social Media"]},
    {"name": "Buffer", "url": "https://buffer.com", "dr": 90, "niche": ["Social Media", "Tools"]},
    {"name": "TechImply", "url": "https://techimply.com", "dr": 36, "niche": ["Technology"]},
    {"name": "Katalon", "url": "https://katalon.com", "dr": 48, "niche": ["Testing", "QA"]},
    {"name": "OutrightCRM", "url": "https://store.outrightcrm.com", "dr": 35, "niche": ["CRM", "B2B"]},
    {"name": "TechDogs", "url": "https://techdogs.com", "dr": 42, "niche": ["Technology"]},
    {"name": "SeekAHost", "url": "https://seekahost.com", "dr": 26, "niche": ["Web Hosting"]},
    {"name": "TechTarget", "url": "https://techtarget.com", "dr": 91, "niche": ["Technology", "IT"]},
    {"name": "Tech Reviewer", "url": "https://techreviewer.co", "dr": 36, "niche": ["Technology", "Reviews"]},
    {"name": "Analytics Insight", "url": "https://analyticsinsight.net", "dr": 66, "niche": ["Analytics", "AI"]},
    {"name": "Chanty", "url": "https://chanty.com", "dr": 50, "niche": ["Communication", "Tools"]},
    {"name": "Reverb ICO", "url": "https://reverbico.com", "dr": 36, "niche": ["Cryptocurrency"]},
    {"name": "Colocation America", "url": "https://colocationamerica.com", "dr": 52, "niche": ["Web Hosting"]},
    {"name": "Creately", "url": "https://creately.com", "dr": 77, "niche": ["Diagramming", "Design"]},
    {"name": "Crunchbase", "url": "https://crunchbase.com", "dr": 91, "niche": ["Tech", "Investment"]},
    {"name": "DZone", "url": "https://dzone.com", "dr": 84, "niche": ["Technology", "Development"]},
    {"name": "Freshworks", "url": "https://freshworks.com", "dr": 77, "niche": ["CRM", "Customer Service"]},
    {"name": "Hongkiat", "url": "https://hongkiat.com", "dr": 81, "niche": ["Web Design", "Technology"]},
    {"name": "How Stuff Works", "url": "https://howstuffworks.com", "dr": 92, "niche": ["Education", "Knowledge"]},
    {"name": "Jungleworks", "url": "https://jungleworks.com", "dr": 36, "niche": ["SaaS", "Startups"]},
    {"name": "ProProfs", "url": "https://proprofs.com", "dr": 86, "niche": ["Training", "Knowledge"]},
    {"name": "SitePoint", "url": "https://sitepoint.com", "dr": 85, "niche": ["Web Development", "Design"]},
    {"name": "Slashdot", "url": "https://slashdot.org", "dr": 91, "niche": ["Technology", "News"]},
    {"name": "Technology Networks", "url": "https://technologynetworks.com", "dr": 69, "niche": ["Technology", "Science"]},
    {"name": "TechRepublic", "url": "https://techrepublic.com", "dr": 88, "niche": ["Technology", "IT"]},
    {"name": "The Drive", "url": "https://thedrive.com", "dr": 86, "niche": ["Automotive", "Culture"]},
    {"name": "VentureBeat", "url": "https://venturebeat.com", "dr": 91, "niche": ["Technology", "Startups"]},
    {"name": "The IT Base", "url": "https://theitbase.com", "dr": 59, "niche": ["Technology"]},
    {"name": "AI's Tech Labs", "url": "https://aistechnolabs.com", "dr": 42, "niche": ["AI", "Development"]},
    {"name": "Wisdom Labs", "url": "https://wisdmlabs.com", "dr": 43, "niche": ["Web Development"]},
    {"name": "Icons8", "url": "https://icons8.com", "dr": 85, "niche": ["Design", "Icons"]},
    {"name": "This Is Colossal", "url": "https://thisiscolossal.com", "dr": 78, "niche": ["Design", "Art"]},
    {"name": "Creative Bloq", "url": "https://creativebloq.com", "dr": 86, "niche": ["Design"]},
    {"name": "CSS-Tricks", "url": "https://css-tricks.com", "dr": 84, "niche": ["Web Development", "CSS"]},
    {"name": "Design Milk", "url": "https://design-milk.com", "dr": 73, "niche": ["Design"]},
    {"name": "MotoCMS", "url": "https://motocms.com", "dr": 53, "niche": ["Website Builder", "CMS"]},
    {"name": "Netguru", "url": "https://netguru.com", "dr": 56, "niche": ["Web Development", "Design"]},
    {"name": "Reseller Club", "url": "https://resellerclub.com", "dr": 51, "niche": ["Web Hosting"]},
    {"name": "Smashing Magazine", "url": "https://smashingmagazine.com", "dr": 89, "niche": ["Web Design", "Development"]},
    {"name": "Specky Boy", "url": "https://speckyboy.com", "dr": 76, "niche": ["Web Design"]},
    {"name": "Stackify", "url": "https://stackify.com", "dr": 56, "niche": ["Development", "Tools"]},
    {"name": "Web Alive", "url": "https://webalive.com.au", "dr": 40, "niche": ["Web Design", "Australia"]},
    {"name": "Webdew", "url": "https://webdew.com", "dr": 34, "niche": ["Web Design"]},
]

print(f"Collaborator.pro entries: {len(collaborator_entries)}\n")

# Create map of existing posts by normalized URL
def normalize_url(url):
    return url.lower().rstrip("/")

url_map = {}
for post in main_posts:
    url_norm = normalize_url(post["url"])
    url_map[url_norm] = post

# Merge collaborator entries
duplicates_found = 0
new_entries = 0
updated_entries = []
duplicate_list = []

for col_entry in collaborator_entries:
    url_norm = normalize_url(col_entry["url"])
    
    if url_norm in url_map:
        # Duplicate found - add source to existing entry
        existing_post = url_map[url_norm]
        
        # Update DR if new entry has higher DR
        if col_entry["dr"] and (existing_post.get("dr") is None or col_entry["dr"] > existing_post.get("dr", 0)):
            existing_post["dr"] = col_entry["dr"]
        
        # Add source if not already there
        if "collaborator.pro" not in existing_post["listedOn"]:
            existing_post["listedOn"].append("collaborator.pro")
            duplicates_found += 1
            updated_entries.append((existing_post["name"], existing_post["dr"]))
            duplicate_list.append(f"{col_entry['name']} → {existing_post['name']}")
    else:
        # New entry
        new_post = {
            "id": col_entry["name"].lower().replace(" ", "-").replace(".", "").replace(",", ""),
            "name": col_entry["name"],
            "url": col_entry["url"],
            "dr": col_entry["dr"],
            "description": f"Free guest posting opportunity from collaborator.pro.",
            "niche": col_entry["niche"],
            "submissionType": "free",
            "listedOn": ["collaborator.pro"],
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
print(f"Duplicates consolidated: {duplicates_found}")
if duplicate_list:
    print(f"  Examples of consolidations:")
    for dup in duplicate_list[:10]:
        print(f"    • {dup}")
    if len(duplicate_list) > 10:
        print(f"    ... and {len(duplicate_list) - 10} more")
print(f"New entries added: {new_entries}")
print(f"\nFile saved to: {data_dir / 'guest-posts.json'}")
