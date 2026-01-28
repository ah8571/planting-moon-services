/**
 * Schema Configurations for Free Tools Pages
 * Defines what schemas to load on each page
 */

// Guest Posts Page Configuration
const GUEST_POSTS_SCHEMA_CONFIG = {
    pageType: 'guestPosts',
    pageUrl: 'https://plantingmoon.com/guest-posts',
    
    // FAQPage schema
    faq: {
        enabled: true,
        extractFromDOM: true, // Automatically extract FAQs from .faq-item elements
        // Or provide manually:
        faqs: [
            {
                question: 'What exactly is guest posting and how does it help my SEO?',
                answer: 'Guest posting is the process of writing and publishing content on another company\'s blog or website in exchange for a byline and a link back to your website. It helps your SEO because you\'re acquiring high-quality backlinks from authoritative, relevant websites.'
            },
            {
                question: 'Why is domain authority important for guest posting?',
                answer: 'Domain authority indicates a website\'s credibility and influence. Higher DA websites pass more SEO value through their links. A link from a DA 60+ site is exponentially more valuable than from a DA 20 site.'
            },
            {
                question: 'How do I know if a guest posting opportunity is worth my time?',
                answer: 'Look for: 1) Domain authority of 30+, 2) Relevance to your niche, 3) Active audience engagement, 4) No nofollow links in the byline, 5) Clear submission guidelines.'
            }
        ]
    },

    // Dataset schema
    dataset: {
        enabled: true,
        name: 'Free Guest Post Sites Database',
        description: 'A comprehensive collection of 593 verified free guest posting opportunities aggregated from multiple trusted sources. Filter by domain authority, niche category, or submission type.',
        keywords: ['guest posting', 'link building', 'SEO', 'backlinks', 'guest post opportunities', 'domain authority'],
        datePublished: '2026-01-01',
        license: 'https://creativecommons.org/publicdomain/zero/1.0/',
        creator: {
            '@type': 'Organization',
            'name': 'Planting Moon',
            'url': 'https://plantingmoon.com'
        }
    },

    // Organization schema
    organization: {
        enabled: true
    },

    // Breadcrumb schema
    breadcrumb: {
        enabled: true,
        items: [
            { name: 'Home', url: 'https://plantingmoon.com' },
            { name: 'Free Tools', url: 'https://plantingmoon.com/free-tools' },
            { name: 'Guest Posts', url: 'https://plantingmoon.com/guest-posts' }
        ]
    }
};

// SaaS Directories Page Configuration
const SAAS_DIRECTORIES_SCHEMA_CONFIG = {
    pageType: 'saasDirs',
    pageUrl: 'https://plantingmoon.com/saasdirectories',
    
    // FAQPage schema
    faq: {
        enabled: true,
        extractFromDOM: true, // Automatically extract FAQs from .faq-item elements
        // Or provide manually:
        faqs: [
            {
                question: 'What are SaaS directories and why do they matter?',
                answer: 'SaaS directories are platforms that aggregate and showcase software-as-a-service products. Getting listed helps with visibility, credibility, and SEO. Many have high domain authority which means quality backlinks.'
            },
            {
                question: 'How many directories should I submit to?',
                answer: 'Quality over quantity. Focus on directories relevant to your niche with domain authority above 30. 10-15 high-quality submissions will have more impact than 100 low-quality ones.'
            },
            {
                question: 'Do all directories provide backlinks?',
                answer: 'Not all. Some are nofollow links, while others are dofollow. This database indicates which provide domain rating and tracks their backlink value.'
            },
            {
                question: 'How often should I update my directory listings?',
                answer: 'After initial submission, update listings when major changes occur (pricing, features, company info). Most directories maintain your listing automatically once submitted.'
            }
        ]
    },

    // Dataset schema
    dataset: {
        enabled: true,
        name: 'SaaS Directories Database',
        description: 'A curated collection of 160+ free SaaS directories aggregated from multiple sources. Filter by platform type, free/paid status, and domain rating to find the best platforms for your product.',
        keywords: ['SaaS directories', 'product directory', 'SaaS marketing', 'product launch', 'directory submission'],
        datePublished: '2026-01-01',
        license: 'https://creativecommons.org/publicdomain/zero/1.0/',
        creator: {
            '@type': 'Organization',
            'name': 'Planting Moon',
            'url': 'https://plantingmoon.com'
        }
    },

    // Organization schema
    organization: {
        enabled: true
    },

    // Breadcrumb schema
    breadcrumb: {
        enabled: true,
        items: [
            { name: 'Home', url: 'https://plantingmoon.com' },
            { name: 'Free Tools', url: 'https://plantingmoon.com/free-tools' },
            { name: 'SaaS Directories', url: 'https://plantingmoon.com/saasdirectories' }
        ]
    }
};

// Export configs
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        GUEST_POSTS_SCHEMA_CONFIG,
        SAAS_DIRECTORIES_SCHEMA_CONFIG
    };
}
