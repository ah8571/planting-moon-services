#!/usr/bin/env python3
"""
Merge guest post sources from multiple blogging aggregator sites.
Checks for duplicates and adds new guest post opportunities to guest-posts.json
"""

import json

# Guest post data from bloggerspassion.com (comprehensive list)
bloggerspassion_data = [
    # SEO Oriented
    {"name": "TechWyse", "url": "https://www.techwyse.com/blog", "dr": 71, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"], "source": "bloggerspassion.com"},
    {"name": "MarketingTechNews", "url": "https://www.marketingtechnews.net", "dr": 76, "niche": ["SaaS", "Marketing", "Technology", "Digital Marketing"], "source": "bloggerspassion.com"},
    {"name": "RankWatch Blog", "url": "https://www.rankwatch.com/blog", "dr": 73, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"], "source": "bloggerspassion.com"},
    {"name": "Serpstat Blog", "url": "https://serpstat.com/blog", "dr": 79, "niche": ["SaaS", "SEO", "Marketing", "Content Marketing"], "source": "bloggerspassion.com"},
    {"name": "Jeffbullas's Blog", "url": "https://www.jeffbullas.com", "dr": 80, "niche": ["SaaS", "Marketing", "Social Media", "Content Marketing"], "source": "bloggerspassion.com"},
    {"name": "Search Engine Watch", "url": "https://www.searchenginewatch.com", "dr": 86, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"], "source": "bloggerspassion.com"},
    {"name": "Search Engine Land", "url": "https://searchengineland.com", "dr": 91, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"], "source": "bloggerspassion.com"},
    {"name": "Search Engine Roundtable", "url": "https://www.seroundtable.com", "dr": 84, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"], "source": "bloggerspassion.com"},
    {"name": "Main Street Host", "url": "https://www.mainstreethost.com", "dr": 65, "niche": ["SaaS", "Web Development", "Hosting"], "source": "bloggerspassion.com"},
    {"name": "EZ Rankings", "url": "https://www.ezrankings.com", "dr": 64, "niche": ["SaaS", "SEO", "Digital Marketing"], "source": "bloggerspassion.com"},
    
    # Blogging
    {"name": "Content Marketing Institute", "url": "https://contentmarketinginstitute.com", "dr": 89, "niche": ["SaaS", "Content Marketing", "Marketing"], "source": "bloggerspassion.com"},
    {"name": "The Blog Herald", "url": "https://www.theblogherald.com", "dr": 69, "niche": ["SaaS", "Content", "Blogging"], "source": "bloggerspassion.com"},
    {"name": "Webnus", "url": "https://webnus.net", "dr": 81, "niche": ["SaaS", "Web Development", "WordPress"], "source": "bloggerspassion.com"},
    {"name": "CyberChimps", "url": "https://www.cyberchimps.com", "dr": 91, "niche": ["SaaS", "Web Development", "Design"], "source": "bloggerspassion.com"},
    {"name": "WebScoot Blog", "url": "https://www.webscoot.io", "dr": 43, "niche": ["SaaS", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "MakeWebBetter", "url": "https://makewebbetter.com", "dr": 73, "niche": ["SaaS", "Web Development", "WordPress"], "source": "bloggerspassion.com"},
    
    # Marketing/More
    {"name": "WebEngage", "url": "https://www.webengage.com/blog", "dr": 72, "niche": ["SaaS", "Marketing", "Automation", "Customer Engagement"], "source": "bloggerspassion.com"},
    {"name": "NetHunt", "url": "https://nethunt.com/blog", "dr": 73, "niche": ["SaaS", "CRM", "Sales", "Automation"], "source": "bloggerspassion.com"},
    {"name": "Cloudways", "url": "https://cloudways.com/blog", "dr": 91, "niche": ["SaaS", "Web Development", "Hosting"], "source": "bloggerspassion.com"},
    {"name": "Chatter Buzz", "url": "https://www.chatterbuzz.com", "dr": 62, "niche": ["SaaS", "Marketing", "Social Media"], "source": "bloggerspassion.com"},
    {"name": "Make a Living Writing", "url": "https://makealivinwriting.com", "dr": 70, "niche": ["SaaS", "Content Marketing", "Writing"], "source": "bloggerspassion.com"},
    {"name": "ResellerClub Blog", "url": "https://www.resellerclub.com/blog", "dr": 78, "niche": ["SaaS", "Business Tools", "Reseller"], "source": "bloggerspassion.com"},
    
    # Business
    {"name": "AllBusiness.com", "url": "https://www.allbusiness.com", "dr": 80, "niche": ["SaaS", "Business", "Entrepreneurship"], "source": "bloggerspassion.com"},
    {"name": "Inc.com", "url": "https://www.inc.com", "dr": 92, "niche": ["SaaS", "Business", "Entrepreneurship"], "source": "bloggerspassion.com"},
    {"name": "Success.com", "url": "https://www.success.com", "dr": 81, "niche": ["SaaS", "Business", "Entrepreneurship"], "source": "bloggerspassion.com"},
    {"name": "Bplans.com", "url": "https://www.bplans.com", "dr": 80, "niche": ["SaaS", "Business", "Planning"], "source": "bloggerspassion.com"},
    {"name": "MyCorporation.com", "url": "https://www.mycorporation.com", "dr": 74, "niche": ["SaaS", "Business", "Legal"], "source": "bloggerspassion.com"},
    {"name": "Successful-Blog.com", "url": "https://successful-blog.com", "dr": 54, "niche": ["SaaS", "Business", "Content"], "source": "bloggerspassion.com"},
    {"name": "Sogolytics", "url": "https://www.sogolytics.com", "dr": 71, "niche": ["SaaS", "Analytics", "Business"], "source": "bloggerspassion.com"},
    {"name": "The Ken", "url": "https://the-ken.com", "dr": 67, "niche": ["SaaS", "Business", "India"], "source": "bloggerspassion.com"},
    {"name": "Business Insider India", "url": "https://www.businessinsider.in", "dr": 84, "niche": ["SaaS", "Business", "India"], "source": "bloggerspassion.com"},
    {"name": "Exabytes", "url": "https://www.exabytes.com", "dr": 83, "niche": ["SaaS", "Web Development", "Hosting"], "source": "bloggerspassion.com"},
    {"name": "Convert.com", "url": "https://convert.com", "dr": 77, "niche": ["SaaS", "Conversion Optimization", "Marketing"], "source": "bloggerspassion.com"},
    {"name": "Gimmio Blog", "url": "https://gimmio.com", "dr": 66, "niche": ["SaaS", "Marketing", "Business"], "source": "bloggerspassion.com"},
    
    # Technology
    {"name": "SitePoint", "url": "https://www.sitepoint.com", "dr": 87, "niche": ["SaaS", "Development", "Web Development", "Technology"], "source": "bloggerspassion.com"},
    {"name": "Read Write", "url": "https://readwrite.com", "dr": 84, "niche": ["SaaS", "Technology", "Entrepreneurship", "Innovation"], "source": "bloggerspassion.com"},
    {"name": "PragProg", "url": "https://pragprog.com", "dr": 80, "niche": ["SaaS", "Development", "Technology", "Programming"], "source": "bloggerspassion.com"},
    {"name": "iTechCode", "url": "https://itechcode.com", "dr": 30, "niche": ["SaaS", "Technology", "Development"], "source": "bloggerspassion.com"},
    {"name": "VentureBeat", "url": "https://venturebeat.com", "dr": 91, "niche": ["SaaS", "Technology", "Entrepreneurship", "Innovation"], "source": "bloggerspassion.com"},
    {"name": "MakingDifferent", "url": "https://makingdifferent.com", "dr": 54, "niche": ["SaaS", "Technology", "Startups"], "source": "bloggerspassion.com"},
    {"name": "TechLila", "url": "https://techlila.com", "dr": 47, "niche": ["SaaS", "Technology"], "source": "bloggerspassion.com"},
    {"name": "Colocation America", "url": "https://colocationamerica.com", "dr": 66, "niche": ["SaaS", "Technology", "Hosting"], "source": "bloggerspassion.com"},
    {"name": "All Tech Buzz", "url": "https://alltechbuzz.net", "dr": 63, "niche": ["SaaS", "Technology"], "source": "bloggerspassion.com"},
    {"name": "Creately.com", "url": "https://creately.com", "dr": 77, "niche": ["SaaS", "Design", "Diagramming"], "source": "bloggerspassion.com"},
    {"name": "Analytics India Magazine", "url": "https://analyticsindiamag.com", "dr": 79, "niche": ["SaaS", "Technology", "Analytics", "AI"], "source": "bloggerspassion.com"},
    {"name": "SoftwareWorld", "url": "https://www.softwareworld.net", "dr": 74, "niche": ["SaaS", "Technology", "Software Reviews"], "source": "bloggerspassion.com"},
    {"name": "ProProfs", "url": "https://www.proprofs.com/blog", "dr": 80, "niche": ["SaaS", "Productivity", "Training", "Business Tools"], "source": "bloggerspassion.com"},
    {"name": "Neptune Blog", "url": "https://neptune.io", "dr": 72, "niche": ["SaaS", "Technology", "Development"], "source": "bloggerspassion.com"},
    {"name": "iMocha", "url": "https://www.imocha.io", "dr": 57, "niche": ["SaaS", "Business Tools", "Assessment"], "source": "bloggerspassion.com"},
    {"name": "Freshdesk", "url": "https://freshdesk.com/blog", "dr": 90, "niche": ["SaaS", "Customer Support", "CRM", "Business Tools"], "source": "bloggerspassion.com"},
    {"name": "Analytics Insight", "url": "https://www.analyticsinsight.net", "dr": 81, "niche": ["SaaS", "Technology", "Analytics", "AI"], "source": "bloggerspassion.com"},
    {"name": "Mobisoft Infotech", "url": "https://www.mobisoftinfotech.com", "dr": 64, "niche": ["SaaS", "Development", "Mobile"], "source": "bloggerspassion.com"},
    {"name": "Complete Connection", "url": "https://completeconnection.com", "dr": 51, "niche": ["SaaS", "Technology"], "source": "bloggerspassion.com"},
    {"name": "Technology Networks", "url": "https://www.technologynetworks.com", "dr": 78, "niche": ["SaaS", "Technology", "Innovation"], "source": "bloggerspassion.com"},
    {"name": "Chanty", "url": "https://chanty.com/blog", "dr": 77, "niche": ["SaaS", "Productivity", "Remote Work", "Collaboration"], "source": "bloggerspassion.com"},
    {"name": "Jungleworks", "url": "https://jungleworks.com", "dr": 72, "niche": ["SaaS", "Technology", "Business"], "source": "bloggerspassion.com"},
    {"name": "PAT RESEARCH", "url": "https://www.patresearch.com", "dr": 70, "niche": ["SaaS", "Technology"], "source": "bloggerspassion.com"},
    {"name": "TechSupremo", "url": "https://techsupremo.com", "dr": 45, "niche": ["SaaS", "Technology"], "source": "bloggerspassion.com"},
    {"name": "The Next Tech", "url": "https://thenexttech.com", "dr": 59, "niche": ["SaaS", "Technology"], "source": "bloggerspassion.com"},
    
    # Digital Marketing
    {"name": "OnCrawl", "url": "https://www.oncrawl.com/blog", "dr": 74, "niche": ["SaaS", "SEO", "Marketing", "Analytics"], "source": "bloggerspassion.com"},
    {"name": "ContactPigeon", "url": "https://www.contactpigeon.com/blog", "dr": 71, "niche": ["SaaS", "Marketing", "Email Marketing"], "source": "bloggerspassion.com"},
    {"name": "ClickZ", "url": "https://www.clickz.com", "dr": 83, "niche": ["SaaS", "Marketing", "Digital Marketing"], "source": "bloggerspassion.com"},
    {"name": "Mediapost", "url": "https://www.mediapost.com", "dr": 88, "niche": ["SaaS", "Marketing", "Advertising", "Digital Marketing"], "source": "bloggerspassion.com"},
    
    # Web Development
    {"name": "Smashing Magazine", "url": "https://www.smashingmagazine.com", "dr": 90, "niche": ["SaaS", "Development", "Design", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "Hongkiat", "url": "https://www.hongkiat.com", "dr": 81, "niche": ["SaaS", "Development", "Design", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "Colossal", "url": "https://www.colossalmedia.com", "dr": 80, "niche": ["SaaS", "Design", "Inspiration"], "source": "bloggerspassion.com"},
    {"name": "Web Design Ledger", "url": "https://webdesignledger.com", "dr": 77, "niche": ["SaaS", "Design", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "Fatbit", "url": "https://www.fatbit.com", "dr": 71, "niche": ["SaaS", "Web Development", "Design"], "source": "bloggerspassion.com"},
    {"name": "Quertime", "url": "https://www.quertime.com", "dr": 43, "niche": ["SaaS", "Web Development", "Tutorials"], "source": "bloggerspassion.com"},
    {"name": "A List Apart", "url": "https://alistapart.com", "dr": 86, "niche": ["SaaS", "Development", "Web Development", "Design"], "source": "bloggerspassion.com"},
    {"name": "Creative Blog (CB)", "url": "https://www.creativebloq.com", "dr": 86, "niche": ["SaaS", "Design", "Inspiration"], "source": "bloggerspassion.com"},
    {"name": "CrazyLeafDesign", "url": "https://www.crazyleafdesign.com", "dr": 56, "niche": ["SaaS", "Design", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "Writer's Relief", "url": "https://writersrelief.com", "dr": 52, "niche": ["SaaS", "Content", "Writing"], "source": "bloggerspassion.com"},
    {"name": "Top Design Magazine", "url": "https://www.topdesignmag.com", "dr": 59, "niche": ["SaaS", "Design"], "source": "bloggerspassion.com"},
    {"name": "Creative Nerds", "url": "https://creativeNerds.co.uk", "dr": 63, "niche": ["SaaS", "Design", "Development"], "source": "bloggerspassion.com"},
    {"name": "webdew", "url": "https://webdew.io", "dr": 72, "niche": ["SaaS", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "Stackify", "url": "https://stackify.com/blog", "dr": 75, "niche": ["SaaS", "Development", "Technology", "DevOps"], "source": "bloggerspassion.com"},
    {"name": "WebAlive", "url": "https://www.webalive.com.au", "dr": 74, "niche": ["SaaS", "Development", "Web Development", "Marketing"], "source": "bloggerspassion.com"},
    {"name": "Speckyboy", "url": "https://speckyboy.com", "dr": 79, "niche": ["SaaS", "Design", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "InstantShift", "url": "https://www.instantshift.com", "dr": 71, "niche": ["SaaS", "Web Development", "Design"], "source": "bloggerspassion.com"},
    {"name": "Netguru Blog", "url": "https://www.netguru.com/blog", "dr": 76, "niche": ["SaaS", "Development", "Technology", "Software"], "source": "bloggerspassion.com"},
    
    # Finance
    {"name": "Bigger Pockets", "url": "https://www.biggerpockets.com", "dr": 81, "niche": ["SaaS", "Finance", "Real Estate", "Investment"], "source": "bloggerspassion.com"},
    {"name": "Investing.com", "url": "https://www.investing.com", "dr": 88, "niche": ["SaaS", "Finance", "Investment"], "source": "bloggerspassion.com"},
    {"name": "FinancesOnline.com", "url": "https://financesonline.com", "dr": 87, "niche": ["SaaS", "Finance", "Business Tools"], "source": "bloggerspassion.com"},
    {"name": "Wise Bread", "url": "https://www.wisebread.com", "dr": 76, "niche": ["SaaS", "Finance", "Money Management"], "source": "bloggerspassion.com"},
    {"name": "Money Saving Mom", "url": "https://moneysavingmom.com", "dr": 72, "niche": ["SaaS", "Finance", "Money Management"], "source": "bloggerspassion.com"},
    {"name": "Modest Money", "url": "https://www.modestmoney.com", "dr": 71, "niche": ["SaaS", "Finance", "Investment"], "source": "bloggerspassion.com"},
    {"name": "Geek Estate Blog", "url": "https://geepestate.com", "dr": 57, "niche": ["SaaS", "Finance", "Real Estate"], "source": "bloggerspassion.com"},
    {"name": "OilPrice.com", "url": "https://oilprice.com", "dr": 80, "niche": ["SaaS", "Finance", "Energy"], "source": "bloggerspassion.com"},
    {"name": "MoneyMiniBlog", "url": "https://moneyminiblog.com", "dr": 53, "niche": ["SaaS", "Finance", "Money"], "source": "bloggerspassion.com"},
    
    # Education
    {"name": "ASCD.org", "url": "https://www.ascd.org", "dr": 81, "niche": ["SaaS", "Education", "Learning"], "source": "bloggerspassion.com"},
    {"name": "SimpleK12", "url": "https://www.simplek12.com", "dr": 56, "niche": ["SaaS", "Education", "K-12"], "source": "bloggerspassion.com"},
    {"name": "Infed.org", "url": "https://infed.org", "dr": 73, "niche": ["SaaS", "Education", "Learning"], "source": "bloggerspassion.com"},
    {"name": "The PIE News", "url": "https://www.thepienews.com", "dr": 73, "niche": ["SaaS", "Education", "International"], "source": "bloggerspassion.com"},
    {"name": "eLearn Magazine", "url": "https://elearnmag.org", "dr": 91, "niche": ["SaaS", "Education", "E-Learning"], "source": "bloggerspassion.com"},
    {"name": "Edutopia", "url": "https://www.edutopia.org", "dr": 84, "niche": ["SaaS", "Education", "K-12"], "source": "bloggerspassion.com"},
    {"name": "Getting Smart", "url": "https://www.gettingsmart.com", "dr": 75, "niche": ["SaaS", "Education", "Innovation"], "source": "bloggerspassion.com"},
    {"name": "EduGorilla", "url": "https://www.edugorilla.com", "dr": 74, "niche": ["SaaS", "Education", "Test Prep"], "source": "bloggerspassion.com"},
    {"name": "KnowledgeHut", "url": "https://www.knowledgehut.com", "dr": 74, "niche": ["SaaS", "Education", "Training"], "source": "bloggerspassion.com"},
    {"name": "The Greater Good Science Center", "url": "https://greatergood.berkeley.edu", "dr": 91, "niche": ["SaaS", "Education", "Science"], "source": "bloggerspassion.com"},
    {"name": "TutorialsTeacher", "url": "https://www.tutorialsteacher.com", "dr": 61, "niche": ["SaaS", "Education", "Programming"], "source": "bloggerspassion.com"},
    {"name": "Everyday Power", "url": "https://everydaypower.com", "dr": 74, "niche": ["SaaS", "Education", "Motivation"], "source": "bloggerspassion.com"},
    {"name": "TopUniversities.com", "url": "https://www.topuniversities.com", "dr": 84, "niche": ["SaaS", "Education", "Higher Ed"], "source": "bloggerspassion.com"},
    {"name": "Eduonix", "url": "https://www.eduonix.com", "dr": 69, "niche": ["SaaS", "Education", "Online Courses"], "source": "bloggerspassion.com"},
    {"name": "InformIT", "url": "https://www.informit.com", "dr": 80, "niche": ["SaaS", "Education", "Technology"], "source": "bloggerspassion.com"},
    {"name": "Manning.com", "url": "https://manning.com", "dr": 82, "niche": ["SaaS", "Education", "Programming"], "source": "bloggerspassion.com"},
    {"name": "ASU LodestarCenter", "url": "https://lodestar.asu.edu", "dr": 90, "niche": ["SaaS", "Education", "Leadership"], "source": "bloggerspassion.com"},
    {"name": "MindMajix", "url": "https://mindmajix.com", "dr": 66, "niche": ["SaaS", "Education", "Training"], "source": "bloggerspassion.com"},
    
    # Money Online
    {"name": "IncomeDiary.com", "url": "https://incomediary.com", "dr": 70, "niche": ["SaaS", "Finance", "Side Hustle"], "source": "bloggerspassion.com"},
    {"name": "LeavingWorkBehind.com", "url": "https://leavingworkbehind.com", "dr": 68, "niche": ["SaaS", "Entrepreneurship", "Finance"], "source": "bloggerspassion.com"},
    
    # Entrepreneurship
    {"name": "Entrepreneur.com", "url": "https://www.entrepreneur.com", "dr": 91, "niche": ["SaaS", "Entrepreneurship", "Business"], "source": "bloggerspassion.com"},
    {"name": "Inc42.com", "url": "https://inc42.com", "dr": 80, "niche": ["SaaS", "Entrepreneurship", "Startups", "India"], "source": "bloggerspassion.com"},
    {"name": "Addicted2Success", "url": "https://www.addicted2success.com", "dr": 73, "niche": ["SaaS", "Entrepreneurship", "Motivation"], "source": "bloggerspassion.com"},
    {"name": "StartupNation", "url": "https://www.startupnation.com", "dr": 75, "niche": ["SaaS", "Entrepreneurship", "Startups"], "source": "bloggerspassion.com"},
    {"name": "KillerStartups.com", "url": "https://killerstartups.com", "dr": 74, "niche": ["SaaS", "Entrepreneurship", "Startups"], "source": "bloggerspassion.com"},
    {"name": "YFS Magazine", "url": "https://www.yfsmagazine.com", "dr": 70, "niche": ["SaaS", "Entrepreneurship", "Business"], "source": "bloggerspassion.com"},
    {"name": "StartupBros Blog", "url": "https://www.startupbros.com", "dr": 63, "niche": ["SaaS", "Entrepreneurship", "Startups"], "source": "bloggerspassion.com"},
    {"name": "SmallBizClub", "url": "https://www.smallbizclub.com", "dr": 66, "niche": ["SaaS", "Business", "Entrepreneurship"], "source": "bloggerspassion.com"},
    {"name": "Harvard Business Review", "url": "https://hbr.org", "dr": 92, "niche": ["SaaS", "Business", "Leadership"], "source": "bloggerspassion.com"},
    {"name": "MyVenturePad", "url": "https://myventurepad.com", "dr": 52, "niche": ["SaaS", "Entrepreneurship", "Startups"], "source": "bloggerspassion.com"},
    
    # Real Estate
    {"name": "International Living Magazine", "url": "https://internationalliving.com", "dr": 75, "niche": ["SaaS", "Real Estate", "Lifestyle"], "source": "bloggerspassion.com"},
    {"name": "EscapeArtist", "url": "https://www.escapeartist.com", "dr": 62, "niche": ["SaaS", "Real Estate", "Expat"], "source": "bloggerspassion.com"},
    {"name": "GeekEstate Blog", "url": "https://geepestate.com", "dr": 57, "niche": ["SaaS", "Real Estate", "Finance"], "source": "bloggerspassion.com"},
    
    # New Sites (Major publications)
    {"name": "Forbes.com", "url": "https://www.forbes.com", "dr": 94, "niche": ["SaaS", "Business", "Leadership"], "source": "bloggerspassion.com"},
    {"name": "TheGuardian.com", "url": "https://www.theguardian.com", "dr": 93, "niche": ["SaaS", "News", "Opinion"], "source": "bloggerspassion.com"},
    {"name": "Wall Street Journal", "url": "https://www.wsj.com", "dr": 92, "niche": ["SaaS", "Finance", "News"], "source": "bloggerspassion.com"},
    {"name": "Fast Company", "url": "https://www.fastcompany.com", "dr": 91, "niche": ["SaaS", "Business", "Innovation"], "source": "bloggerspassion.com"},
    {"name": "HuffPost.com", "url": "https://www.huffpost.com", "dr": 93, "niche": ["SaaS", "News", "Opinion"], "source": "bloggerspassion.com"},
    {"name": "The Diplomat", "url": "https://thediplomat.com", "dr": 82, "niche": ["SaaS", "News", "International"], "source": "bloggerspassion.com"},
    {"name": "ORF", "url": "https://www.orf.at", "dr": 76, "niche": ["SaaS", "News", "Austria"], "source": "bloggerspassion.com"},
    {"name": "Times of India", "url": "https://timesofindia.indiatimes.com", "dr": 92, "niche": ["SaaS", "News", "India"], "source": "bloggerspassion.com"},
    {"name": "Asia Times", "url": "https://www.atimes.com", "dr": 78, "niche": ["SaaS", "News", "Asia"], "source": "bloggerspassion.com"},
    {"name": "Swarajya", "url": "https://swarajyamag.com", "dr": 73, "niche": ["SaaS", "News", "India"], "source": "bloggerspassion.com"},
    {"name": "GIJN", "url": "https://gijn.org", "dr": 72, "niche": ["SaaS", "News", "Journalism"], "source": "bloggerspassion.com"},
    {"name": "The Conversation", "url": "https://theconversation.com", "dr": 91, "niche": ["SaaS", "Opinion", "Academic"], "source": "bloggerspassion.com"},
    
    # Law
    {"name": "Above the Law", "url": "https://abovethelaw.com", "dr": 79, "niche": ["SaaS", "Law", "Legal"], "source": "bloggerspassion.com"},
    {"name": "Attorney at Work", "url": "https://www.attorneyatwork.com", "dr": 71, "niche": ["SaaS", "Law", "Legal"], "source": "bloggerspassion.com"},
    {"name": "LawFuel", "url": "https://www.lawfuel.com", "dr": 58, "niche": ["SaaS", "Law", "Legal"], "source": "bloggerspassion.com"},
    
    # Social/Community Platforms
    {"name": "reddit.com", "url": "https://reddit.com", "dr": 100, "niche": ["SaaS", "Community", "Social"], "source": "bloggerspassion.com"},
    {"name": "Github.com", "url": "https://github.com", "dr": 96, "niche": ["SaaS", "Development", "Community"], "source": "bloggerspassion.com"},
    {"name": "tumblr.com", "url": "https://www.tumblr.com", "dr": 94, "niche": ["SaaS", "Content Platform", "Social"], "source": "bloggerspassion.com"},
    {"name": "substack.com", "url": "https://substack.com", "dr": 79, "niche": ["SaaS", "Content Platform", "Newsletter"], "source": "bloggerspassion.com"},
    {"name": "outbrain.com", "url": "https://www.outbrain.com", "dr": 53, "niche": ["SaaS", "Marketing", "Content Discovery"], "source": "bloggerspassion.com"},
    {"name": "wix.com", "url": "https://www.wix.com", "dr": 83, "niche": ["SaaS", "Web Development", "Site Builder"], "source": "bloggerspassion.com"},
    {"name": "blogger.com", "url": "https://www.blogger.com", "dr": 95, "niche": ["SaaS", "Content Platform", "Blogging"], "source": "bloggerspassion.com"},
    {"name": "flickr.com", "url": "https://www.flickr.com", "dr": 85, "niche": ["SaaS", "Content Platform", "Photo"], "source": "bloggerspassion.com"},
    {"name": "wikidot.com", "url": "https://www.wikidot.com", "dr": 75, "niche": ["SaaS", "Content Platform", "Wiki"], "source": "bloggerspassion.com"},
    {"name": "hubpages.com", "url": "https://hubpages.com", "dr": 65, "niche": ["SaaS", "Content Platform", "Publishing"], "source": "bloggerspassion.com"},
    {"name": "yourstory.com", "url": "https://yourstory.com", "dr": 64, "niche": ["SaaS", "Community", "Startups", "India"], "source": "bloggerspassion.com"},
    {"name": "about.me", "url": "https://about.me", "dr": 57, "niche": ["SaaS", "Content Platform", "Personal"], "source": "bloggerspassion.com"},
    {"name": "webnode.com", "url": "https://www.webnode.com", "dr": 51, "niche": ["SaaS", "Site Builder", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "strikingly.com", "url": "https://www.strikingly.com", "dr": 51, "niche": ["SaaS", "Site Builder", "Web Development"], "source": "bloggerspassion.com"},
    {"name": "hackernoon.com", "url": "https://hackernoon.com", "dr": 52, "niche": ["SaaS", "Technology", "Development", "Community"], "source": "bloggerspassion.com"},
    {"name": "opensource.com", "url": "https://opensource.com", "dr": 56, "niche": ["SaaS", "Technology", "Open Source"], "source": "bloggerspassion.com"},
    {"name": "joomla.org", "url": "https://www.joomla.org", "dr": 54, "niche": ["SaaS", "Development", "CMS"], "source": "bloggerspassion.com"},
    {"name": "fark.com", "url": "https://www.fark.com", "dr": 46, "niche": ["SaaS", "Community", "News"], "source": "bloggerspassion.com"},
    {"name": "indiehackers.com", "url": "https://www.indiehackers.com", "dr": 43, "niche": ["SaaS", "Community", "Entrepreneurship", "Startups"], "source": "bloggerspassion.com"},
    {"name": "scoop.it", "url": "https://www.scoop.it", "dr": 43, "niche": ["SaaS", "Content Curation", "Marketing"], "source": "bloggerspassion.com"},
    {"name": "blogadda.com", "url": "https://www.blogadda.com", "dr": 33, "niche": ["SaaS", "Community", "India"], "source": "bloggerspassion.com"},
    {"name": "wakelet.com", "url": "https://wakelet.com", "dr": 42, "niche": ["SaaS", "Content Curation"], "source": "bloggerspassion.com"},
    {"name": "indibloghub.com", "url": "https://www.indibloghub.com", "dr": 50, "niche": ["SaaS", "Community", "India"], "source": "bloggerspassion.com"},
    {"name": "diigo.com", "url": "https://www.diigo.com", "dr": 86, "niche": ["SaaS", "Productivity", "Bookmarking"], "source": "bloggerspassion.com"},
    {"name": "bloglovin.com", "url": "https://www.bloglovin.com", "dr": 31, "niche": ["SaaS", "Community", "Blogging"], "source": "bloggerspassion.com"},
    {"name": "blogengage.com", "url": "https://www.blogengage.com", "dr": 57, "niche": ["SaaS", "Community", "Blogging"], "source": "bloggerspassion.com"},
    {"name": "blogarama.com", "url": "https://www.blogarama.com", "dr": 32, "niche": ["SaaS", "Directory", "Blogging"], "source": "bloggerspassion.com"},
]

def load_guest_posts():
    """Load existing guest posts from JSON file"""
    try:
        with open('data/guest-posts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"guestPosts": [], "niches": []}

def get_existing_names(guest_posts):
    """Get set of existing publication names for duplicate checking"""
    return {site['name'].lower() for site in guest_posts}

def merge_sources():
    """Merge bloggerspassion data with existing guest-posts"""
    data = load_guest_posts()
    existing_names = get_existing_names(data['guestPosts'])
    
    added_count = 0
    duplicates = []
    sources_updated = 0
    
    for site in bloggerspassion_data:
        if site['name'].lower() not in existing_names:
            # Create entry with all fields
            entry = {
                "id": site['name'].lower().replace(' ', '-').replace('.', ''),
                "name": site['name'],
                "url": site['url'],
                "dr": site['dr'],
                "description": f"Guest post opportunity from {site['source']}.",
                "niche": site['niche'],
                "submissionType": "free",
                "listedOn": [site['source']],
                "notes": ""
            }
            data['guestPosts'].append(entry)
            added_count += 1
        else:
            # Site already exists - add this source to listedOn if not already there
            duplicates.append(site['name'])
            for entry in data['guestPosts']:
                if entry['name'].lower() == site['name'].lower():
                    if site['source'] not in entry['listedOn']:
                        entry['listedOn'].append(site['source'])
                        sources_updated += 1
                    break
    
    # Update niches array with all unique niches found
    all_niches = set(data['niches'])
    for site in data['guestPosts']:
        all_niches.update(site['niche'])
    data['niches'] = sorted(list(all_niches))
    
    # Save updated data
    with open('data/guest-posts.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Merge Complete!")
    print(f"  Added: {added_count} new sites")
    print(f"  Duplicates found: {len(duplicates)}")
    print(f"  Additional sources added: {sources_updated}")
    if duplicates:
        print(f"  Duplicate sites: {', '.join(duplicates)}")
    print(f"  Total guest posts: {len(data['guestPosts'])}")
    print(f"  Total niches: {len(data['niches'])}")

if __name__ == "__main__":
    merge_sources()
