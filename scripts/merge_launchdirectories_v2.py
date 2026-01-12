import json
import re
from urllib.parse import urlparse

# URL normalization function
def normalize_url(url):
    """Normalize URL for comparison"""
    # Remove protocol
    url = re.sub(r'^https?://', '', url).lower()
    # Remove trailing slash
    url = url.rstrip('/')
    # Remove www
    url = re.sub(r'^www\.', '', url)
    return url

# Load the new directories from launchdirectories.com
new_dirs = [
    {
      "id": "peerpush",
      "name": "PeerPush",
      "url": "https://peerpush.net",
      "description": "A community-driven startup directory with high domain rating that rewards you for spotlighting the next big thing while showcasing your own growth journey.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 68,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "shipybara",
      "name": "Shipybara",
      "url": "https://shipybara.com",
      "description": "Launch your startup, get seen by early adopters",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 49,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "reddit",
      "name": "Reddit",
      "url": "https://reddit.com",
      "description": "The front page of the internet - diverse communities and discussions.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 95,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "sourceforge",
      "name": "Sourceforge",
      "url": "https://sourceforge.net",
      "description": "Platform for sharing and reviewing open-source and commercial software.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 92,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "techcrunch",
      "name": "TechCrunch",
      "url": "https://techcrunch.com",
      "description": "Leading technology media property, dedicated to obsessively profiling startups.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 92,
      "submissionType": "paid",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "capterra",
      "name": "Capterra",
      "url": "https://www.capterra.com",
      "description": "A site for comparing business software.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 91,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "product-hunt",
      "name": "Product Hunt",
      "url": "https://www.producthunt.com",
      "description": "The premier platform for discovering and launching new products daily.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 91,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "g2",
      "name": "G2",
      "url": "https://www.g2.com",
      "description": "Platform for discovering and comparing software.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 91,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "hacker-news",
      "name": "Hacker News",
      "url": "https://news.ycombinator.com",
      "description": "Y Combinator's community-driven tech news and startup discussion platform.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 91,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "launched-by-lovable",
      "name": "Launched by Lovable",
      "url": "https://launched.lovable.app",
      "description": "Showcase of projects built with Lovable platform.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 87,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "angellist",
      "name": "AngelList",
      "url": "https://angel.co",
      "description": "The world's largest startup community for investors, entrepreneurs, and job seekers.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 87,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startupfame",
      "name": "StartupFA.me",
      "url": "https://startupfa.me",
      "description": "Directory for finding and submitting startup tools and resources.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 82,
      "submissionType": "paid",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "indie-hackers",
      "name": "Indie Hackers",
      "url": "https://indiehackers.com",
      "description": "Community of developers who are sharing the strategies behind their companies.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 80,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "alternativeto",
      "name": "AlternativeTo",
      "url": "https://alternativeto.net",
      "description": "Crowdsourced software recommendations and alternatives.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 79,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "dang-ai",
      "name": "Dang AI",
      "url": "https://dang.ai",
      "description": "Directory of AI tools and artificial intelligence resources.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 79,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "fazier",
      "name": "Fazier",
      "url": "https://fazier.com",
      "description": "Marketplace for SaaS products and startup tools.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 79,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "twelve-tools",
      "name": "Twelve Tools",
      "url": "https://twelve.tools",
      "description": "Curated collection of tools for entrepreneurs and makers.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 79,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "there's-an-ai-for-that",
      "name": "There's An AI For That",
      "url": "https://theresanaiforthat.com",
      "description": "Comprehensive database of AI tools for every use case.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 77,
      "submissionType": "paid",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "turbo0",
      "name": "Turbo0",
      "url": "https://turbo0.com",
      "description": "Fast-track platform for launching products quickly.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 77,
      "submissionType": "paid",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "saashub",
      "name": "SaaSHub",
      "url": "https://www.saashub.com",
      "description": "Software alternatives and reviews platform.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 76,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "toolpilot",
      "name": "Toolpilot",
      "url": "https://www.toolpilot.ai",
      "description": "AI tools discovery and directory",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 76,
      "submissionType": "paid",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "peerlist",
      "name": "Peerlist",
      "url": "https://peerlist.io",
      "description": "Network and portfolio platform for tech professionals.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 75,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "betalist",
      "name": "BetaList",
      "url": "https://betalist.com",
      "description": "Platform for discovering and getting early access to tomorrow's startups.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 74,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "findlytools",
      "name": "findly.tools",
      "url": "https://findly.tools",
      "description": "The best tools, all in one place.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 74,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "uneed",
      "name": "Uneed",
      "url": "https://www.uneed.best",
      "description": "Curated directory of the best tools for entrepreneurs.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 73,
      "submissionType": "paid",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "alternativeme",
      "name": "Alternative.me",
      "url": "https://alternative.me",
      "description": "Find alternatives to popular software and services.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 73,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "softwareworld",
      "name": "SoftwareWorld",
      "url": "https://www.softwareworld.co",
      "description": "Find The Best Software & Services For Your Business",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 73,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "launchigniter",
      "name": "LaunchIgniter",
      "url": "https://launchigniter.com",
      "description": "Launch Platform",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 72,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "magicboxtools",
      "name": "magicbox.tools",
      "url": "https://magicbox.tools",
      "description": "Featuring over 20,000 awesome AI tools",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 72,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "submitaitools",
      "name": "SubmitAiTools",
      "url": "https://submitaitools.org",
      "description": "Simple platform to discover and share AI tools.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 72,
      "submissionType": "paid",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "sideprojectors",
      "name": "SideProjectors",
      "url": "https://www.sideprojectors.com",
      "description": "Community for sharing and discovering side projects.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 70,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "tinylaunch",
      "name": "TinyLaunch",
      "url": "https://www.tinylaunch.com",
      "description": "Product launch platform with visibility",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 69,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "future-tools",
      "name": "Future Tools",
      "url": "https://www.futuretools.io",
      "description": "Directory of AI tools and future technology.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 68,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "aitools",
      "name": "AiTools",
      "url": "https://aitools.inc",
      "description": "Handy directory for finding AI tools",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 67,
      "submissionType": "freemium",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "aiwithme",
      "name": "aiwith.me",
      "url": "https://aiwith.me",
      "description": "Discover the latest and best AI tools",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 66,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startup-stash",
      "name": "Startup Stash",
      "url": "https://startupstash.com",
      "description": "Curated directory of resources and tools for startups.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 65,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "indie-deals",
      "name": "Indie Deals",
      "url": "https://www.indie.deals",
      "description": "Deals and discounts for indie makers and startups.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 60,
      "submissionType": "paid",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "pitchwall",
      "name": "Pitchwall",
      "url": "https://pitchwall.co",
      "description": "Premium startup showcase",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 60,
      "submissionType": "freemium",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "devhunt",
      "name": "DevHunt",
      "url": "https://devhunt.org",
      "description": "Product Hunt for developers - showcase developer tools.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 59,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "super-launch",
      "name": "Super Launch",
      "url": "https://www.superlaun.ch",
      "description": "A product launch platform cum directory.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 57,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "microlaunch",
      "name": "MicroLaunch",
      "url": "https://microlaunch.net",
      "description": "Platform for launching and discovering micro startups.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 57,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "open-launch",
      "name": "Open Launch",
      "url": "https://open-launch.com",
      "description": "Open platform for product launches and feedback.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 57,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "acidtoolscom",
      "name": "acidtools.com",
      "url": "https://acidtools.com",
      "description": "Directory of productivity & AI tools.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 56,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "ideakiln",
      "name": "IdeaKiln",
      "url": "https://ideakiln.com",
      "description": "A community-driven directory for early-stage startup ideas, prototypes, and MVPs.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 56,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "firsto",
      "name": "Firsto",
      "url": "https://firsto.co",
      "description": "Firsto is a product‐launch platform tailored for indie makers, developers, and startups. It offers a fair, visibility‐first environment where every submitted project gains exposure, unlike curated or exclusive platforms with gatekeepers.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 56,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startupfast",
      "name": "startupfa.st",
      "url": "https://www.startupfa.st",
      "description": "Startup directory",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 56,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "agenthunter",
      "name": "AgentHunter",
      "url": "https://www.agenthunter.io",
      "description": "Best AI Agents in One Place",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 55,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startups-lab",
      "name": "Startups Lab",
      "url": "https://startupslab.site",
      "description": "Showcase your startup",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 55,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "scoutforge",
      "name": "Scoutforge",
      "url": "https://scoutforge.net",
      "description": "Discover new apps with unbiased reviews",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 51,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "launching-next",
      "name": "Launching Next",
      "url": "https://www.launchingnext.com",
      "description": "Platform for announcing upcoming product launches.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 51,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "open-alternative",
      "name": "Open Alternative",
      "url": "https://openalternative.co",
      "description": "Open source alternatives to popular software.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 51,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "trustmrr",
      "name": "TrustMRR",
      "url": "https://trustmrr.com",
      "description": "The database of verified startup revenues",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 51,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "tiny-startups",
      "name": "Tiny Startups",
      "url": "https://tinystartups.com",
      "description": "Community for small startups and indie hackers.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 50,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "makerthrive",
      "name": "MakerThrive",
      "url": "https://makerthrive.com",
      "description": "Community and resources for makers and creators.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 50,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "openhunts",
      "name": "Openhunts",
      "url": "https://openhunts.com",
      "description": "Launch and hunt products openly.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 49,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "ai-tech-viral",
      "name": "AI Tech Viral",
      "url": "https://aitechviral.com",
      "description": "AI Tech Viral is a simple directory for sharing AI tools",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 49,
      "submissionType": "free",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "promote-project",
      "name": "Promote Project",
      "url": "https://www.promoteproject.com",
      "description": "Platform for promoting and marketing your projects.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 48,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "saashunt",
      "name": "SaasHunt",
      "url": "https://saashunt.best",
      "description": "Product Hunt Alternative for SaaS products",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 48,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "unite-list",
      "name": "Unite List",
      "url": "https://unitelist.com",
      "description": "Unite List is a straightforward directory where makers and SaaS creators can easily find and add useful digital tools.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 47,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startuptrustedcom",
      "name": "startuptrusted.com",
      "url": "https://Discover trusted startups and submit your own to get discovered.",
      "description": "Visit Site",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 47,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "appalist",
      "name": "AppaList",
      "url": "https://appalist.com",
      "description": "Explore software solutions that take your productivity to the next level",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 46,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "huzzler",
      "name": "Huzzler",
      "url": "https://huzzler.so",
      "description": "Platform for discovering and promoting new startup projects.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 46,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "foundrlist",
      "name": "FoundrList",
      "url": "https://foundrlist.com",
      "description": "SaaS and startup directory",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 46,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "solopush",
      "name": "SoloPush",
      "url": "https://solopush.com",
      "description": "Platform for solo entrepreneurs to promote their projects.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 45,
      "submissionType": "paid",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "we-like-tools",
      "name": "We Like Tools",
      "url": "https://weliketools.com",
      "description": "We Like Tools celebrates the best productivity solutions. Discover tools that we genuinely recommend and love.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 44,
      "submissionType": "freemium",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startuplisting",
      "name": "startuplist.ing",
      "url": "https://startuplist.ing",
      "description": "All-in-one platform for builders",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 41,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "toolfio",
      "name": "Toolfio",
      "url": "https://toolfio.com",
      "description": "The ultimate hub for finding and showcasing SaaS products.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 41,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "micro-saas-examples",
      "name": "Micro SaaS Examples",
      "url": "https://www.microsaasexamples.com",
      "description": "Explore the best micro saas ideas from the internet.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 40,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "awesome-tools",
      "name": "Awesome Tools",
      "url": "https://awesome.tools",
      "description": "Best Awesome Tools for Startups",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 40,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "productburst",
      "name": "ProductBurst",
      "url": "https://productburst.com",
      "description": "Daily featured products and startup showcases.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 39,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "indiehub",
      "name": "IndieHub",
      "url": "https://indiehub.best",
      "description": "All-in-One Directory for Indie Makers",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 39,
      "submissionType": "paid",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "toolfolio",
      "name": "toolfolio",
      "url": "https://toolfolio.io",
      "description": "All the tools & resources you need, in one place.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 38,
      "submissionType": "freemium",
      "followType": "nofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "rankyourai",
      "name": "RankYourAI",
      "url": "https://rankyourai.com",
      "description": "Ranking and review platform for AI tools.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 38,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startupbase",
      "name": "StartupBase",
      "url": "https://startupbase.io",
      "description": "Database and directory of startup companies.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 38,
      "submissionType": "freemium",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "saaspage",
      "name": "Saaspa.ge",
      "url": "https://www.saaspa.ge",
      "description": "Saas Products Directory",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 36,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "shipyard-hq",
      "name": "ShipYard HQ",
      "url": "https://shipyardhq.dev",
      "description": "Shipyard shows what builders are actually clicking on.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 35,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "launch",
      "name": "Launch",
      "url": "https://trylaunch.ai",
      "description": "The best new AI products. Every day.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 35,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "startupsfm",
      "name": "Startups.fm",
      "url": "https://startups.fm",
      "description": "Podcast and community focused on startup stories.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 35,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "best-of-web",
      "name": "Best of Web",
      "url": "https://www.bestofweb.site",
      "description": "All-in-One Growth Platform",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 35,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "proofstories",
      "name": "Proofstories",
      "url": "https://proofstories.io",
      "description": "A collection of tools sharing how they won their first customers.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 34,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "tinylaunchpad",
      "name": "TinyLaunchpad",
      "url": "https://tinylaunchpad.com",
      "description": "Fresh products and startups launched every Monday.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 33,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "freemium",
      "name": "Freemium",
      "url": "https://neeed.directory",
      "description": "neeed.directory",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 33,
      "submissionType": "unknown",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "euroalternative",
      "name": "EuroAlternative",
      "url": "https://euroalternative.co",
      "description": "Discover European Alternatives to Big Tech Companies",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 32,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "confettisaas",
      "name": "ConfettiSaaS",
      "url": "https://confettisaas.com",
      "description": "ConfettiSaaS.com is a platform for showcasing and discovering confetti-powered apps.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 32,
      "submissionType": "unknown",
      "followType": "unknown",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
    {
      "id": "resourcefyi",
      "name": "Resource.fyi",
      "url": "https://resource.fyi",
      "description": "Collection of useful resources for entrepreneurs.",
      "type": [
        "Launch Platform",
        "SaaS Directory"
      ],
      "domainRating": 30,
      "submissionType": "free",
      "followType": "dofollow",
      "listedOn": [
        "launchdirectories.com"
      ],
      "notes": "Added from launchdirectories.com"
    },
]

# Load existing directories
with open('../public/data/directories.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    existing_dirs = data['directories']

# Create a normalized URL map for existing directories
url_map = {}
for dir_entry in existing_dirs:
    normalized = normalize_url(dir_entry['url'])
    if normalized not in url_map:
        url_map[normalized] = dir_entry

# Track results
merged = 0
added = 0
matches = []

# Process new directories
for new_dir in new_dirs:
    new_normalized = normalize_url(new_dir['url'])
    
    if new_normalized in url_map:
        # Found a match - add source to existing entry
        existing_entry = url_map[new_normalized]
        if 'launchdirectories.com' not in existing_entry['listedOn']:
            existing_entry['listedOn'].append('launchdirectories.com')
        merged += 1
        matches.append({
            'new': new_dir['name'],
            'existing': existing_entry['name'],
            'url': new_dir['url']
        })
    else:
        # New entry - add it
        existing_dirs.append(new_dir)
        added += 1

# Write updated directories back
with open('../public/data/directories.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nMerge Summary:")
print(f"Total launchdirectories.com entries: {len(new_dirs)}")
print(f"Merged (added source to existing): {merged}")
print(f"Added (new directories): {added}")
print(f"\nMatches found ({len(matches)}):")
for match in matches:
    print(f"  - {match['new']} → {match['existing']}")
