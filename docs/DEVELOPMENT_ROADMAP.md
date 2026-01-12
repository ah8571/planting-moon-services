# Trading Moon - Development Roadmap

**Status**: v1.0 - Stable production  
**Last Updated**: December 31, 2025

To Do:
- **another directory list to consider reviewing** https://uneed-directories.com/

---

## ✅ Phase 1: Completed

- Component system (navbar/footer with CSS)
- CSS consolidation (single source of truth)
- Clean URLs (/contact, /case-studies, /saasdirectories)
- Landing pages (Homepage, Contact, Case Studies, SaaS Directories)
- Bug fixes (JSON path, navbar alignment, CSS conflicts)
- Vercel deployment with proper routing

**Current Pages**: index.html, contact.html, case-studies.html, saasdirectories.html, navbar.html, footer.html

---

## 📋 Phase 2-3: Near-term (Next 3-6 months)

### Performance & SEO
- [ ] Lazy loading for images
- [ ] Meta descriptions and Open Graph tags
- [ ] Google Analytics & error monitoring
- [ ] Minify JS/CSS

### Content Expansion
- [ ] Blog page & functionality
- [ ] About Us page
- [ ] Service detail pages (Web Dev, Mobile Dev, MVP, etc.)
- [ ] Privacy Policy & Terms of Service
- [ ] Case study filtering

### SaaS Directories Enhancements
- [ ] Favorites/bookmarking (localStorage)
- [ ] Export to CSV
- [ ] Advanced filtering and search
- [ ] Mobile-optimized table

---

## 🛠️ Phase 4: Technical (6-12 months)

- [ ] Extract inline scripts to separate files
- [ ] Unit tests & automated browser testing
- [ ] Accessibility audit (WCAG 2.1)
- [ ] Build tool integration (Vite/Webpack)
- [ ] CI/CD automation
- [ ] Developer documentation

---

## 🚀 Phase 5: Advanced (12+ months)

- [ ] CMS integration (Contentful/Strapi)
- [ ] Dark mode & theme customization
- [ ] Backend API for data management
- [ ] Multi-language support
- [ ] Admin dashboard
- [ ] Live chat widget


---

## 👷 Development Quick Tips

**Add New Page**
1. Create `/public/newpage.html`
2. Include navbar and footer containers
3. Load: `<script src="./navbar.js"></script>` and `footer.js`
4. Add only page-specific CSS

**Update Navigation/Footer**
- Edit only `navbar.html` or `footer.html`
- Changes auto-propagate to all pages
- Never add these styles to landing pages

**Add Data**
- Store in `public/data/filename.json`
- Use relative paths: `./data/filename.json`

---

**For project context**: See AGENT.md
