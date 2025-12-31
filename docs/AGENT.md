# Trading Moon Project - Agent Brief

## Project Overview
Trading Moon is a static HTML/CSS/JavaScript website deployed on Vercel. The site showcases services including Web/Mobile app development, MVP development, SEO/PPC help, and analytics consulting. It also features a comprehensive SaaS Directories Aggregator (500+ directories).

**Current Status**: v1.0 - Stable production deployment  
**Last Updated**: December 31, 2025

---

## Quick Context for Agents

### What This Project Does
- **Landing page** showcasing development and consulting services
- **Service pages** detailing Web/Mobile app development, MVP development, SEO, PPC, Analytics, and Automation consulting
- **Case studies** demonstrating successful project implementations
- **Contact form** for potential clients to reach out
- **SaaS Directories Aggregator** - a searchable tool with 500+ SaaS submission platforms, sortable by domain rating and service type

### Tech Stack
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Hosting**: Vercel (static site)
- **Components**: Reusable navbar and footer with JavaScript injection
- **Data**: JSON-based (directories.json for SaaS listings)
- **Routing**: Clean URLs with Vercel configuration

### Key Files & Structure
```
public/
├── index.html                 # Homepage
├── contact.html              # Contact form (Formspree integration)
├── case-studies.html         # Case studies showcase
├── saasdirectories.html      # SaaS aggregator tool
├── navbar.html               # Navigation component (with CSS)
├── footer.html               # Footer component (with CSS)
├── navbar.js                 # Navbar loader
├── footer.js                 # Footer loader
├── data/
│   └── directories.json      # 500+ SaaS directories data
├── sitemap.xml               # SEO
└── robots.txt                # Search engines

vercel.json                   # Routing & deployment config
docs/
├── DEVELOPMENT_ROADMAP.md   # Full project roadmap
└── AGENT.md                 # This file
```

