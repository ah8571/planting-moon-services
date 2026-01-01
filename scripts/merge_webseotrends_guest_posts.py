#!/usr/bin/env python3
"""
Merge webseotrends.com free guest post sites into guest-posts.json
Handles duplicate URL consolidation with source attribution.
DR values left blank unless already in database.
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

# Webseotrends data - parsed from the list (organized by category)
webseotrends_entries = [
    # SEO Sites
    {"name": "Webseotrends", "url": "https://webseotrends.com", "dr": None, "niche": ["SEO"]},
    {"name": "SEO Scout", "url": "https://seoscout.com", "dr": None, "niche": ["SEO"]},
    {"name": "OnCrawl", "url": "https://oncrawl.com", "dr": None, "niche": ["SEO", "Technical SEO"]},
    {"name": "Rank Ranger", "url": "https://www.rankranger.com", "dr": None, "niche": ["SEO"]},
    {"name": "DZone", "url": "https://dzone.com", "dr": None, "niche": ["Technology", "SEO"]},
    {"name": "UnderConstructionPage", "url": "https://underconstructionpage.com", "dr": None, "niche": ["WordPress", "Blogging"]},
    {"name": "WP Reset", "url": "https://wpreset.com", "dr": None, "niche": ["WordPress"]},
    {"name": "EZ Rankings", "url": "https://ezrankings.com", "dr": None, "niche": ["SEO"]},
    {"name": "SEOmator", "url": "https://seomator.com", "dr": None, "niche": ["SEO"]},
    {"name": "Super Monitoring", "url": "https://www.supermonitoring.com", "dr": None, "niche": ["SEO", "Monitoring"]},
    {"name": "Rank Tracker", "url": "https://www.ranktracker.com", "dr": None, "niche": ["SEO"]},
    
    # Marketing/Content Marketing Sites
    {"name": "Ecwid", "url": "https://www.ecwid.com", "dr": None, "niche": ["eCommerce", "Marketing"]},
    {"name": "Cloudways", "url": "https://www.cloudways.com", "dr": None, "niche": ["Web Hosting", "Technology"]},
    {"name": "BuzzSumo", "url": "https://buzzsumo.com", "dr": None, "niche": ["Content Marketing", "Digital PR"]},
    {"name": "VWO", "url": "https://vwo.com", "dr": None, "niche": ["A/B Testing", "CRO"]},
    {"name": "CustomerThink", "url": "https://customerthink.com", "dr": None, "niche": ["Customer Experience"]},
    {"name": "SingleGrain", "url": "https://www.singlegrain.com", "dr": None, "niche": ["Digital Marketing"]},
    {"name": "Blogging Wizard", "url": "https://www.bloggingwizard.com", "dr": None, "niche": ["Blogging"]},
    {"name": "involve.me", "url": "https://www.involve.me", "dr": None, "niche": ["Quizzes", "Lead Generation"]},
    {"name": "Prowly", "url": "https://prowly.com", "dr": None, "niche": ["PR"]},
    {"name": "ResellerClub Blog", "url": "https://blog.resellerclub.com", "dr": None, "niche": ["Web Hosting"]},
    {"name": "Promo", "url": "https://promo.com", "dr": None, "niche": ["Video Marketing", "Social Media"]},
    {"name": "Noupe", "url": "https://www.noupe.com", "dr": None, "niche": ["Design", "Creativity"]},
    {"name": "B2B Marketing", "url": "https://www.b2bmarketing.net", "dr": None, "niche": ["B2B", "Marketing"]},
    {"name": "MarketingTech", "url": "https://marketingtech.com", "dr": None, "niche": ["Marketing"]},
    {"name": "SurveySparrow", "url": "https://www.surveysparrow.com", "dr": None, "niche": ["Surveys", "Marketing"]},
    {"name": "Omniconvert", "url": "https://www.omniconvert.com", "dr": None, "niche": ["eCommerce", "CRO"]},
    {"name": "Wave.video", "url": "https://wave.video", "dr": None, "niche": ["Video Marketing"]},
    {"name": "Taggbox", "url": "https://www.taggbox.com", "dr": None, "niche": ["Social Media", "Content"]},
    {"name": "Woorise", "url": "https://www.woorise.com", "dr": None, "niche": ["Contests", "Marketing"]},
    {"name": "Pole Position Marketing", "url": "https://www.polepositionmarketing.com", "dr": None, "niche": ["SEO", "Marketing"]},
    {"name": "The Next Scoop", "url": "https://thenextscoop.com", "dr": None, "niche": ["News", "Marketing"]},
    {"name": "Userpilot", "url": "https://userpilot.com", "dr": None, "niche": ["Product Marketing", "SaaS"]},
    {"name": "DeskTime", "url": "https://www.desktime.com", "dr": None, "niche": ["Productivity"]},
    {"name": "WebEngage", "url": "https://www.webengage.com", "dr": None, "niche": ["Marketing Automation"]},
    {"name": "Website Promoter", "url": "https://www.websitepromoter.com", "dr": None, "niche": ["Digital Marketing"]},
    {"name": "NetHunt", "url": "https://nethunt.com", "dr": None, "niche": ["CRM", "B2B"]},
    {"name": "Reputation X", "url": "https://reputationx.com", "dr": None, "niche": ["Reputation Management"]},
    {"name": "Compose.ly", "url": "https://www.compose.ly", "dr": None, "niche": ["Content", "Freelance"]},
    {"name": "Contact Pigeon", "url": "https://www.contactpigeon.com", "dr": None, "niche": ["eCommerce", "Marketing"]},
    {"name": "Love My Online Marketing", "url": "https://lovemyonlinemarketing.com", "dr": None, "niche": ["Digital Marketing", "SEO"]},
    {"name": "Outreach Monks", "url": "https://www.outreachmonks.com", "dr": None, "niche": ["Outreach", "Link Building"]},
    {"name": "Digital Success", "url": "https://digitalsuccess.com.au", "dr": None, "niche": ["Digital Marketing"]},
    {"name": "Digital Delane", "url": "https://www.digitaldelane.com", "dr": None, "niche": ["Web Development", "Marketing"]},
    {"name": "Logicsofts Blog", "url": "https://blog.logicsofts.com", "dr": None, "niche": ["IT", "Marketing"]},
    {"name": "Valasys Media", "url": "https://valasysmedia.com", "dr": None, "niche": ["Marketing", "Business Tech"]},
    
    # Email Marketing Sites
    {"name": "GrowMeOrganic", "url": "https://www.growmeorganic.com", "dr": None, "niche": ["Email Marketing", "Growth"]},
    {"name": "AMPmails", "url": "https://ampmails.com", "dr": None, "niche": ["Email Marketing"]},
    {"name": "Search Engine Insight", "url": "https://searchengineinsight.com", "dr": None, "niche": ["Email Marketing", "SEO"]},
    {"name": "MailerCloud", "url": "https://www.mailercloud.com", "dr": None, "niche": ["Email Marketing"]},
    {"name": "Upgrow", "url": "https://upgrow.com", "dr": None, "niche": ["Digital Marketing", "Email"]},
    {"name": "CXL", "url": "https://cxl.com", "dr": None, "niche": ["Digital Marketing", "Data-driven"]},
    {"name": "Content Whale", "url": "https://contentwhale.com", "dr": None, "niche": ["Guest Posting", "Content"]},
    {"name": "MailerLite", "url": "https://www.mailerlite.com", "dr": None, "niche": ["Email Marketing"]},
    
    # Social Media Sites
    {"name": "Social Media Week", "url": "https://socialmediaweek.org", "dr": None, "niche": ["Social Media"]},
    {"name": "ContentStudio", "url": "https://contentstudio.io", "dr": None, "niche": ["Social Media", "Content"]},
    {"name": "Digital Monk", "url": "https://www.digitalmonk.in", "dr": None, "niche": ["Digital Marketing", "Social Media"]},
    {"name": "Corexta", "url": "https://corexta.com", "dr": None, "niche": ["SaaS", "Digital Marketing"]},
    
    # Business/Entrepreneurship Sites
    {"name": "GoDaddy Garage", "url": "https://www.godaddy.com/garage", "dr": None, "niche": ["Business", "Entrepreneurship"]},
    {"name": "Exabytes", "url": "https://www.exabytes.com", "dr": None, "niche": ["IT", "Business"]},
    {"name": "ReferralCandy Blog", "url": "https://www.referralcandy.com/blog", "dr": None, "niche": ["eCommerce"]},
    {"name": "Startup Info", "url": "https://startupinfo.co", "dr": None, "niche": ["Startups"]},
    {"name": "SoGoSurvey Blog", "url": "https://www.sogosurvey.com/blog", "dr": None, "niche": ["Surveys", "Marketing"]},
    {"name": "Convert Write for Us", "url": "https://www.convert.com", "dr": None, "niche": ["CRO", "A/B Testing"]},
    {"name": "CandyBar Blog", "url": "https://www.candybar.io", "dr": None, "niche": ["Business"]},
    {"name": "Sansan Resources", "url": "https://sansan.com", "dr": None, "niche": ["B2B", "Business"]},
    {"name": "Curatti", "url": "https://www.curatti.com", "dr": None, "niche": ["B2B", "Thought Leadership"]},
    {"name": "Young Upstarts", "url": "https://www.youngupstarts.com", "dr": None, "niche": ["Entrepreneurship"]},
    {"name": "Insights for Professionals", "url": "https://www.insightsforprofessionals.com", "dr": None, "niche": ["Business", "Professional"]},
    {"name": "The Ken", "url": "https://the-ken.com", "dr": None, "niche": ["Business", "India"]},
    {"name": "Gimm.io Blog", "url": "https://gimm.io", "dr": None, "niche": ["Entrepreneurship"]},
    {"name": "MyVenturePad", "url": "https://www.myventurepad.com", "dr": None, "niche": ["Entrepreneurship"]},
    {"name": "Punnaka", "url": "https://punnaka.com", "dr": None, "niche": ["Business"]},
    
    # Content Writing Sites
    {"name": "Contently", "url": "https://contently.com", "dr": None, "niche": ["Content", "Journalism"]},
    {"name": "Copyhackers", "url": "https://copyhackers.com", "dr": None, "niche": ["Copywriting"]},
    {"name": "99signals", "url": "https://www.99signals.com", "dr": None, "niche": ["Digital Marketing"]},
    {"name": "Make a Living Writing", "url": "https://www.makealivinwriting.com", "dr": None, "niche": ["Writing", "Freelance"]},
    {"name": "Spin Sucks", "url": "https://spinsucks.com", "dr": None, "niche": ["PR", "Content"]},
    {"name": "Webnus", "url": "https://webnus.net", "dr": None, "niche": ["WordPress", "Web Design"]},
    {"name": "Authority Hacker", "url": "https://www.authorityhacker.com", "dr": None, "niche": ["SEO", "Content"]},
    {"name": "CyberChimps", "url": "https://www.cyberchimps.com", "dr": None, "niche": ["WordPress"]},
    {"name": "Writing Commons", "url": "https://writingcommons.org", "dr": None, "niche": ["Writing"]},
    {"name": "Muck Rack", "url": "https://muckrack.com", "dr": None, "niche": ["PR", "Journalism"]},
    {"name": "GIJN", "url": "https://gijn.org", "dr": None, "niche": ["Journalism"]},
    {"name": "WebsiteSetup", "url": "https://websitesetup.org", "dr": None, "niche": ["Web Design", "Blogging"]},
    
    # Finance Sites
    {"name": "Money Crashers", "url": "https://www.moneycrashers.com", "dr": None, "niche": ["Finance", "Personal Finance"]},
    {"name": "Wise Bread", "url": "https://www.wisebread.com", "dr": None, "niche": ["Finance", "Personal Finance"]},
    
    # Tech/Technology Sites
    {"name": "Technology Networks", "url": "https://technologynetworks.com", "dr": None, "niche": ["Technology"]},
    {"name": "DotNetCurry", "url": "https://www.dotnetcurry.com", "dr": None, "niche": [".NET", "Technology"]},
    {"name": "LoginRadius", "url": "https://www.loginradius.com", "dr": None, "niche": ["Identity", "Security"]},
    {"name": "Simple Programmer", "url": "https://simpleprogrammer.com", "dr": None, "niche": ["Programming"]},
    {"name": "SoftwareWorld", "url": "https://www.softwareworld.co.uk", "dr": None, "niche": ["Software", "B2B"]},
    {"name": "ProProfs", "url": "https://www.proprofs.com", "dr": None, "niche": ["Training", "Knowledge"]},
    {"name": "ClickZ", "url": "https://www.clickz.com", "dr": None, "niche": ["Digital Marketing", "Tech"]},
    {"name": "HackerNoon", "url": "https://hackernoon.com", "dr": None, "niche": ["Technology", "Programming"]},
    {"name": "Crunchbase", "url": "https://www.crunchbase.com", "dr": None, "niche": ["Tech", "Investment"]},
    {"name": "Analytics India Magazine", "url": "https://analyticsindiamag.com", "dr": None, "niche": ["Analytics", "AI"]},
    {"name": "All Tech Buzz", "url": "https://www.alltechbuzz.net", "dr": None, "niche": ["Technology"]},
    {"name": "CookieYes", "url": "https://www.cookieyes.com", "dr": None, "niche": ["Compliance", "Web"]},
    {"name": "Chetu", "url": "https://www.chetu.com", "dr": None, "niche": ["Software Development"]},
    {"name": "iMocha", "url": "https://www.imocha.io", "dr": None, "niche": ["HR Tech", "Assessment"]},
    {"name": "The Next Tech", "url": "https://www.thenexttech.net", "dr": None, "niche": ["Technology"]},
    {"name": "Analytics Insight", "url": "https://www.analyticsinsight.net", "dr": None, "niche": ["Analytics", "AI"]},
    {"name": "Mobisoft Infotech", "url": "https://www.mobisoftinfotech.com", "dr": None, "niche": ["Mobile", "Technology"]},
    {"name": "Neptune Blog", "url": "https://www.getoptimo.com", "dr": None, "niche": ["Optimization"]},
    {"name": "Big Data Made Simple", "url": "https://bigdatamadesmple.com", "dr": None, "niche": ["Big Data"]},
    {"name": "iTechCode", "url": "https://itechcode.com", "dr": None, "niche": ["Technology", "Code"]},
    {"name": "Chanty", "url": "https://www.chanty.com", "dr": None, "niche": ["Communication", "Productivity"]},
    {"name": "Jungleworks", "url": "https://www.jungleworks.com", "dr": None, "niche": ["SaaS", "Startups"]},
    {"name": "I Drop News", "url": "https://www.idropnews.com", "dr": None, "niche": ["Apple", "Tech News"]},
    
    # eLearning/Education Sites
    {"name": "eLearning Industry", "url": "https://elearningindustry.com", "dr": None, "niche": ["eLearning", "Education"]},
    {"name": "Edureka", "url": "https://www.edureka.co", "dr": None, "niche": ["Online Learning", "Tech"]},
    {"name": "MindMajix", "url": "https://mindmajix.com", "dr": None, "niche": ["EdTech", "Training"]},
    {"name": "TutorialsTeacher", "url": "https://www.tutorialsteacher.com", "dr": None, "niche": ["Programming", "Tutorials"]},
    {"name": "Teach.com", "url": "https://teach.com", "dr": None, "niche": ["Education", "Teaching"]},
    {"name": "Edutopia", "url": "https://www.edutopia.org", "dr": None, "niche": ["Education", "Teaching"]},
    {"name": "Chronicle", "url": "https://www.chronicle.com", "dr": None, "niche": ["Higher Education"]},
    {"name": "THE (Times Higher Ed)", "url": "https://www.timeshighereducation.com", "dr": None, "niche": ["Higher Education"]},
    {"name": "EdWeek", "url": "https://www.edweek.org", "dr": None, "niche": ["Education", "News"]},
    {"name": "Getting Smart", "url": "https://www.gettingsmart.com", "dr": None, "niche": ["Education", "Innovation"]},
    {"name": "LearnWorlds", "url": "https://learnworlds.com", "dr": None, "niche": ["eLearning", "Course Creation"]},
    {"name": "TopUniversities", "url": "https://www.topuniversities.com", "dr": None, "niche": ["Higher Education"]},
    {"name": "Open Colleges", "url": "https://www.opencolleges.edu.au", "dr": None, "niche": ["Online Education"]},
    {"name": "ASCD Express", "url": "https://www.ascd.org", "dr": None, "niche": ["Education", "Teaching"]},
    {"name": "InformIT", "url": "https://www.informit.com", "dr": None, "niche": ["Tech Education"]},
    {"name": "Infed.org", "url": "https://infed.org", "dr": None, "niche": ["Education", "Learning"]},
    {"name": "The PIE News", "url": "https://thepienews.com", "dr": None, "niche": ["International Education"]},
    {"name": "Greater Good Science Center", "url": "https://greatergood.berkeley.edu", "dr": None, "niche": ["Education", "Well-being"]},
    {"name": "eLearn Magazine", "url": "https://elearnmag.org", "dr": None, "niche": ["eLearning"]},
    
    # Design/Web Design Sites
    {"name": "Webflow", "url": "https://webflow.com", "dr": None, "niche": ["Web Design", "No-code"]},
    {"name": "UX Matters", "url": "https://www.uxmatters.com", "dr": None, "niche": ["UX Design"]},
    {"name": "Web Design Ledger", "url": "https://webdesignledger.com", "dr": None, "niche": ["Web Design"]},
    {"name": "Stackify", "url": "https://stackify.com", "dr": None, "niche": ["Development", "Tools"]},
    {"name": "WebAlive", "url": "https://www.webalive.com.au", "dr": None, "niche": ["Web Design"]},
    {"name": "Ink Bot Design", "url": "https://www.inkbotdesign.com", "dr": None, "niche": ["Design", "Marketing"]},
    {"name": "Netguru", "url": "https://www.netguru.com", "dr": None, "niche": ["Web Design", "Development"]},
    {"name": "Webdew", "url": "https://www.webdew.com", "dr": None, "niche": ["Web Design"]},
    {"name": "binPress", "url": "https://www.binpress.com", "dr": None, "niche": ["Development", "Design"]},
    {"name": "Creative Nerds", "url": "https://creativedennis.com", "dr": None, "niche": ["Design", "Creativity"]},
    {"name": "Top Design Magazine", "url": "https://www.topdesignmag.com", "dr": None, "niche": ["Design"]},
    {"name": "Skyje", "url": "https://skyje.com", "dr": None, "niche": ["Design", "Photography"]},
]

print(f"WebseoTrends entries: {len(webseotrends_entries)}\n")

# Create map of existing posts by normalized URL
def normalize_url(url):
    return url.lower().rstrip("/")

url_map = {}
for post in main_posts:
    url_norm = normalize_url(post["url"])
    url_map[url_norm] = post

# Merge webseotrends entries
duplicates_found = 0
new_entries = 0
updated_entries = []

for wt_entry in webseotrends_entries:
    url_norm = normalize_url(wt_entry["url"])
    
    if url_norm in url_map:
        # Duplicate found - add webseotrends.com to sources
        existing_post = url_map[url_norm]
        if "webseotrends.com" not in existing_post["listedOn"]:
            existing_post["listedOn"].append("webseotrends.com")
            duplicates_found += 1
            updated_entries.append(existing_post["name"])
            
            # If existing post has no DR and this one specifies one, keep existing
            # (DR was already set from another source)
    else:
        # New entry - create JSON object with proper structure
        new_post = {
            "id": wt_entry["name"].lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", ""),
            "name": wt_entry["name"],
            "url": wt_entry["url"],
            "dr": wt_entry["dr"],
            "description": f"Free guest posting opportunity from webseotrends.com.",
            "niche": wt_entry["niche"],
            "submissionType": "free",
            "listedOn": ["webseotrends.com"],
            "notes": ""
        }
        main_posts.append(new_post)
        url_map[url_norm] = new_post
        new_entries += 1

# Sort by DR descending (None values go to end)
main_posts.sort(key=lambda x: (x.get("dr") is None, -x.get("dr", 0) if x.get("dr") else 0))

# Save back
main_data["guestPosts"] = main_posts
with open(data_dir / "guest-posts.json", "w") as f:
    json.dump(main_data, f, indent=2)

print(f"=== Merge Summary ===")
print(f"Total entries: {len(main_posts)}")
print(f"Duplicates consolidated: {duplicates_found}")
if updated_entries:
    print(f"  Examples: {', '.join(updated_entries[:5])}")
print(f"New entries added: {new_entries}")
print(f"\nFile saved to: {data_dir / 'guest-posts.json'}")
