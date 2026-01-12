import json
import re
from urllib.parse import urlparse

# Parse the new data from launchdirectories.com
new_data_text = """PeerPush
peerpush.net
37

A community-driven startup directory with high domain rating that rewards you for spotlighting the next big thing while showcasing your own growth journey.
Visit Site
DR: 68
Dofollow
Free
Shipybara
shipybara.com
19

Launch your startup, get seen by early adopters
Visit Site
DR: 49
Dofollow
Freemium
New
HUNT0
hunt0.com
1

LaunchPad - Ship Early. Hunt Early.
Visit Site
DR: 22
3
Dofollow
Freemium
Reddit
reddit.com
109

The front page of the internet - diverse communities and discussions.
Visit Site
DR: 95
Nofollow
Free
Sourceforge
sourceforge.net
7

Platform for sharing and reviewing open-source and commercial software.
Visit Site
DR: 92
Dofollow
Freemium
TechCrunch
techcrunch.com
47

Leading technology media property, dedicated to obsessively profiling startups.
Visit Site
DR: 92
Nofollow
Paid
Capterra
www.capterra.com
2

A site for comparing business software.
Visit Site
DR: 91
Dofollow
Freemium
Product Hunt
www.producthunt.com
40

The premier platform for discovering and launching new products daily.
Visit Site
DR: 91
Nofollow
Free
G2
www.g2.com
2

Platform for discovering and comparing software.
Visit Site
DR: 91
Dofollow
Freemium
Hacker News
news.ycombinator.com
15

Y Combinator's community-driven tech news and startup discussion platform.
Visit Site
DR: 91
Nofollow
Free
Launched by Lovable
launched.lovable.app
6

Showcase of projects built with Lovable platform.
Visit Site
DR: 87
1
Dofollow
Free
AngelList
angel.co
15

The world's largest startup community for investors, entrepreneurs, and job seekers.
Visit Site
DR: 87
Dofollow
Freemium
StartupFA.me
startupfa.me
12

Directory for finding and submitting startup tools and resources.
Visit Site
DR: 82
Dofollow
Paid
Indie Hackers
indiehackers.com
11

Community of developers who are sharing the strategies behind their companies.
Visit Site
DR: 80
Dofollow
Free
AlternativeTo
alternativeto.net
10

Crowdsourced software recommendations and alternatives.
Visit Site
DR: 79
Nofollow
Free
Dang AI
dang.ai
3

Directory of AI tools and artificial intelligence resources.
Visit Site
DR: 79
Dofollow
Free
Fazier
fazier.com
2

Marketplace for SaaS products and startup tools.
Visit Site
DR: 79
Dofollow
Freemium
Twelve Tools
twelve.tools
1

Curated collection of tools for entrepreneurs and makers.
Visit Site
DR: 79
1
Dofollow
Freemium
There's An AI For That
theresanaiforthat.com
1

Comprehensive database of AI tools for every use case.
Visit Site
DR: 77
Dofollow
Paid
Turbo0
turbo0.com
2

Fast-track platform for launching products quickly.
Visit Site
DR: 77
Dofollow
Paid
SaaSHub
www.saashub.com
8

Software alternatives and reviews platform.
Visit Site
DR: 76
Dofollow
Free
Toolpilot
www.toolpilot.ai
1

AI tools discovery and directory
Visit Site
DR: 76
Dofollow
Paid
Peerlist
peerlist.io
3

Network and portfolio platform for tech professionals.
Visit Site
DR: 75
Nofollow
Free
BetaList
betalist.com
7

Platform for discovering and getting early access to tomorrow's startups.
Visit Site
DR: 74
Dofollow
Free
findly.tools
findly.tools

The best tools, all in one place.
Visit Site
DR: 74
1
Dofollow
Freemium
Uneed
www.uneed.best
1

Curated directory of the best tools for entrepreneurs.
Visit Site
DR: 73
Dofollow
Paid
Alternative.me
alternative.me
5

Find alternatives to popular software and services.
Visit Site
DR: 73
Dofollow
Free
SoftwareWorld
www.softwareworld.co
1

Find The Best Software & Services For Your Business
Visit Site
DR: 73
Dofollow
Freemium
LaunchIgniter
launchigniter.com
3

Launch Platform
Visit Site
DR: 72
1
Nofollow
Freemium
magicbox.tools
magicbox.tools

Featuring over 20,000 awesome AI tools
Visit Site
DR: 72
Dofollow
Freemium
SubmitAiTools
submitaitools.org
1

Simple platform to discover and share AI tools.
Visit Site
DR: 72
Nofollow
Paid
SideProjectors
www.sideprojectors.com
1

Community for sharing and discovering side projects.
Visit Site
DR: 70
Dofollow
Freemium
TinyLaunch
www.tinylaunch.com
3

Product launch platform with visibility
Visit Site
DR: 69
Dofollow
Freemium
Future Tools
www.futuretools.io
3

Directory of AI tools and future technology.
Visit Site
DR: 68
Dofollow
Free
AiTools
aitools.inc

Handy directory for finding AI tools
Visit Site
DR: 67
Nofollow
Freemium
toolsfine
toolsfine.com
1

better tools, better work
Visit Site
DR: 67
Dofollow
Free
aiwith.me
aiwith.me
1

Discover the latest and best AI tools
Visit Site
DR: 66
1
Dofollow
Paid
Startup Stash
startupstash.com
2

Curated directory of resources and tools for startups.
Visit Site
DR: 65
Nofollow
Free
Indie Deals
www.indie.deals
1

Deals and discounts for indie makers and startups.
Visit Site
DR: 60
Dofollow
Paid
Pitchwall
pitchwall.co

Premium startup showcase
Visit Site
DR: 60
Nofollow
Freemium
DevHunt
devhunt.org

Product Hunt for developers - showcase developer tools.
Visit Site
DR: 59
1
Dofollow
Free
Super Launch
www.superlaun.ch
5

A product launch platform cum directory.
Visit Site
DR: 57
2
Dofollow
Freemium
MicroLaunch
microlaunch.net
3

Platform for launching and discovering micro startups.
Visit Site
DR: 57
2
Dofollow
Free
Open Launch
open-launch.com
5

Open platform for product launches and feedback.
Visit Site
DR: 57
1
Dofollow
Free
acidtools.com
acidtools.com

Directory of productivity & AI tools.
Visit Site
DR: 56
Dofollow
Free
IdeaKiln
ideakiln.com
1

A community-driven directory for early-stage startup ideas, prototypes, and MVPs.
Visit Site
DR: 56
1
Dofollow
Free
Firsto
firsto.co
6

Firsto is a product‑launch platform tailored for indie makers, developers, and startups. It offers a fair, visibility‑first environment where every submitted project gains exposure, unlike curated or exclusive platforms with gatekeepers.
Visit Site
DR: 56
2
Nofollow
Free
startupfa.st
www.startupfa.st

Startup directory
Visit Site
DR: 56
4
Nofollow
Freemium
AgentHunter
www.agenthunter.io
1

Best AI Agents in One Place
Visit Site
DR: 55
Dofollow
Freemium
Startups Lab
startupslab.site

Showcase your startup
Visit Site
DR: 55
1
Dofollow
Freemium
Scoutforge
scoutforge.net
1

Discover new apps with unbiased reviews
Visit Site
DR: 51
Dofollow
Freemium
Launching Next
www.launchingnext.com

Platform for announcing upcoming product launches.
Visit Site
DR: 51
1
Dofollow
Free
Open Alternative
openalternative.co
2

Open source alternatives to popular software.
Visit Site
DR: 51
2
Dofollow
Free
TrustMRR
trustmrr.com
2

The database of verified startup revenues
Visit Site
DR: 51
1
Dofollow
Free
Tiny Startups
tinystartups.com
3

Community for small startups and indie hackers.
Visit Site
DR: 50
Dofollow
Free
MakerThrive
makerthrive.com
2

Community and resources for makers and creators.
Visit Site
DR: 50
1
Dofollow
Freemium
Openhunts
openhunts.com
1

Launch and hunt products openly.
Visit Site
DR: 49
Nofollow
Free
AI Tech Viral
aitechviral.com

AI Tech Viral is a simple directory for sharing AI tools
Visit Site
DR: 49
Nofollow
Free
Promote Project
www.promoteproject.com

Platform for promoting and marketing your projects.
Visit Site
DR: 48
1
Dofollow
Free
SaasHunt
saashunt.best

Product Hunt Alternative for SaaS products
Visit Site
DR: 48
2
Dofollow
Freemium
Unite List
unitelist.com

Unite List is a straightforward directory where makers and SaaS creators can easily find and add useful digital tools.
Visit Site
DR: 47
1
Dofollow
AiTools
aitools.fyi
2

Find Best AI Tools That Make Your Life Easy!
Visit Site
DR: 47
Dofollow
Paid
StartupTrusted
startuptrusted.com

Discover trusted startups and submit your own to get discovered.
Visit Site
DR: 47
3
Dofollow
Freemium
A
AppaList
appalist.com

Explore software solutions that take your productivity to the next level
Visit Site
DR: 46
Dofollow
Freemium
Huzzler
huzzler.so
1

Platform for discovering and promoting new startup projects.
Visit Site
DR: 46
Dofollow
Freemium
FoundrList
foundrlist.com
12

SaaS and startup directory
Visit Site
DR: 46
8
Dofollow
Free
SoloPush
solopush.com
1

Platform for solo entrepreneurs to promote their projects.
Visit Site
DR: 45
Dofollow
Paid
We Like Tools
weliketools.com

We Like Tools celebrates the best productivity solutions. Discover tools that we genuinely recommend and love.
Visit Site
DR: 44
Nofollow
Freemium
startuplist.ing
startuplist.ing
5

All-in-one platform for builders
Visit Site
DR: 41
1
Dofollow
Paid
Toolfio
toolfio.com

The ultimate hub for finding and showcasing SaaS products.
Visit Site
DR: 41
Dofollow
Free
Micro SaaS Examples
www.microsaasexamples.com
1

Explore the best micro saas ideas from the internet.
Visit Site
DR: 40
1
Nofollow
Free
Awesome Tools
awesome.tools
1

Best Awesome Tools for Startups
Visit Site
DR: 40
1
Nofollow
Freemium
ProductBurst
productburst.com
1

Daily featured products and startup showcases.
Visit Site
DR: 39
Dofollow
Free
I
IndieHub
indiehub.best

All-in-One Directory for Indie Makers
Visit Site
DR: 39
Nofollow
Paid
toolfolio
toolfolio.io

All the tools & resources you need, in one place.
Visit Site
DR: 38
Nofollow
Freemium
R
RankYourAI
rankyourai.com

Ranking and review platform for AI tools.
Visit Site
DR: 38
1
Dofollow
Free
StartupBase
startupbase.io
3

Database and directory of startup companies.
Visit Site
DR: 38
Dofollow
Freemium
Saaspa.ge
www.saaspa.ge
4

Saas Products Directory
Visit Site
DR: 36
1
Dofollow
Free
ShipYard HQ
shipyardhq.dev

Shipyard shows what builders are actually clicking on.
Visit Site
DR: 35
1
Dofollow
Freemium
Launch
trylaunch.ai

The best new AI products. Every day.
Visit Site
DR: 35
2
Dofollow
Freemium
Startups.fm
startups.fm

Podcast and community focused on startup stories.
Visit Site
DR: 35
1
Dofollow
Paid
Best of Web
www.bestofweb.site

All-in-One Growth Platform
Visit Site
DR: 35
Dofollow
Free
Proofstories
proofstories.io
1

A collection of tools sharing how they won their first customers.
Visit Site
DR: 34
2
Dofollow
Freemium
1000.tools
1000.tools

An exclusive list of the 1000 best tools. Carefully vetted and maintained by humans.
Visit Site
DR: 34
1
Nofollow
Paid
TinyLaunchpad
tinylaunchpad.com

Fresh products and startups launched every Monday.
Visit Site
DR: 33
23
Dofollow
Freemium
neeed.directory
neeed.directory
1

Tools Directory
Visit Site
DR: 33
Dofollow
EuroAlternative
euroalternative.co
1

Discover European Alternatives to Big Tech Companies
Visit Site
DR: 32
2
Dofollow
Free
ConfettiSaaS
confettisaas.com
1

ConfettiSaaS.com is a platform for showcasing and discovering confetti-powered apps.
Visit Site
DR: 32
1
Dofollow
Freemium
Resource.fyi
resource.fyi

Collection of useful resources for entrepreneurs.
Visit Site
DR: 30
Dofollow
Free
FindYourSaaS
www.findyoursaas.com
1

Discover and compare SaaS products for your business.
Visit Site
DR: 29
Dofollow
Freemium
Made with Lovable
madewithlovable.com
5

Showcase of websites and apps built with Lovable.
Visit Site
DR: 28
Dofollow
Free
hot100
www.hot100.ai
12

The weekly chart for indie AI projects and Vibe Coders.
Visit Site
DR: 28
1
Dofollow
Free
ToolHub
toolhub.me
1

Central hub for discovering useful tools and apps.
Visit Site
DR: 28
1
Dofollow
Paid
S
Startups.fyi
startups.fyi
2

Information and resources for startup founders.
Visit Site
DR: 28
1
Dofollow
Paid
I
IndieHackerStacks
indiehackerstacks.com
1

Discover the best tools from fellow indie hackers to build your product.
Visit Site
DR: 27
Dofollow
Daily Pings
dailypings.com

Daily digest of new product launches and startup news.
Visit Site
DR: 27
1
Dofollow
Freemium
AwesomeIndie
awesomeindie.com
2

Awesome Indie is a curated platform for discovering indie products, side projects, and micro-startups
Visit Site
DR: 26
1
Nofollow
Free
Saassy Board
saassy-board.com
3

Launch SaaS, earn rewards, fight hunger
Visit Site
DR: 25
1
Dofollow
Paid
madewithbolt
madewithbolt.com
2

A collection of apps and websites made with Bolt.new
Visit Site
DR: 24
Nofollow
Free
S
SubmitHunt
www.submithunt.com
1

Visual showcase for startups
Visit Site
DR: 24
Dofollow
Paid
New
R
rankinpublic.xyz
rankinpublic.xyz

Live product rankings
Visit Site
DR: 23
3
Nofollow
Freemium
New
Top10
top10.now
1

Top 10 lists of tools and services in various categories.
Visit Site
DR: 23
Dofollow
Freemium
New
Stellar Launch
stellarlaunch.org

Where products keep getting discovered after launch day.
Visit Site
DR: 22
Nofollow
Freemium
New
BuildVoyage
buildvoyage.com

Discover and track real micro‑SaaS journeys
Visit Site
DR: 20
Dofollow
Freemium
New
J
Justgotfound
justgotfound.com

Discover Amazing Products
Visit Site
DR: 20
Dofollow
Free
Toollist
toollist.ai

Directory of Artificial Intelligence Tools
Visit Site
DR: 19
Dofollow
Paid
New
Launch Vibe
www.launchvibe.app

Launch to 1000s of founders
Visit Site
DR: 8
Dofollow
Free
startuups
startuups.com
1

Launch platform for SaaS products
Visit Site
DR: 3
Dofollow
Freemium"""

# Parse the data
entries = []
lines = [line.strip() for line in new_data_text.split('\n') if line.strip()]

i = 0
while i < len(lines):
    if not lines[i] or lines[i].startswith('Visit Site'):
        i += 1
        continue
    
    # Try to parse entry
    name = lines[i]
    
    # Skip lines that are just "A", "I", "R", "S", "J" (formatting)
    if len(name) == 1:
        i += 1
        continue
    
    # Find URL/domain
    i += 1
    if i >= len(lines):
        break
    
    url_line = lines[i]
    
    # Extract URL
    if url_line.startswith('www.'):
        url = 'https://' + url_line
    elif url_line.startswith('http'):
        url = url_line
    elif '.' in url_line and not url_line.startswith('DR:'):
        url = 'https://' + url_line
    else:
        i += 1
        continue
    
    # Skip numbers/empty lines
    i += 1
    while i < len(lines) and (lines[i].isdigit() or lines[i] == '' or lines[i].startswith('New')):
        i += 1
    
    # Get description
    description = ""
    if i < len(lines) and not lines[i].startswith('DR:'):
        description = lines[i]
        i += 1
    
    # Skip to DR line
    while i < len(lines) and not lines[i].startswith('DR:'):
        i += 1
    
    if i >= len(lines):
        continue
    
    # Parse DR, Follow type, and submission type
    dr_match = re.search(r'DR:\s*(\d+)', lines[i])
    dr = int(dr_match.group(1)) if dr_match else 0
    
    # Filter out DR < 30
    if dr < 30:
        # Skip this entry
        i += 1
        while i < len(lines) and not (lines[i] and len(lines[i]) > 1 and lines[i][0].isupper() and not lines[i].startswith('DR:') and not lines[i].startswith('Visit')):
            i += 1
        continue
    
    i += 1
    
    # Get follow type and submission type
    followtype = "unknown"
    submissiontype = "unknown"
    
    if i < len(lines) and lines[i] in ["Dofollow", "Nofollow"]:
        followtype = lines[i].lower()
        i += 1
    
    if i < len(lines) and lines[i] in ["Free", "Paid", "Freemium"]:
        submissiontype = lines[i].lower()
        i += 1
    
    entries.append({
        "name": name,
        "url": url,
        "description": description,
        "dr": dr,
        "followtype": followtype,
        "submissiontype": submissiontype
    })

print(f"Parsed {len(entries)} entries with DR >= 30")

# Load existing directories
with open('c:\\Users\\bmaff\\OneDrive\\Desktop\\Code projects\\trading-moon-services\\public\\data\\directories.json', 'r') as f:
    data = json.load(f)

existing_dirs = {d['url'].lower(): d for d in data['directories']}
print(f"Existing directories: {len(existing_dirs)}")

# Merge entries
source_name = "launchdirectories.com"
merged_count = 0
added_count = 0

for entry in entries:
    url_key = entry['url'].lower()
    
    if url_key in existing_dirs:
        # Add source to existing entry
        existing_dirs[url_key]['listedOn'].append(source_name)
        existing_dirs[url_key]['listedOn'] = list(set(existing_dirs[url_key]['listedOn']))  # Remove duplicates
        merged_count += 1
    else:
        # Add new entry
        new_id = entry['name'].lower().replace(' ', '-').replace('.', '')
        
        new_entry = {
            "id": new_id,
            "name": entry['name'],
            "url": entry['url'],
            "description": entry['description'],
            "type": ["Launch Platform", "SaaS Directory"],  # Default types
            "domainRating": entry['dr'],
            "submissionType": entry['submissiontype'],
            "followType": entry['followtype'],
            "listedOn": [source_name],
            "notes": f"Added from {source_name}"
        }
        
        data['directories'].append(new_entry)
        added_count += 1

print(f"Merged: {merged_count}, Added: {added_count}")

# Save updated data
with open('c:\\Users\\bmaff\\OneDrive\\Desktop\\Code projects\\trading-moon-services\\public\\data\\directories.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Updated directories.json with {merged_count} merged and {added_count} new entries")
