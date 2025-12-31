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

### Architecture Highlights
1. **Component System**: Navbar and footer are separate HTML files with embedded CSS and JavaScript loaders
2. **Single Source of Truth**: All navbar CSS in navbar.html, all footer CSS in footer.html
3. **Clean URLs**: `/contact`, `/case-studies`, `/saasdirectories` instead of file paths
4. **Static Deployment**: No build process required, Vercel serves files directly from `/public`

---

## Common Development Tasks

### Adding a New Page
1. Create new `.html` file in `/public`
2. Include navbar: `<nav id="navbar-container"></nav>`
3. Include footer: `<div id="footer-container"></div>`
4. Load scripts: `<script src="./navbar.js"></script>` and `<script src="./footer.js"></script>`
5. Add page-specific CSS only (components handle their own styling)

### Updating Navigation
- Edit `navbar.html` only (changes propagate to all pages)
- Edit `footer.html` for footer changes
- Update links in both files if adding new pages

### Adding New Data
- Store in `public/data/filename.json`
- Use relative path: `./data/filename.json`
- Ensure valid JSON format

### Modifying Styling
- **Navbar CSS**: Edit `<style>` in `navbar.html`
- **Footer CSS**: Edit `<style>` in `footer.html`
- **Page-specific CSS**: Add only to that page's `<style>` tag

---

## Recent Major Updates (Phase 1 - Completed)
- ✅ Consolidated all files to `/public` folder for Vercel deployment
- ✅ Removed duplicate component files
- ✅ Implemented component system with CSS consolidation
- ✅ Implemented clean URLs
- ✅ Fixed navbar alignment issues across all pages
- ✅ Fixed SaaS directories page JSON loading issue
- ✅ Removed CSS conflicts (no duplicate styles on landing pages)

---

## Known Working Features
- ✅ Navbar/footer injection on all pages
- ✅ Contact form submission (Formspree)
- ✅ SaaS directories search, filter, and pagination
- ✅ Responsive design
- ✅ Clean URL routing
- ✅ All navigation links functional

---

## Deployment
- **Platform**: Vercel
- **Source**: GitHub repository
- **Deployment**: Automatic on push to main branch
- **Configuration**: `vercel.json` handles routing and headers

---

## For Future Agents

### If Tasked With...

**Bug Fixes or Debugging**
- Check console for errors (browser dev tools)
- Look at component files first (navbar.html, footer.html)
- Verify JSON paths are correct (must be relative: `./data/filename.json`)
- Check for CSS conflicts (compare against component files)

**Adding Features**
- Reference `DEVELOPMENT_ROADMAP.md` for planned features
- Follow component architecture (reusable, injectable)
- Keep CSS in components, not in page files
- Test on all pages to ensure consistency

**Performance Issues**
- Check file sizes (JSON data, scripts)
- Verify no duplicate CSS loading
- Look for inefficient JavaScript loops
- Consider image optimization

**Styling Issues**
- Always check if styles are in component files first
- Verify CSS specificity isn't causing conflicts
- Test on multiple pages (components should be consistent)
- Check for responsive design breakpoints

---

## Contact & Questions
Refer to commit history in GitHub for specific implementation details and context about changes made. Each commit includes detailed messages about what was changed and why.

---

**Version**: 1.0  
**Last Updated**: December 31, 2025  
**Purpose**: Project brief for agents and future developers
