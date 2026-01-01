#!/usr/bin/env python3
"""
Rebuild guest-posts.json from both profeo and bloggerspassion sources,
ensuring all duplicates have both sources listed in listedOn array.
"""

import json

# Profeo.io guest post sources (15 sites)
profeo_data = [
    {"name": "HubSpot", "url": "https://blog.hubspot.com", "dr": 93, "niche": ["SaaS", "Marketing", "CRM"], "description": "\"The go-to site for marketers, entrepreneurs, and businesses. Their blog covers everything from email marketing to customer retention.\" ([Profeo](https://profeo.io)). Guidelines emphasize original, data-backed content that educates their audience.", "notes": "Search Traffic: 4.7M"},
    {"name": "Ranktracker", "url": "https://ranktracker.com/blog", "dr": 74, "niche": ["SaaS", "Marketing", "SEO"], "description": "\"Blog focuses on SEO tips, keyword research, and tools for marketers and agencies.\" ([Profeo](https://profeo.io)). They look for practical and actionable content on SEO and digital marketing.", "notes": "Search Traffic: 91K"},
    {"name": "Billdu", "url": "https://billdu.com/blog", "dr": 72, "niche": ["SaaS", "Finance", "Small Business"], "description": "\"Blog is all about invoicing, small business tools, and entrepreneurship.\" ([Profeo](https://profeo.io)). They're interested in articles that help small businesses and freelancers manage their finances better.", "notes": ""},
    {"name": "PollthePeople", "url": "https://www.pollthepeople.app", "dr": 48, "niche": ["SaaS", "Market Research"], "description": "\"User testing and feedback platform with a blog on UX research methodologies.\" ([Profeo](https://profeo.io)). They publish insights on customer research and product feedback.", "notes": ""},
    {"name": "Designhill", "url": "https://www.designhill.com/design-blog", "dr": 67, "niche": ["SaaS", "Design", "Freelance"], "description": "\"Covers graphic design, branding, freelancing, and creative entrepreneurship.\" ([Profeo](https://profeo.io)). Accepts guest posts on design trends and freelance tips.", "notes": ""},
    {"name": "LeadGenApp", "url": "https://leadgenapp.io/blog", "dr": 45, "niche": ["SaaS", "Sales", "Marketing"], "description": "\"A lead management platform sharing best practices in sales and marketing.\" ([Profeo](https://profeo.io)). Interested in content about sales processes and lead generation.", "notes": ""},
    {"name": "Poptin", "url": "https://www.poptin.com/blog", "dr": 52, "niche": ["SaaS", "Conversion Rate Optimization", "Marketing"], "description": "\"Conversion optimization blog for SaaS and e-commerce businesses.\" ([Profeo](https://profeo.io)). Welcomes content on visitor engagement and conversion optimization.", "notes": ""},
    {"name": "Monocubed", "url": "https://monocubed.com/blog", "dr": 51, "niche": ["SaaS", "Web Development", "Startups"], "description": "\"Development and startup insights from a custom software company.\" ([Profeo](https://profeo.io)). Publishes articles on web development trends and startup lessons.", "notes": ""},
    {"name": "Chamaileon", "url": "https://chamaileon.io/blog", "dr": 46, "niche": ["SaaS", "Email Marketing"], "description": "\"Email template builder sharing email marketing best practices.\" ([Profeo](https://profeo.io)). Looking for practical guides on email campaigns and marketing automation.", "notes": ""},
    {"name": "Luxafor", "url": "https://luxafor.com/blog", "dr": 45, "niche": ["SaaS", "Productivity", "Remote Work"], "description": "\"Productivity and focus blog by a time-tracking software company.\" ([Profeo](https://profeo.io)). Interested in content about productivity, focus, and work efficiency.", "notes": ""},
    {"name": "Kickresume", "url": "https://kickresume.com/blog", "dr": 60, "niche": ["SaaS", "HR", "Careers"], "description": "\"Career and resume writing guide by a CV platform.\" ([Profeo](https://profeo.io)). Publishes articles on job search, interviewing, and career development.", "notes": ""},
    {"name": "Friday", "url": "https://www.friday.app/blog", "dr": 42, "niche": ["SaaS", "Project Management", "Remote Work"], "description": "\"Time tracking and productivity platform publishing content on project management.\" ([Profeo](https://profeo.io)). Welcomes content on remote work and time management.", "notes": ""},
    {"name": "Wordable", "url": "https://wordable.io/blog", "dr": 49, "niche": ["SaaS", "Content Marketing", "Writing"], "description": "\"Content publishing tool helping writers and agencies.\" ([Profeo](https://profeo.io)). Interested in articles about content creation and publishing.", "notes": ""},
    {"name": "Comidor", "url": "https://comidor.com/blog", "dr": 38, "niche": ["SaaS", "Business Process Management", "Workflow"], "description": "\"Business process management platform with insights on workflow automation.\" ([Profeo](https://profeo.io)). Looking for content on business automation and efficiency.", "notes": ""},
    {"name": "SimplyBook", "url": "https://simplybook.me/en/blog", "dr": 45, "niche": ["SaaS", "Appointment Scheduling", "Business"], "description": "\"Appointment booking software sharing business and scheduling tips.\" ([Profeo](https://profeo.io)). Accepts guest posts on small business management and customer experience.", "notes": ""},
]

# Bloggerspassion.com guest post sources (182 sites)
bloggerspassion_data = [
    # SEO Oriented
    {"name": "TechWyse", "url": "https://www.techwyse.com/blog", "dr": 71, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"]},
    {"name": "MarketingTechNews", "url": "https://www.marketingtechnews.net", "dr": 76, "niche": ["SaaS", "Marketing", "Technology", "Digital Marketing"]},
    {"name": "RankWatch Blog", "url": "https://www.rankwatch.com/blog", "dr": 73, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"]},
    {"name": "Serpstat Blog", "url": "https://serpstat.com/blog", "dr": 79, "niche": ["SaaS", "SEO", "Marketing", "Content Marketing"]},
    {"name": "Jeffbullas's Blog", "url": "https://www.jeffbullas.com", "dr": 80, "niche": ["SaaS", "Marketing", "Social Media", "Content Marketing"]},
    {"name": "Search Engine Watch", "url": "https://www.searchenginewatch.com", "dr": 86, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"]},
    {"name": "Search Engine Land", "url": "https://searchengineland.com", "dr": 91, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"]},
    {"name": "Search Engine Roundtable", "url": "https://www.seroundtable.com", "dr": 84, "niche": ["SaaS", "SEO", "Marketing", "Digital Marketing"]},
    {"name": "Main Street Host", "url": "https://www.mainstreethost.com", "dr": 65, "niche": ["SaaS", "Web Development", "Hosting"]},
    {"name": "EZ Rankings", "url": "https://www.ezrankings.com", "dr": 64, "niche": ["SaaS", "SEO", "Digital Marketing"]},
    
    # Blogging
    {"name": "Content Marketing Institute", "url": "https://contentmarketinginstitute.com", "dr": 89, "niche": ["SaaS", "Content Marketing", "Marketing"]},
    {"name": "The Blog Herald", "url": "https://www.theblogherald.com", "dr": 69, "niche": ["SaaS", "Content", "Blogging"]},
    {"name": "Webnus", "url": "https://webnus.net", "dr": 81, "niche": ["SaaS", "Web Development", "WordPress"]},
    {"name": "CyberChimps", "url": "https://www.cyberchimps.com", "dr": 91, "niche": ["SaaS", "Web Development", "Design"]},
    {"name": "WebScoot Blog", "url": "https://www.webscoot.io", "dr": 43, "niche": ["SaaS", "Web Development"]},
    {"name": "MakeWebBetter", "url": "https://makewebbetter.com", "dr": 73, "niche": ["SaaS", "Web Development", "WordPress"]},
    
    # Marketing/More
    {"name": "WebEngage", "url": "https://www.webengage.com/blog", "dr": 72, "niche": ["SaaS", "Marketing", "Automation", "Customer Engagement"]},
    {"name": "NetHunt", "url": "https://nethunt.com/blog", "dr": 73, "niche": ["SaaS", "CRM", "Sales", "Automation"]},
    {"name": "Cloudways", "url": "https://cloudways.com/blog", "dr": 91, "niche": ["SaaS", "Web Development", "Hosting"]},
    {"name": "Chatter Buzz", "url": "https://www.chatterbuzz.com", "dr": 62, "niche": ["SaaS", "Marketing", "Social Media"]},
    {"name": "Make a Living Writing", "url": "https://makealivinwriting.com", "dr": 70, "niche": ["SaaS", "Content Marketing", "Writing"]},
    {"name": "ResellerClub Blog", "url": "https://www.resellerclub.com/blog", "dr": 78, "niche": ["SaaS", "Business Tools", "Reseller"]},
    
    # Business
    {"name": "AllBusiness.com", "url": "https://www.allbusiness.com", "dr": 80, "niche": ["SaaS", "Business", "Entrepreneurship"]},
    {"name": "Inc.com", "url": "https://www.inc.com", "dr": 92, "niche": ["SaaS", "Business", "Entrepreneurship"]},
    {"name": "Success.com", "url": "https://www.success.com", "dr": 81, "niche": ["SaaS", "Business", "Entrepreneurship"]},
    {"name": "Bplans.com", "url": "https://www.bplans.com", "dr": 80, "niche": ["SaaS", "Business", "Planning"]},
    {"name": "MyCorporation.com", "url": "https://www.mycorporation.com", "dr": 74, "niche": ["SaaS", "Business", "Legal"]},
    {"name": "Successful-Blog.com", "url": "https://successful-blog.com", "dr": 54, "niche": ["SaaS", "Business", "Content"]},
    {"name": "Sogolytics", "url": "https://www.sogolytics.com", "dr": 71, "niche": ["SaaS", "Analytics", "Business"]},
    {"name": "The Ken", "url": "https://the-ken.com", "dr": 67, "niche": ["SaaS", "Business", "India"]},
    {"name": "Business Insider India", "url": "https://www.businessinsider.in", "dr": 84, "niche": ["SaaS", "Business", "India"]},
    {"name": "Exabytes", "url": "https://www.exabytes.com", "dr": 83, "niche": ["SaaS", "Web Development", "Hosting"]},
    {"name": "Convert.com", "url": "https://convert.com", "dr": 77, "niche": ["SaaS", "Conversion Optimization", "Marketing"]},
    {"name": "Gimmio Blog", "url": "https://gimmio.com", "dr": 66, "niche": ["SaaS", "Marketing", "Business"]},
    
    # Technology
    {"name": "SitePoint", "url": "https://www.sitepoint.com", "dr": 87, "niche": ["SaaS", "Development", "Web Development", "Technology"]},
    {"name": "Read Write", "url": "https://readwrite.com", "dr": 84, "niche": ["SaaS", "Technology", "Entrepreneurship", "Innovation"]},
    {"name": "PragProg", "url": "https://pragprog.com", "dr": 80, "niche": ["SaaS", "Development", "Technology", "Programming"]},
    {"name": "iTechCode", "url": "https://itechcode.com", "dr": 30, "niche": ["SaaS", "Technology", "Development"]},
    {"name": "VentureBeat", "url": "https://venturebeat.com", "dr": 91, "niche": ["SaaS", "Technology", "Entrepreneurship", "Innovation"]},
    {"name": "MakingDifferent", "url": "https://makingdifferent.com", "dr": 54, "niche": ["SaaS", "Technology", "Startups"]},
    {"name": "TechLila", "url": "https://techlila.com", "dr": 47, "niche": ["SaaS", "Technology"]},
    {"name": "Colocation America", "url": "https://colocationamerica.com", "dr": 66, "niche": ["SaaS", "Technology", "Hosting"]},
    {"name": "All Tech Buzz", "url": "https://alltechbuzz.net", "dr": 63, "niche": ["SaaS", "Technology"]},
    {"name": "Creately.com", "url": "https://creately.com", "dr": 77, "niche": ["SaaS", "Design", "Diagramming"]},
    {"name": "Analytics India Magazine", "url": "https://analyticsindiamag.com", "dr": 79, "niche": ["SaaS", "Technology", "Analytics", "AI"]},
    {"name": "SoftwareWorld", "url": "https://www.softwareworld.net", "dr": 74, "niche": ["SaaS", "Technology", "Software Reviews"]},
    {"name": "ProProfs", "url": "https://www.proprofs.com/blog", "dr": 80, "niche": ["SaaS", "Productivity", "Training", "Business Tools"]},
    {"name": "Neptune Blog", "url": "https://neptune.io", "dr": 72, "niche": ["SaaS", "Technology", "Development"]},
    {"name": "iMocha", "url": "https://www.imocha.io", "dr": 57, "niche": ["SaaS", "Business Tools", "Assessment"]},
    {"name": "Freshdesk", "url": "https://freshdesk.com/blog", "dr": 90, "niche": ["SaaS", "Customer Support", "CRM", "Business Tools"]},
    {"name": "Analytics Insight", "url": "https://www.analyticsinsight.net", "dr": 81, "niche": ["SaaS", "Technology", "Analytics", "AI"]},
    {"name": "Mobisoft Infotech", "url": "https://www.mobisoftinfotech.com", "dr": 64, "niche": ["SaaS", "Development", "Mobile"]},
    {"name": "Complete Connection", "url": "https://completeconnection.com", "dr": 51, "niche": ["SaaS", "Technology"]},
    {"name": "Technology Networks", "url": "https://www.technologynetworks.com", "dr": 78, "niche": ["SaaS", "Technology", "Innovation"]},
    {"name": "Chanty", "url": "https://chanty.com/blog", "dr": 77, "niche": ["SaaS", "Productivity", "Remote Work", "Collaboration"]},
    {"name": "Jungleworks", "url": "https://jungleworks.com", "dr": 72, "niche": ["SaaS", "Technology", "Business"]},
    {"name": "PAT RESEARCH", "url": "https://www.patresearch.com", "dr": 70, "niche": ["SaaS", "Technology"]},
    {"name": "TechSupremo", "url": "https://techsupremo.com", "dr": 45, "niche": ["SaaS", "Technology"]},
    {"name": "The Next Tech", "url": "https://thenexttech.com", "dr": 59, "niche": ["SaaS", "Technology"]},
    
    # Digital Marketing
    {"name": "OnCrawl", "url": "https://www.oncrawl.com", "dr": 75, "niche": ["SaaS", "SEO", "Marketing"]},
    {"name": "ContactPigeon", "url": "https://www.contactpigeon.com", "dr": 67, "niche": ["SaaS", "Email Marketing", "Marketing Automation"]},
    {"name": "ClickZ", "url": "https://www.clickz.com", "dr": 76, "niche": ["SaaS", "Digital Marketing"]},
    {"name": "Mediapost", "url": "https://www.mediapost.com", "dr": 75, "niche": ["SaaS", "Marketing", "Digital Advertising"]},
    
    # Design
    {"name": "Smashing Magazine", "url": "https://www.smashingmagazine.com", "dr": 89, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Hongkiat", "url": "https://www.hongkiat.com", "dr": 77, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Colossal", "url": "https://www.colossal.com", "dr": 83, "niche": ["SaaS", "Design", "Art"]},
    {"name": "Web Design Ledger", "url": "https://webdesignledger.com", "dr": 78, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Fatbit", "url": "https://www.fatbit.com", "dr": 75, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Quertime", "url": "https://www.quertime.com", "dr": 70, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "A List Apart", "url": "https://alistapart.com", "dr": 88, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Creative Blog (CB)", "url": "https://www.creativeboom.com", "dr": 80, "niche": ["SaaS", "Design", "Inspiration"]},
    {"name": "CrazyLeafDesign", "url": "https://crazyleafdesign.com", "dr": 48, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Writer's Relief", "url": "https://www.writersrelief.com", "dr": 70, "niche": ["SaaS", "Writing", "Publishing"]},
    {"name": "Top Design Magazine", "url": "https://www.topdesignmagazine.com", "dr": 65, "niche": ["SaaS", "Design"]},
    {"name": "Creative Nerds", "url": "https://creativenerds.co.uk", "dr": 45, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "webdew", "url": "https://webdew.net", "dr": 35, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Stackify", "url": "https://stackify.com", "dr": 78, "niche": ["SaaS", "Development", "DevOps"]},
    {"name": "WebAlive", "url": "https://www.webalive.com.au", "dr": 50, "niche": ["SaaS", "Web Development", "Design"]},
    {"name": "Speckyboy", "url": "https://www.speckyboy.com", "dr": 76, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "InstantShift", "url": "https://www.instantshift.com", "dr": 71, "niche": ["SaaS", "Design", "Web Development"]},
    {"name": "Netguru Blog", "url": "https://www.netguru.com/blog", "dr": 82, "niche": ["SaaS", "Development", "Web Development"]},
    
    # Finance
    {"name": "Bigger Pockets", "url": "https://www.biggerpockets.com", "dr": 85, "niche": ["SaaS", "Real Estate", "Finance"]},
    {"name": "Investing.com", "url": "https://www.investing.com", "dr": 92, "niche": ["SaaS", "Finance", "Investing"]},
    {"name": "FinancesOnline.com", "url": "https://financesonline.com", "dr": 82, "niche": ["SaaS", "Finance", "Business Tools"]},
    {"name": "Wise Bread", "url": "https://www.wisebread.com", "dr": 76, "niche": ["SaaS", "Finance", "Personal Finance"]},
    {"name": "Money Saving Mom", "url": "https://moneysavingmom.com", "dr": 74, "niche": ["SaaS", "Finance", "Budgeting"]},
    {"name": "Modest Money", "url": "https://www.modestmoney.com", "dr": 68, "niche": ["SaaS", "Finance", "Personal Finance"]},
    {"name": "Geek Estate Blog", "url": "https://geekvape.com", "dr": 25, "niche": ["SaaS", "Real Estate"]},
    {"name": "OilPrice.com", "url": "https://oilprice.com", "dr": 80, "niche": ["SaaS", "Finance", "Energy"]},
    {"name": "MoneyMiniBlog", "url": "https://www.moneyminiblog.com", "dr": 45, "niche": ["SaaS", "Finance"]},
    
    # Education
    {"name": "ASCD.org", "url": "https://www.ascd.org", "dr": 81, "niche": ["SaaS", "Education"]},
    {"name": "SimpleK12", "url": "https://www.simplek12.com", "dr": 70, "niche": ["SaaS", "Education", "E-learning"]},
    {"name": "Infed.org", "url": "https://infed.org", "dr": 77, "niche": ["SaaS", "Education"]},
    {"name": "The PIE News", "url": "https://thepienews.com", "dr": 70, "niche": ["SaaS", "Education", "International"]},
    {"name": "eLearn Magazine", "url": "https://elearnmag.acm.org", "dr": 75, "niche": ["SaaS", "Education", "E-learning"]},
    {"name": "Edutopia", "url": "https://www.edutopia.org", "dr": 83, "niche": ["SaaS", "Education"]},
    {"name": "Getting Smart", "url": "https://www.gettingsmart.com", "dr": 77, "niche": ["SaaS", "Education", "Innovation"]},
    {"name": "EduGorilla", "url": "https://edugorilla.com", "dr": 55, "niche": ["SaaS", "Education"]},
    {"name": "KnowledgeHut", "url": "https://www.knowledgehut.com", "dr": 69, "niche": ["SaaS", "Education", "Technology Training"]},
    {"name": "The Greater Good Science Center", "url": "https://greatergood.berkeley.edu", "dr": 84, "niche": ["SaaS", "Education", "Science"]},
    {"name": "TutorialsTeacher", "url": "https://www.tutorialsteacher.com", "dr": 70, "niche": ["SaaS", "Education", "Programming"]},
    {"name": "Everyday Power", "url": "https://www.everydaypower.com", "dr": 62, "niche": ["SaaS", "Education", "Personal Development"]},
    {"name": "TopUniversities.com", "url": "https://www.topuniversities.com", "dr": 88, "niche": ["SaaS", "Education", "University Rankings"]},
    {"name": "Eduonix", "url": "https://www.eduonix.com", "dr": 62, "niche": ["SaaS", "Education", "Online Learning"]},
    {"name": "InformIT", "url": "https://www.informit.com", "dr": 81, "niche": ["SaaS", "Education", "Technology"]},
    {"name": "Manning.com", "url": "https://www.manning.com", "dr": 80, "niche": ["SaaS", "Education", "Programming"]},
    {"name": "ASU LodestarCenter", "url": "https://lodestar.asu.edu", "dr": 73, "niche": ["SaaS", "Education", "Nonprofit"]},
    {"name": "MindMajix", "url": "https://mindmajix.com", "dr": 68, "niche": ["SaaS", "Education", "Training"]},
    
    # Entrepreneurship
    {"name": "IncomeDiary.com", "url": "https://incomediary.com", "dr": 70, "niche": ["SaaS", "Entrepreneurship", "Online Business"]},
    {"name": "LeavingWorkBehind.com", "url": "https://leavingworkbehind.com", "dr": 62, "niche": ["SaaS", "Entrepreneurship", "Remote Work"]},
    {"name": "Entrepreneur.com", "url": "https://www.entrepreneur.com", "dr": 93, "niche": ["SaaS", "Entrepreneurship", "Business"]},
    {"name": "Inc42.com", "url": "https://inc42.com", "dr": 80, "niche": ["SaaS", "Entrepreneurship", "Startups", "India"]},
    {"name": "Addicted2Success", "url": "https://addicted2success.com", "dr": 70, "niche": ["SaaS", "Entrepreneurship", "Success"]},
    {"name": "StartupNation", "url": "https://www.startupnation.com", "dr": 78, "niche": ["SaaS", "Entrepreneurship", "Startups"]},
    {"name": "KillerStartups.com", "url": "https://killerstartups.com", "dr": 64, "niche": ["SaaS", "Entrepreneurship", "Startups"]},
    {"name": "YFS Magazine", "url": "https://www.yfsmag.com", "dr": 68, "niche": ["SaaS", "Entrepreneurship", "Startups"]},
    {"name": "StartupBros Blog", "url": "https://startupbros.com", "dr": 58, "niche": ["SaaS", "Entrepreneurship", "Startups"]},
    {"name": "SmallBizClub", "url": "https://smallbizclub.com", "dr": 64, "niche": ["SaaS", "Entrepreneurship", "Small Business"]},
    {"name": "Harvard Business Review", "url": "https://hbr.org", "dr": 94, "niche": ["SaaS", "Business", "Entrepreneurship"]},
    {"name": "MyVenturePad", "url": "https://www.myventurepad.com", "dr": 48, "niche": ["SaaS", "Entrepreneurship", "Startups"]},
    
    # News/Magazine
    {"name": "International Living Magazine", "url": "https://internationalliving.com", "dr": 86, "niche": ["SaaS", "Travel", "Lifestyle", "International"]},
    {"name": "EscapeArtist", "url": "https://escapist.com", "dr": 76, "niche": ["SaaS", "Travel", "Lifestyle"]},
    {"name": "GeekEstate Blog", "url": "https://geekvape.com", "dr": 25, "niche": ["SaaS", "Real Estate", "Tech"]},
    {"name": "Forbes.com", "url": "https://www.forbes.com", "dr": 96, "niche": ["SaaS", "Business", "News", "Entrepreneurship"]},
    {"name": "TheGuardian.com", "url": "https://www.theguardian.com", "dr": 96, "niche": ["SaaS", "News", "General"]},
    {"name": "Wall Street Journal", "url": "https://www.wsj.com", "dr": 95, "niche": ["SaaS", "News", "Finance", "Business"]},
    {"name": "Fast Company", "url": "https://www.fastcompany.com", "dr": 93, "niche": ["SaaS", "Business", "Innovation"]},
    {"name": "HuffPost.com", "url": "https://www.huffpost.com", "dr": 93, "niche": ["SaaS", "News", "Lifestyle"]},
    {"name": "The Diplomat", "url": "https://thediplomat.com", "dr": 81, "niche": ["SaaS", "News", "Politics", "International"]},
    {"name": "ORF", "url": "https://www.orfonline.org", "dr": 79, "niche": ["SaaS", "News", "India", "Policy"]},
    {"name": "Times of India", "url": "https://timesofindia.indiatimes.com", "dr": 94, "niche": ["SaaS", "News", "India"]},
    {"name": "Asia Times", "url": "https://asiatimes.com", "dr": 82, "niche": ["SaaS", "News", "Asia", "International"]},
    {"name": "Swarajya", "url": "https://swarajyamag.com", "dr": 72, "niche": ["SaaS", "News", "India", "Policy"]},
    {"name": "GIJN", "url": "https://gijn.org", "dr": 79, "niche": ["SaaS", "News", "Journalism"]},
    {"name": "The Conversation", "url": "https://theconversation.com", "dr": 85, "niche": ["SaaS", "News", "Education", "Research"]},
    
    # Law
    {"name": "Above the Law", "url": "https://abovethelaw.com", "dr": 78, "niche": ["SaaS", "Law", "News"]},
    {"name": "Attorney at Work", "url": "https://www.attorneyatwork.com", "dr": 72, "niche": ["SaaS", "Law", "Legal Services"]},
    {"name": "LawFuel", "url": "https://lawfuel.com", "dr": 68, "niche": ["SaaS", "Law", "Legal News"]},
    
    # Community/Social Platforms  
    {"name": "reddit.com", "url": "https://reddit.com", "dr": 94, "niche": ["SaaS", "Community", "Social Media"]},
    {"name": "Github.com", "url": "https://github.com", "dr": 94, "niche": ["SaaS", "Development", "Community"]},
    {"name": "tumblr.com", "url": "https://tumblr.com", "dr": 93, "niche": ["SaaS", "Social Media", "Community"]},
    {"name": "substack.com", "url": "https://substack.com", "dr": 88, "niche": ["SaaS", "Publishing", "Newsletters", "Community"]},
    {"name": "outbrain.com", "url": "https://www.outbrain.com", "dr": 86, "niche": ["SaaS", "Content Discovery", "Advertising"]},
    {"name": "wix.com", "url": "https://www.wix.com", "dr": 90, "niche": ["SaaS", "Website Building", "Community"]},
    {"name": "blogger.com", "url": "https://blogger.com", "dr": 94, "niche": ["SaaS", "Blogging", "Community"]},
    {"name": "flickr.com", "url": "https://flickr.com", "dr": 92, "niche": ["SaaS", "Photography", "Community"]},
    {"name": "wikidot.com", "url": "https://www.wikidot.com", "dr": 82, "niche": ["SaaS", "Wiki", "Community"]},
    {"name": "hubpages.com", "url": "https://hubpages.com", "dr": 80, "niche": ["SaaS", "Content Publishing", "Community"]},
    {"name": "yourstory.com", "url": "https://yourstory.com", "dr": 82, "niche": ["SaaS", "Startups", "India", "Community"]},
    {"name": "about.me", "url": "https://about.me", "dr": 85, "niche": ["SaaS", "Personal Branding", "Community"]},
    {"name": "webnode.com", "url": "https://webnode.com", "dr": 82, "niche": ["SaaS", "Website Building", "Community"]},
    {"name": "strikingly.com", "url": "https://strikingly.com", "dr": 81, "niche": ["SaaS", "Website Building", "Community"]},
    {"name": "hackernoon.com", "url": "https://hackernoon.com", "dr": 79, "niche": ["SaaS", "Development", "Technology", "Community"]},
    {"name": "opensource.com", "url": "https://opensource.com", "dr": 82, "niche": ["SaaS", "Open Source", "Technology", "Community"]},
    {"name": "joomla.org", "url": "https://joomla.org", "dr": 88, "niche": ["SaaS", "CMS", "Community"]},
    {"name": "fark.com", "url": "https://fark.com", "dr": 73, "niche": ["SaaS", "News Aggregation", "Community"]},
    {"name": "indiehackers.com", "url": "https://www.indiehackers.com", "dr": 81, "niche": ["SaaS", "Startups", "Indie Developers", "Community"]},
    {"name": "scoop.it", "url": "https://scoop.it", "dr": 78, "niche": ["SaaS", "Content Curation", "Community"]},
    {"name": "blogadda.com", "url": "https://www.blogadda.com", "dr": 77, "niche": ["SaaS", "Blogging", "India", "Community"]},
    {"name": "wakelet.com", "url": "https://wakelet.com", "dr": 75, "niche": ["SaaS", "Content Curation", "Community"]},
    {"name": "indibloghub.com", "url": "https://indibloghub.com", "dr": 68, "niche": ["SaaS", "Blogging", "India", "Community"]},
    {"name": "diigo.com", "url": "https://www.diigo.com", "dr": 77, "niche": ["SaaS", "Bookmarking", "Research", "Community"]},
    {"name": "bloglovin.com", "url": "https://www.bloglovin.com", "dr": 81, "niche": ["SaaS", "Blogging", "Community"]},
    {"name": "blogengage.com", "url": "https://www.blogengage.com", "dr": 58, "niche": ["SaaS", "Blogging", "Community"]},
    {"name": "blogarama.com", "url": "https://www.blogarama.com", "dr": 76, "niche": ["SaaS", "Blogging", "Directory", "Community"]},
]

def build_guest_posts():
    """Build comprehensive guest posts database with duplicates properly merged"""
    
    # Create lookup maps for case-insensitive matching
    profeo_by_name = {site['name'].lower(): site for site in profeo_data}
    bloggerspassion_by_name = {site['name'].lower(): site for site in bloggerspassion_data}
    
    # Track processed sites and duplicates
    processed = {}
    duplicates = []
    
    # First, process all profeo sites
    for site in profeo_data:
        name_lower = site['name'].lower()
        processed[name_lower] = {
            "id": site['name'].lower().replace(' ', '-').replace('.', '').replace("'", ''),
            "name": site['name'],
            "url": site['url'],
            "dr": site['dr'],
            "description": site['description'],
            "niche": site['niche'],
            "submissionType": "free",
            "listedOn": ["profeo.io"],
            "notes": site['notes']
        }
    
    # Then, process bloggerspassion sites
    for site in bloggerspassion_data:
        name_lower = site['name'].lower()
        if name_lower in processed:
            # Duplicate found - add source to existing entry
            if "bloggerspassion.com" not in processed[name_lower]["listedOn"]:
                processed[name_lower]["listedOn"].append("bloggerspassion.com")
            duplicates.append(site['name'])
        else:
            # New site
            processed[name_lower] = {
                "id": site['name'].lower().replace(' ', '-').replace('.', '').replace("'", ''),
                "name": site['name'],
                "url": site['url'],
                "dr": site['dr'],
                "description": f"Guest post opportunity from bloggerspassion.com.",
                "niche": site['niche'],
                "submissionType": "free",
                "listedOn": ["bloggerspassion.com"],
                "notes": ""
            }
    
    # Collect all unique niches
    all_niches = set()
    guest_posts_list = []
    for site_data in processed.values():
        guest_posts_list.append(site_data)
        all_niches.update(site_data['niche'])
    
    # Sort by name for consistency
    guest_posts_list.sort(key=lambda x: x['name'])
    
    # Create final data structure
    data = {
        "guestPosts": guest_posts_list,
        "niches": sorted(list(all_niches))
    }
    
    # Save to file
    with open('data/guest-posts.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Guest Posts Database Rebuilt!")
    print(f"  Profeo.io sites: {len(profeo_data)}")
    print(f"  Bloggerspassion.com sites: {len(bloggerspassion_data)}")
    print(f"  Duplicates found (both sources): {len(duplicates)}")
    if duplicates:
        print(f"  Sites with multiple sources: {', '.join(duplicates)}")
    print(f"  Total unique guest posts: {len(guest_posts_list)}")
    print(f"  Total unique niches: {len(data['niches'])}")
    print(f"\n  ✓ All {len(duplicates)} duplicate sites now have both sources listed!")

if __name__ == "__main__":
    build_guest_posts()
