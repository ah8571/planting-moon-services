#!/usr/bin/env python3
"""
Merge webmetools.com guest post list into guest-posts.json
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

# Webmetools data - parsed from the list
webmetools_entries = [
    {"name": "Mini Business News", "url": "https://minibusinessnews.com", "dr": 55, "niche": ["News"]},
    {"name": "SEO Hacker", "url": "https://seo-hacker.com/guest-post/", "dr": 51, "niche": ["SEO"]},
    {"name": "Pole Position Marketing", "url": "https://www.polepositionmarketing.com/emp/write-for-us/", "dr": 48, "niche": ["SEO"]},
    {"name": "TechWyse", "url": "https://www.techwyse.com/write-for-us/", "dr": 54, "niche": ["SEO", "Marketing"]},
    {"name": "MarketingTechNews", "url": "https://www.marketingtechnews.net/about-us/write-us/", "dr": 56, "niche": ["Marketing", "Technology"]},
    {"name": "Linkody Blog", "url": "https://blog.linkody.com/write-for-us", "dr": 42, "niche": ["SEO"]},
    {"name": "SEMrush", "url": "https://www.semrush.com/blog/guidelines/", "dr": 79, "niche": ["SEO", "Marketing"]},
    {"name": "RankWatch Blog", "url": "https://www.rankwatch.com/blog/write-for-us/", "dr": 45, "niche": ["SEO"]},
    {"name": "Serpstat Blog", "url": "https://serpstat.com/blog/how-to-submit-a-guest-post-to-serpstat-blog/", "dr": 54, "niche": ["SEO"]},
    {"name": "Jeff Bullas", "url": "https://www.jeffbullas.com/writing-process-guidelines/", "dr": 72, "niche": ["Marketing", "Social Media"]},
    {"name": "Search Engine Watch", "url": "https://www.searchenginewatch.com/become-a-contributor.html", "dr": 79, "niche": ["SEO"]},
    {"name": "Search Engine Land", "url": "https://searchengineland.com/how-to-become-a-guest-contributor", "dr": 90, "niche": ["SEO", "Marketing"]},
    {"name": "Search Engine Roundtable", "url": "https://www.seroundtable.com/contact.php", "dr": 77, "niche": ["SEO"]},
    {"name": "SEO Blog", "url": "https://www.seoblog.com/contribute/", "dr": 43, "niche": ["SEO"]},
    {"name": "Mainstreethost", "url": "https://www.mainstreethost.com/contribute", "dr": 51, "niche": ["Web Hosting"]},
    {"name": "John Chow", "url": "https://www.johnchow.com/get-more-exposure-for-your-blog-with-a-guest-post/", "dr": 58, "niche": ["Blogging", "Marketing"]},
    {"name": "Daily Blog Tips", "url": "https://www.dailyblogtips.com/daily-blog-tips-guest-post-guidelines/", "dr": 57, "niche": ["Blogging"]},
    {"name": "Blog Engage", "url": "https://www.blogengage.com/blogger/guest-blog/", "dr": 45, "niche": ["Blogging"]},
    {"name": "Bloggers Passion", "url": "https://bloggerspassion.com/contact/", "dr": 47, "niche": ["Blogging"]},
    {"name": "BlogSolute", "url": "https://www.blogsolute.com/contact-us/", "dr": 48, "niche": ["Blogging"]},
    {"name": "Hellbound Bloggers", "url": "https://hellboundbloggers.com/join-hbb/", "dr": 47, "niche": ["Blogging"]},
    {"name": "Content Marketing Institute", "url": "https://contentmarketinginstitute.com/blog/blog-guidelines/", "dr": 77, "niche": ["Content Marketing"]},
    {"name": "The Blog Herald", "url": "https://www.blogherald.com/contact-us/", "dr": 61, "niche": ["Blogging"]},
    {"name": "Dealer Marketing", "url": "https://www.dealermarketing.com/write-for-us/", "dr": 43, "niche": ["Marketing"]},
    {"name": "Hinge Marketing", "url": "https://hingemarketing.com/careers/writers", "dr": 52, "niche": ["Marketing"]},
    {"name": "B2B Marketing", "url": "https://www.b2bmarketing.net/en-gb/get-involved", "dr": 68, "niche": ["B2B", "Marketing"]},
    {"name": "HubSpot Blog", "url": "https://blog.hubspot.com/marketing-guest-blogging-guidelines", "dr": 91, "niche": ["Marketing", "Sales"]},
    {"name": "Kikolani", "url": "https://kikolani.com/contact-us/", "dr": 50, "niche": ["Marketing"]},
    {"name": "MarketingProfs", "url": "https://www.marketingprofs.com/write-for-us", "dr": 75, "niche": ["Marketing"]},
    {"name": "AllBusiness", "url": "https://www.allbusiness.com/guest-post-overview", "dr": 79, "niche": ["Business"]},
    {"name": "Business2Community", "url": "https://www.business2community.com/become-a-contributor", "dr": 86, "niche": ["Business", "Marketing"]},
    {"name": "Business.com", "url": "https://www.business.com/experts/", "dr": 78, "niche": ["Business"]},
    {"name": "GrowMap", "url": "https://growmap.com/growmap-guest-blogging-guidelines/", "dr": 48, "niche": ["Business"]},
    {"name": "Outbrain", "url": "https://www.outbrain.com/blog/guest-blogging-guidelines/", "dr": 82, "niche": ["Content Marketing"]},
    {"name": "Inc", "url": "https://www.inc.com/about/contact_us.html", "dr": 92, "niche": ["Business", "Entrepreneurship"]},
    {"name": "Tweak Your Biz", "url": "https://tweakyourbiz.com/write-for-tyb", "dr": 58, "niche": ["Business"]},
    {"name": "GoDaddy Garage", "url": "https://www.godaddy.com/garage/contribute/", "dr": 93, "niche": ["Business", "Technology"]},
    {"name": "Success.com", "url": "https://www.success.com/contact-us/", "dr": 76, "niche": ["Business", "Entrepreneurship"]},
    {"name": "BPlans", "url": "https://articles.bplans.com/authors/", "dr": 68, "niche": ["Business", "Entrepreneurship"]},
    {"name": "MyCorporation Blog", "url": "https://blog.mycorporation.com/become-author-mycorporation/", "dr": 60, "niche": ["Business"]},
    {"name": "Successful Blog", "url": "https://www.successful-blog.com/got-a-success-story-or-tip-to-share/", "dr": 52, "niche": ["Business"]},
    {"name": "Social Media Examiner", "url": "https://www.socialmediaexaminer.com/writers/", "dr": 79, "niche": ["Social Media", "Marketing"]},
    {"name": "Mashable", "url": "https://mashable.com/submit/", "dr": 93, "niche": ["Technology", "Culture"]},
    {"name": "Social Media Today", "url": "https://www.socialmediatoday.com/contribute/", "dr": 78, "niche": ["Social Media", "Marketing"]},
    {"name": "CoSchedule", "url": "https://coschedule.com/write-for-us/", "dr": 72, "niche": ["Marketing", "Social Media"]},
    {"name": "PostPlanner", "url": "https://www.postplanner.com/guest-blogger-welcome/", "dr": 64, "niche": ["Social Media"]},
    {"name": "Socialnomics", "url": "https://socialnomics.net/contact/", "dr": 59, "niche": ["Social Media"]},
    {"name": "Mention", "url": "https://mention.com/en/blog/guest-blogging/", "dr": 72, "niche": ["Social Media", "Marketing"]},
    {"name": "Social Media Week", "url": "https://socialmediaweek.org/news/write-for-us/", "dr": 71, "niche": ["Social Media"]},
    {"name": "Social Media Explorer", "url": "https://socialmediaexplorer.com/work-with-us/", "dr": 63, "niche": ["Social Media"]},
    {"name": "Agorapulse", "url": "https://www.agorapulse.com/write-for-us", "dr": 67, "niche": ["Social Media"]},
    {"name": "Brand24 Blog", "url": "https://brand24.com/blog/write-for-us/", "dr": 54, "niche": ["Social Media", "Marketing"]},
    {"name": "Social Media Strategies Summit", "url": "https://socialmediastrategiessummit.com/get-involved/write-for-us.html", "dr": 44, "niche": ["Social Media"]},
    {"name": "Sociable Blog", "url": "https://www.sociableblog.com/submit-news/", "dr": 50, "niche": ["Social Media"]},
    {"name": "ClickFire", "url": "https://clickfire.com/writers/", "dr": 45, "niche": ["Social Media"]},
    {"name": "Social Media Revolver", "url": "https://socialmediarevolver.com/guest-posts/", "dr": 42, "niche": ["Social Media"]},
    {"name": "iDigic", "url": "https://www.idigic.net/write-for-us/", "dr": 41, "niche": ["Social Media"]},
    {"name": "DLvrit Blog", "url": "https://blog.dlvrit.com/write-for-us/", "dr": 61, "niche": ["Social Media"]},
    {"name": "GetResponse Blog", "url": "https://www.getresponse.com/blog/write-for-us", "dr": 82, "niche": ["Email Marketing"]},
    {"name": "Benchmark Email", "url": "https://blog.benchmarkemail.com/marketing-professionals-write-guest-blogs-for-benchmark-email/", "dr": 64, "niche": ["Email Marketing"]},
    {"name": "Mailjet", "url": "https://www.mailjet.com/contributor-guidelines/", "dr": 66, "niche": ["Email Marketing"]},
    {"name": "Labnol", "url": "https://www.labnol.org/write/", "dr": 80, "niche": ["Technology"]},
    {"name": "SitePoint", "url": "https://www.sitepoint.com/write-for-us/", "dr": 87, "niche": ["Web Development", "Technology"]},
    {"name": "Slashdot", "url": "https://slashdot.org/submission", "dr": 91, "niche": ["Technology", "News"]},
    {"name": "ReadWrite", "url": "https://readwrite.com/contributor-guidelines/", "dr": 85, "niche": ["Technology"]},
    {"name": "TechWalls", "url": "https://www.techwalls.com/become-our-writer/", "dr": 56, "niche": ["Technology"]},
    {"name": "Inspiration Feed", "url": "https://inspirationfeed.com/guest-writing/", "dr": 75, "niche": ["Technology", "Design"]},
    {"name": "PragProg", "url": "https://write-with-us.pragprog.com/", "dr": 63, "niche": ["Technology", "Programming"]},
    {"name": "IAMWire", "url": "https://www.iamwire.com/submit-guest-post", "dr": 58, "niche": ["Technology"]},
    {"name": "VentureBeat", "url": "https://venturebeat.com/guest-posts/", "dr": 93, "niche": ["Technology", "Startups"]},
    {"name": "Manning", "url": "https://www.manning.com/write-for-us", "dr": 65, "niche": ["Technology", "Programming"]},
    {"name": "Making Different", "url": "https://www.makingdifferent.com/write-for-us/", "dr": 48, "niche": ["Technology"]},
    {"name": "TechLila", "url": "https://www.techlila.com/write-for-us/", "dr": 44, "niche": ["Technology"]},
    {"name": "TechiBhai", "url": "https://techibhai.com/write-for-us/", "dr": 38, "niche": ["Technology"]},
    {"name": "Colocation America", "url": "https://www.colocationamerica.com/lets-write", "dr": 51, "niche": ["Technology", "Web Hosting"]},
    {"name": "TechMaish", "url": "https://www.techmaish.com/write-for-us/", "dr": 43, "niche": ["Technology"]},
    {"name": "All Tech Buzz", "url": "https://www.alltechbuzz.net/contact/", "dr": 59, "niche": ["Technology"]},
    {"name": "Creately", "url": "https://creately.com/blog/write-for-us/", "dr": 70, "niche": ["Technology", "Productivity"]},
    {"name": "Milwaukee Magazine", "url": "https://www.milwaukeemag.com/writers-guidelines-milwaukee-magazine/", "dr": 62, "niche": ["Entertainment"]},
    {"name": "Contact Music", "url": "https://www.contactmusic.com/page/writeforus", "dr": 82, "niche": ["Entertainment", "Music"]},
    {"name": "Smashing Magazine", "url": "https://www.smashingmagazine.com/write-for-us/", "dr": 89, "niche": ["Web Design", "Development"]},
    {"name": "Hongkiat", "url": "https://www.hongkiat.com/blog/write-for-us/", "dr": 86, "niche": ["Web Design", "Technology"]},
    {"name": "This Is Colossal", "url": "https://www.thisiscolossal.com/submissions/", "dr": 80, "niche": ["Design", "Art"]},
    {"name": "Speckyboy", "url": "https://speckyboy.com/contribute-an-article/", "dr": 64, "niche": ["Web Design"]},
    {"name": "Web Designer Depot", "url": "https://www.webdesignerdepot.com/write-for-us/", "dr": 80, "niche": ["Web Design"]},
    {"name": "InDesign Secrets", "url": "https://indesignsecrets.com/write-for-us", "dr": 53, "niche": ["Design"]},
    {"name": "Web Design Ledger", "url": "https://webdesignledger.com/contact/", "dr": 83, "niche": ["Web Design"]},
    {"name": "Vandelay Design", "url": "https://www.vandelaydesign.com/write-for-us/", "dr": 64, "niche": ["Web Design"]},
    {"name": "Fatbit", "url": "https://www.fatbit.com/fab/write-for-fablog/", "dr": 50, "niche": ["Web Design"]},
    {"name": "Quertime", "url": "https://www.quertime.com/write-for-us/", "dr": 51, "niche": ["Web Design"]},
    {"name": "Cats Who Code", "url": "https://catswhocode.com/contact/", "dr": 49, "niche": ["Web Development"]},
    {"name": "A List Apart", "url": "https://alistapart.com/about/contribute/", "dr": 78, "niche": ["Web Design", "Development"]},
    {"name": "Creative Bloq", "url": "https://www.creativebloq.com/news/write-creative-bloq-contributor-network-612326", "dr": 87, "niche": ["Design"]},
    {"name": "InstantShift", "url": "https://www.instantshift.com/contribute/", "dr": 70, "niche": ["Web Design"]},
    {"name": "Men with Pens", "url": "https://menwithpens.ca/guest-post-guidelines/", "dr": 50, "niche": ["Writing", "Content"]},
    {"name": "Crazy Leaf Design", "url": "https://www.crazyleafdesign.com/blog/contributors/", "dr": 49, "niche": ["Web Design"]},
    {"name": "Append To", "url": "https://appendto.com/write-for-us/", "dr": 49, "niche": ["Web Development"]},
    {"name": "Collective Ray", "url": "https://www.collectiveray.com/about-us/product-reviews", "dr": 42, "niche": ["Web Design"]},
    {"name": "Writers Relief", "url": "https://writersrelief.com/guest-blogging/", "dr": 51, "niche": ["Writing"]},
    {"name": "Investopedia", "url": "https://www.investopedia.com/about-us", "dr": 91, "niche": ["Finance"]},
    {"name": "Bigger Pockets", "url": "https://www.biggerpockets.com/contact-us", "dr": 83, "niche": ["Real Estate", "Finance"]},
    {"name": "Investing.com", "url": "https://www.investing.com/about-us/editorial-guidelines", "dr": 89, "niche": ["Finance"]},
    {"name": "Finances Online", "url": "https://financesonline.com/write-for-us/", "dr": 69, "niche": ["Finance"]},
    {"name": "Wise Bread", "url": "https://www.wisebread.com/make-money-writing-for-wise-bread", "dr": 72, "niche": ["Finance"]},
    {"name": "I Will Teach You To Be Rich", "url": "https://www.iwillteachyoutoberich.com/write-a-guest-post-for-i-will-teach-you-to-be-rich/", "dr": 68, "niche": ["Finance"]},
    {"name": "Money Saving Mom", "url": "https://moneysavingmom.com/guest-post-submission-form/", "dr": 68, "niche": ["Finance"]},
    {"name": "Modest Money", "url": "https://www.modestmoney.com/modest-money-guest-post-policy", "dr": 54, "niche": ["Finance"]},
    {"name": "Geek Estate Blog", "url": "https://geekestateblog.com/contribute/", "dr": 45, "niche": ["Finance"]},
    {"name": "Oil Price", "url": "https://oilprice.com/write-for-oilprice", "dr": 82, "niche": ["Finance", "Energy"]},
    {"name": "Money Crashers", "url": "https://www.moneycrashers.com/write-for-us/", "dr": 73, "niche": ["Finance"]},
    {"name": "Money Mini Blog", "url": "https://moneyminiblog.com/write-for-us/", "dr": 50, "niche": ["Finance"]},
    {"name": "The Military Wallet", "url": "https://themilitarywallet.com/write-for-military-finance-network/", "dr": 55, "niche": ["Finance", "Military"]},
    {"name": "Income Diary", "url": "https://www.incomediary.com/write-for-incomediary", "dr": 59, "niche": ["Make Money", "Entrepreneurship"]},
    {"name": "Online Income Teacher", "url": "https://onlineincometeacher.com/write-for-us/", "dr": 43, "niche": ["Make Money"]},
    {"name": "Leaving Work Behind", "url": "https://leavingworkbehind.com/guest-post/", "dr": 46, "niche": ["Make Money", "Entrepreneurship"]},
    {"name": "Entrepreneur.com", "url": "https://www.entrepreneur.com/contact", "dr": 92, "niche": ["Entrepreneurship"]},
    {"name": "Entrepreneurship Secret", "url": "https://www.entrepreneurshipsecret.com/about-us/", "dr": 34, "niche": ["Entrepreneurship"]},
    {"name": "Inc42", "url": "https://inc42.com/contact/", "dr": 72, "niche": ["Entrepreneurship", "Startups"]},
    {"name": "Addicted 2 Success", "url": "https://addicted2success.com/write-for-us/", "dr": 63, "niche": ["Entrepreneurship"]},
    {"name": "Startup Nation", "url": "https://startupnation.com/contribute/", "dr": 61, "niche": ["Entrepreneurship", "Startups"]},
    {"name": "Killer Startups", "url": "https://www.killerstartups.com/guest-posts/", "dr": 59, "niche": ["Entrepreneurship", "Startups"]},
    {"name": "YFS Magazine", "url": "https://yfsmagazine.com/contribute/", "dr": 58, "niche": ["Entrepreneurship"]},
    {"name": "Foundr", "url": "https://foundr.com/contributors-form", "dr": 57, "niche": ["Entrepreneurship", "Startups"]},
    {"name": "Startup Bros", "url": "https://startupbros.com/guest-blogging/", "dr": 53, "niche": ["Entrepreneurship"]},
    {"name": "Small Biz Club", "url": "https://smallbizclub.com/write-for-us/", "dr": 44, "niche": ["Entrepreneurship"]},
    {"name": "International Living", "url": "https://internationalliving.com/about-il/write-for-il/", "dr": 69, "niche": ["Travel", "Lifestyle"]},
    {"name": "Escape Artist", "url": "https://www.escapeartist.com/write-us/", "dr": 61, "niche": ["Travel", "Lifestyle"]},
    {"name": "Scotsman Guide", "url": "https://www.scotsmanguide.com/Residential/WriteforUs", "dr": 52, "niche": ["Real Estate"]},
    {"name": "Forbes", "url": "https://www.forbes.com/contact/#6c03d38f7de2", "dr": 95, "niche": ["News", "Business"]},
    {"name": "The Guardian", "url": "https://www.theguardian.com/careers/guardian-careers-guidelines-for-contributors-and-writers", "dr": 95, "niche": ["News"]},
    {"name": "Wall Street Journal", "url": "https://www.wsj.com/articles/oped-guidelines-for-the-wall-street-journal-1384383173", "dr": 94, "niche": ["News", "Finance"]},
    {"name": "Fast Company", "url": "https://www.fastcompany.com/3008467/guidelines-submitting-contributed-articles-fast-company-and-tips-getting-published", "dr": 93, "niche": ["Business", "Innovation"]},
    {"name": "Medium", "url": "https://docs.google.com/forms/d/e/1FAIpQLScrz0kcSTcl6MrGJF-13l2MMSZJ3BBZtt6_znfxb4FwMLQiSQ/viewform", "dr": 99, "niche": ["Publishing"]},
    {"name": "Above the Law", "url": "https://abovethelaw.com/2016/08/how-you-can-write-for-above-the-law/", "dr": 78, "niche": ["Law"]},
    {"name": "Attorney at Work", "url": "https://www.attorneyatwork.com/writing-guidelines/", "dr": 49, "niche": ["Law"]},
    {"name": "ABA for Law Students", "url": "https://abaforlawstudents.com/2016/01/07/write-for-us/", "dr": 48, "niche": ["Law"]},
    {"name": "LawFuel", "url": "https://www.lawfuel.com/write-lawfuel/", "dr": 52, "niche": ["Law"]},
]

print(f"WebmeTools entries: {len(webmetools_entries)}\n")

# Create map of existing posts by normalized URL
def normalize_url(url):
    return url.lower().rstrip("/")

url_map = {}
for post in main_posts:
    url_norm = normalize_url(post["url"])
    url_map[url_norm] = post

# Merge webmetools entries
duplicates_found = 0
new_entries = 0
updated_entries = []

for wm_entry in webmetools_entries:
    url_norm = normalize_url(wm_entry["url"])
    
    if url_norm in url_map:
        # Duplicate found - add webmetools.com to sources
        existing_post = url_map[url_norm]
        if "webmetools.com" not in existing_post["listedOn"]:
            existing_post["listedOn"].append("webmetools.com")
            duplicates_found += 1
            updated_entries.append(existing_post["name"])
    else:
        # New entry - create JSON object with proper structure
        new_post = {
            "id": wm_entry["name"].lower().replace(" ", "-").replace(".", ""),
            "name": wm_entry["name"],
            "url": wm_entry["url"],
            "dr": wm_entry["dr"],
            "description": f"Guest post opportunity from webmetools.com.",
            "niche": wm_entry["niche"],
            "submissionType": "free",
            "listedOn": ["webmetools.com"],
            "notes": ""
        }
        main_posts.append(new_post)
        url_map[url_norm] = new_post
        new_entries += 1

# Sort by DR descending
main_posts.sort(key=lambda x: x.get("dr", 0), reverse=True)

# Save back
main_data["guestPosts"] = main_posts
with open(data_dir / "guest-posts.json", "w") as f:
    json.dump(main_data, f, indent=2)

print(f"=== Merge Summary ===")
print(f"Total entries: {len(main_posts)}")
print(f"Duplicates consolidated: {duplicates_found}")
print(f"  Examples: {', '.join(updated_entries[:5])}")
print(f"New entries added: {new_entries}")
print(f"\nFile saved to: {data_dir / 'guest-posts.json'}")
