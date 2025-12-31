#!/usr/bin/env python3
"""
Script to merge TopSaaS Directories list into directories.json
Handles both new entries and updating existing ones
"""

import json
import re

DIRS_PATH = r"C:\Users\bmaff\OneDrive\Desktop\Code projects\trading-moon-services\data\directories.json"

# TopSaaS data (pasted directly)
TOPSAAS_DATA = """
MCP Server Directory
AI Directory
Developer Tools
Directory

A curated directory of Model Context Protocol (MCP) servers for connecting AI models with external applications, streamlining AI integration.
There's An AI For That
AI Directory

#1 website for AI tools worldwide
BetaList
Directory
Launch Platform
AI Directory

Discover upcoming internet startups and get early access to the future with BetaList's curated overview.
Peerlist Launchpad
Launch Platform

Discover and support innovative projects on Peerlist Launchpad, a platform for launching, feedback, and early user acquisition.
Product Hunt
Launch Platform

Product Hunt is a platform for discovering and launching new tech products, offering daily curated lists and community discussions.
r/SideProject
Directory
AI Directory

r/SideProject - A community for sharing side projects
Open-Launch
Developer Tools
Launch Platform

The first complete open source alternative to Product Hunt.
Micro SaaS Examples
Directory
AI Directory

Discover curated micro SaaS examples, explore innovative products, and get inspired to launch your own successful venture.
Its Launch Day
Launch Platform
Directory

A fair platform for product launches that helps indie makers gain visibility through social sharing campaigns
Stripe Climate
Directory

Stripe Climate enables businesses to remove carbon as they grow by directing a percentage of revenue to support carbon removal technologies.
Dev to
Developer Tools
Business Profile

DEV Community is a social network for software developers to share, stay up-to-date, and grow their careers through collaboration.
HackerNoon
Directory

HackerNoon is a free platform with 25k+ contributing writers where 100M+ humans learn about technology, offering insightful stories and expertise.
A1
Directory

A collection of the best websites found on the web
Lead.dev
Directory
Developer Tools

Lead.dev is a platform for developers to share their startups, compete on a leaderboard, get feedback, and find new users.
Indie Hackers
Launch Platform

A daily leaderboard of build-in-public posts
SideProjectors
Developer Tools
Directory
AI Directory

A marketplace for side projects and developer tools
OpenAlternative

A curated collection of the best open source alternatives to everyday SaaS products. Save money with reliable tools hand-picked for you
Microlaunch
Launch Platform

A Launch Platform for World-Class Startups
Sourceforge
Directory
AI Directory

Compare business software to find the best tools. Create, collaborate & distribute to nearly 20 million users worldwide.
Tiny Launch
Launch Platform

TinyLaunch is a platform to discover and launch new products, offering badges and backlinks for top weekly launches.
F6S
Directory
AI Directory

Platform connecting startups with investors and valuable resources worldwide
Dev Resources
Developer Tools
Directory
AI Directory

A curated list of 800+ resources for developers, categorized and crowdsourced, covering programming, UI, APIs, and much more.
Once Tools
Directory
AI Directory

Your guide to software you only have to pay for once, discover tools and resources with one-time payment options.
GetByte
Directory
AI Directory

A platform empowering startups by providing a place to list their products and grow their businesses.
Tools Fine
AI Directory

Your guide to the best AI tools and apps of 2024, helping internet workers find accessible and reliable AI solutions.
WebCatalog
Directory
AI Directory

Discover and access thousands of web apps through a curated app library, optimized for productivity and ease of use on WebCatalog.
La Chief
AI Directory

Lachief.io is an AI tool directory to discover and simplify work, life, and education with 1000+ AI tools and websites.
Land Book
Directory

Land-book is a curated website design gallery updated daily, offering inspiration for creatives seeking the best hand-picked designs.
Genai Works
AI Directory

Your AI hub for learning, discovering innovations, and exploring top AI products for business and creativity.
Resource FYI
Launch Platform
Directory
AI Directory

A curated directory of free tools, resources, and products for developers, designers, marketers, and tech enthusiasts
FiveTaco
AI Directory
Directory

FiveTaco helps solopreneurs discover the best software solutions vetted for their specific needs, boosting their hustle to the next level
Neil Patel AI Tools
AI Directory

Explore thousands of free and paid tools to kickstart your next big idea
Pinterest
Business Profile

Pinterest Business helps businesses grow by providing marketing tools, advertising solutions, and resources to connect with their target audience
SaaSHub
Directory
Launch Platform
AI Directory

SaaSHub helps software professionals discover new software, find alternatives, and read reviews to grow their business since 2014
Whatsnew
Directory
AI Directory
Developer Tools

Whatsnew.co showcases companies and their latest updates, focusing on AI, tools, and resources for business, productivity, and development.
Bento
Bio

Bento is a platform to create a rich and beautiful personal page, acting as a superior link-in-bio solution
Futuretools
AI Directory
Directory

FutureTools collects & organizes AI tools, helping users discover the exact AI solution for their needs and become superhuman!
Saas AI Tools
AI Directory

SaaS AI Tools is a directory of AI-powered tools to help supercharge your creativity to the next level
AI Tools Inc
AI Directory

Discover AI Tools to automate workflows and 10x output, with a directory of AI tech for various tasks and industries.
Launching Next
Directory
AI Directory

Launching Next showcases promising new startups daily, featuring tech, mobile, web, and green business ideas to a broad audience
Review AI
AI Directory

ReviewAI is the largest AI tools directory, with 3500+ AI tools over 80+ categories like content generator, video editing, image ai creator
Next AI Tool
AI Directory

The Next AI Tool is a directory that provides a comprehensive list of new AI tools across multiple categories, updated daily
Startup Buffer
Directory
AI Directory

Startup Buffer: A premium startup directory to promote your startup or discover new ventures. Submit for free and gain visibility!
Marsx Curated AI tools
AI Directory

Curated list of 600+ AI tools for startup founders, based on GPT3+ and other generative AI, to help bring innovative ideas to market.
Stork AI
AI Directory

Discover AI tools for ChatGPT, Claude, Midjourney, and more to streamline workflows and boost productivity without monthly fees
AI Tools
AI Directory

AI Tool Details is an AI hub exploring AI tools and forums, enabling users to share AI tools and news
Makers
Bio

Make.rs is a platform where makers can showcase their projects and creations to the world
Ramen Tools
Directory
Business Profile

Discover the tech stacks of 2000+ indie makers, solopreneurs, and startups. Explore tools for building, launching, and promoting products.
Owwly
Directory

Owwly is a comprehensive platform that provides a curated list of the latest AI tools, empowering users to explore and integrate cutting-edge technologies.
Fazier
Launch Platform

Fazier helps you discover new tech startups and products every day, offering a platform to submit your own product for free.
AI Depot
AI Directory

AI Depot is a directory showcasing new AI tools, providing a platform to discover and explore innovative AI solutions for various applications.
Discover Waivly
Directory
Launch Platform
AI Directory

Explore tech products, launch tips, and growth strategies for software engineers and tech enthusiasts.
Awesome Indie
Directory
AI Directory
Developer Tools

Discover trending indie products & micro startups: AI tools, SaaS platforms, and developer resources for makers and entrepreneurs.
Growth Boosters
Directory
AI Directory

Find the best tools for startups and entrepreneurs. Discover curated marketing tools to grow your business efficiently.
Web Wiki
Directory
Business Profile

Webwiki is a search engine with website reviews, helping users find trustworthy sites and share experiences. It analyzes website data for insights.
Deepgram
AI Directory

Deepgram's curated directory of AI apps, tools, services & software for image generation, chatbots, writing, coding, video, audio, and more.
Link Centre
Directory

Link Centre is an internet directory and search engine helping users find websites and resources since 1996, offering a categorized web directory.
Promote Project
Directory
AI Directory

A platform for startups to advertise, discover projects, and engage with a community of entrepreneurs.
Softgist
AI Directory

SoftGist is the #1 destination for finding AI tools, offering a curated directory of AI innovations for various needs.
AI Radar
AI Directory

GetInference AI Radar offers a directory of AI tools for marketing, content, and creative professionals.
Free For Dev
Directory
Developer Tools

A curated list of services offering free tiers for developers and open-source authors, helping them make informed decisions.
Top AI Tools
AI Directory

A curated list of AI tools, cataloging outstanding AI-powered products for art, productivity, developer tools, and more.
Awesome Generative AI
AI Directory

A curated list of Generative AI tools, works, models, and references, focusing on technical resources and practical applications.
Awesome AI-Powered Developer
Developer Tools
AI Directory

Curated list of AI-powered developer tools that leverage AI to assist in code completion, debugging, documentation, and more.
Codestash
Developer Tools
Directory

CodeStash is a curated directory of premium resources and tools for developers to boost productivity and streamline workflows.
PoweredbyAI
AI Directory

Your guide to the best free AI tools for 2025, helping businesses optimize operations and drive AI-driven growth.
Dev Suite
Developer Tools
Directory
AI Directory

Curated developer tools to build faster and ship sooner. Save time and cut costs with expertly curated tools.
FMHY
Directory

FMHY is the largest curated collection of free resources on the internet, focusing on media, entertainment, and software.
No Code Founders
Directory

A platform offering resources, tutorials, and community support for building online businesses without coding skills.
Code Market
Directory
AI Directory

Code.market is a curated library of creative tools, including AI tools, mobile and web templates, SaaS solutions, design files, and games.
EU Startups
Directory
AI Directory
Business Profile

Your guide to European startups, funding, and innovation. Discover insights, jobs, and databases for startup success.
Hackernews
Launch Platform

Hacker News "Show" page displays community projects, tools, and creations, offering a platform for developers to share and discover new tech.
Awesome AI Tools
AI Directory

A curated list of AI tools, models, and resources for text, code, image, video, audio generation, marketing, productivity, and learning.
Link Tree
Business Profile
Bio

Linktree helps users create a personalized and easily shareable page that hosts multiple links, streamlining online content discovery.
Appvizer
Directory
AI Directory

Appvizer is a media and software comparison tool for professionals to reinvent their business and thrive by finding the best software.
NoCode List
Directory

A directory of NoCode tools, agencies, and resources to help you build your business without code.
Bio Sites
Bio

Bio Sites by Squarespace lets you share everything you link to online from your link in bio on Instagram, TikTok, and other social media.
Chatgate AI
AI Directory

ChatGate AI is an all-in-one AI platform providing access to cutting-edge AI models and applications worldwide.
Find Dev Tools
Developer Tools
Directory

Curated directory of developer tools for easy comparison and discovery
Cloud Hiker
Directory

Cloudhiker is a curated directory of interesting, weird, and awesome websites, offering a unique exploration experience.
Startup Inspire
Directory
AI Directory

StartupInspiration is a platform to discover and promote startups, offering resources for founders and entrepreneurs to grow their ventures
App Rater
Directory

Discover awesome mobile apps daily since 2011. We curate mobile apps for your smartphone.
The AI Navigator
AI Directory

A comprehensive, manually curated list of AI tools, updated daily, designed to inspire and educate on the latest AI advancements.
Startup Lister
Directory
AI Directory

Discover and share new startups with the Startuplister community, a platform for showcasing and exploring innovative ventures.
Brouseai
AI Directory

Your AI library to boost productivity, enhance learning, and enjoy better entertainment. Explore incredible AI for your everyday life!
Starter Story
Directory
Business Profile

Starter Story interviews entrepreneurs, sharing their business journeys to inspire and provide actionable insights for aspiring founders.
Hunted.Space
Directory

Product Hunt launch calendars & statistics for upvotes, comments & upvote speed to understand successful product launches.
Open Graph Examples
Directory
AI Directory

Open Graph Examples provides advice, helpful content, and tools to make your Open Graph social cards stand out.
Webs URL
Directory
AI Directory

WebsURL is a website gallery showcasing web and interactive design, offering a platform to discover and appreciate innovative website creations.
Startus
Directory
AI Directory

StartUs is a European startup platform connecting founders, enthusiasts, and companies, offering jobs, co-founder matching, and resources.
StartupBase
Directory
AI Directory

Discover and share the latest startups. A community for makers & early adopters to discuss new products and ideas.
Geekwire
Directory
AI Directory
Business Profile

Submit your startup to GeekWire's Startup List database for potential inclusion and increased visibility within the tech community.
SaaS Worthy
Directory
AI Directory

SaaSworthy helps stakeholders make better product decisions with unbiased reviews, comparisons, and insightful guides.
Crozdesk
Directory
AI Directory

Crozdesk helps businesses discover, compare, and select the right software with expert reviews and user insights.
Dang.ai
AI Directory

Dang.ai is the best AI tools directory with 5000+ AI tools in categories like copywriting, image generators, video creators and more.
SoftwareSuggest
Directory
AI Directory
Business Profile

SoftwareSuggest offers a platform to discover business software, read expert reviews, compare features, and get free recommendations.
AI Forums
AI Directory
Business Profile

AI Forums: A community for discussing AI tools, ChatGPT, GPTs, and AI in entrepreneurship, offering news, discussions, and resources.
StartupHub AI
AI Directory
Developer Tools

StartupHub AI delivers data and tech news of the AI startup ecosystem, offering a market-leading startup database with AI-focused filters.
IndieMaker
Directory
AI Directory

IndieMaker is an invite-only community for indie makers to connect, share journeys, and celebrate progress, offering profiles and resources.
Zumvu Software Directory
Directory

Zumvu's Software Directory: Your guide to the best SaaS tools, AI platforms, and software solutions for business and productivity.
Automation Tools Directory
Directory
AI Directory
Developer Tools

Curated collection of automation tools for smarter workflows and higher productivity.
Uneed
Launch Platform

Uneed is a launch platform for tech products, offering a Product Hunt alternative with fair visibility for all creators.
Dev Hunt
Developer Tools
Launch Platform

Dev Hunt: A community-driven platform for discovering and voting on the best new developer tools every day, built open source.
ctrlalt.cc
Launch Platform

CtrlAltCC helps you discover new startup tools every day. See what products other people use, launch your own startup and find new users.
AI Alternative
AI Directory
Developer Tools

Discover the best AI tools and their alternatives
Toolhub
Directory
AI Directory

Find top business software tools to boost productivity and growth with our curated selection of essential solutions.
"""

def parse_topsaas():
    """Parse TopSaaS data - name followed by types and description"""
    entries = []
    lines = [l.strip() for l in TOPSAAS_DATA.strip().split('\n') if l.strip()]
    
    i = 0
    while i < len(lines):
        name = lines[i]
        i += 1
        
        # Skip if it looks like a description (too long or has certain markers)
        if len(name) > 60 or name.startswith('A ') or name.startswith('The '):
            if name.startswith('A ') or name.startswith('The '):
                i += 1  # Skip to next
            continue
        
        # Get types/tags until we hit a description
        types = []
        while i < len(lines) and len(lines[i]) < 60 and not lines[i][0].isupper():
            types.append(lines[i])
            i += 1
        
        # Description is next line
        description = ""
        if i < len(lines):
            description = lines[i]
            i += 1
        
        if name and description:
            entries.append({
                'name': name,
                'types': types,
                'description': description
            })
    
    return entries

def name_to_id(name):
    """Convert name to ID"""
    name_lower = name.lower().strip()
    id_str = re.sub(r'[^a-z0-9]', '-', name_lower)
    id_str = re.sub(r'-+', '-', id_str)
    id_str = id_str.strip('-')
    return id_str[:50]

def guess_type(types_list, name_lower):
    """Guess best type from available types"""
    if not types_list:
        return "Directory"
    
    # Prefer more specific types
    priority = ["AI Directory", "Developer Tools", "Launch Platform", "Directory", "Business Profile", "Bio"]
    for p in priority:
        for t in types_list:
            if p.lower() in t.lower():
                return p
    
    return types_list[0] if types_list else "Directory"

def load_existing():
    """Load existing directories.json"""
    with open(DIRS_PATH, 'r') as f:
        return json.load(f)

def find_matching_entry(name, existing_data):
    """Find if this entry already exists in our database"""
    name_lower = name.lower()
    for d in existing_data['directories']:
        if d['name'].lower() == name_lower:
            return d
    return None

def create_new_entry(name, types_list, description):
    """Create a new directory entry from TopSaaS data"""
    entry_type = guess_type(types_list, name.lower())
    
    return {
        "id": name_to_id(name),
        "name": name,
        "url": "",
        "description": description,
        "type": entry_type,
        "domainRating": "unknown",
        "submissionType": "unknown",
        "followType": "unknown",
        "listedOn": ["topsaasdirectories.com"],
        "notes": "URL, domain rating, submission type, and follow type not available from source"
    }

def main():
    print("Parsing TopSaaS Directories data...")
    topsaas_entries = parse_topsaas()
    print(f"Parsed {len(topsaas_entries)} entries")
    
    print("Loading existing directories...")
    data = load_existing()
    print(f"Currently have {len(data['directories'])} directories")
    
    new_count = 0
    updated_count = 0
    
    print("\nProcessing entries...")
    for entry in topsaas_entries:
        existing = find_matching_entry(entry['name'], data)
        
        if existing:
            # Update listedOn
            if "topsaasdirectories.com" not in existing['listedOn']:
                existing['listedOn'].append("topsaasdirectories.com")
                updated_count += 1
        else:
            # Add new entry
            new_entry = create_new_entry(entry['name'], entry['types'], entry['description'])
            data['directories'].append(new_entry)
            new_count += 1
    
    print(f"\n=== Results ===")
    print(f"New entries added: {new_count}")
    print(f"Existing entries updated: {updated_count}")
    
    # Save
    with open(DIRS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nTotal directories now: {len(data['directories'])}")

if __name__ == "__main__":
    main()
