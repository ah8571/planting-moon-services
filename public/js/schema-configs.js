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
        description: 'A curated guest post database aggregated from multiple public sources. Filter by domain authority and niche to build a practical outreach shortlist.',
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
        description: 'A SaaS-first directories database that can also be combined with adjacent directory types. Filter by platform type, platform fee, and domain rating to build a submission list that matches your product.',
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

// AI Directories Page Configuration
const AI_DIRECTORIES_SCHEMA_CONFIG = {
    pageType: 'aiDirs',
    pageUrl: 'https://plantingmoon.com/aidirectories',
    
    faq: {
        enabled: true,
        extractFromDOM: true,
        faqs: [
            {
                question: 'What are AI directories and why do they matter?',
                answer: 'AI directories are curated collections of AI products, models, agents, and automation tools. Listing in them improves discoverability, credibility, and can help you earn relevant backlinks from high-authority sites.'
            },
            {
                question: 'Should I submit my AI product to general SaaS directories too?',
                answer: 'Yes, if your product overlaps with broader SaaS categories. AI-specific directories help with relevance, while general SaaS directories can widen reach and referral opportunities.'
            },
            {
                question: 'How should I prioritize AI directories?',
                answer: 'Start with directories that combine strong domain authority, clear AI relevance, and a submission model that matches your launch budget. High-authority directories with active curation usually provide the best long-term SEO value.'
            }
        ]
    },

    dataset: {
        enabled: true,
        name: 'AI Directories Database',
        description: 'An AI-first directories database that can be combined with related directory types. Filter by platform type, platform fee, and domain rating to find the best places to list AI products and adjacent software categories.',
        keywords: ['AI directories', 'AI tools directory', 'AI product launch', 'AI marketing', 'AI startup submission'],
        datePublished: '2026-03-15',
        license: 'https://creativecommons.org/publicdomain/zero/1.0/',
        creator: {
            '@type': 'Organization',
            'name': 'Planting Moon',
            'url': 'https://plantingmoon.com'
        }
    },

    organization: {
        enabled: true
    },

    breadcrumb: {
        enabled: true,
        items: [
            { name: 'Home', url: 'https://plantingmoon.com' },
            { name: 'Free Tools', url: 'https://plantingmoon.com/free-tools' },
            { name: 'AI Directories', url: 'https://plantingmoon.com/aidirectories' }
        ]
    }
};

// All Directories Page Configuration
const ALL_DIRECTORIES_SCHEMA_CONFIG = {
    pageType: 'allDirs',
    pageUrl: 'https://plantingmoon.com/directories',

    faq: {
        enabled: true,
        extractFromDOM: true,
        faqs: [
            {
                question: 'Can I combine multiple directory types on this page?',
                answer: 'Yes. Open the Directory Type filter and select more than one type to build a broader list, such as AI Directory plus SaaS Directory for products that span both categories.'
            },
            {
                question: 'Why keep separate landing pages if this page shows all directories?',
                answer: 'The generic explorer is the flexible master view, while dedicated pages like SaaS directories and AI directories provide focused entry points for people searching for a narrower list.'
            },
            {
                question: 'What is the best way to use this chart for submission research?',
                answer: 'Start with the default list or a narrow type filter, then combine adjacent categories, compare platform fee and domain rating, and export only the directories that fit your product positioning and launch stage.'
            }
        ]
    },

    dataset: {
        enabled: true,
        name: 'Startup Directories Database',
        description: 'A flexible directories database for startup, SaaS, AI, and related product categories. Filter by one or more directory types, platform fee, and domain rating to build a submission list that fits your product.',
        keywords: ['startup directories', 'saas directories', 'ai directories', 'product launch directories', 'directory filters'],
        datePublished: '2026-03-31',
        license: 'https://creativecommons.org/publicdomain/zero/1.0/',
        creator: {
            '@type': 'Organization',
            'name': 'Planting Moon',
            'url': 'https://plantingmoon.com'
        }
    },

    organization: {
        enabled: true
    },

    breadcrumb: {
        enabled: true,
        items: [
            { name: 'Home', url: 'https://plantingmoon.com' },
            { name: 'Free Tools', url: 'https://plantingmoon.com/free-tools' },
            { name: 'Directories', url: 'https://plantingmoon.com/directories' }
        ]
    }
};

if (typeof window !== 'undefined') {
    Object.assign(window, {
        GUEST_POSTS_SCHEMA_CONFIG,
        SAAS_DIRECTORIES_SCHEMA_CONFIG,
        AI_DIRECTORIES_SCHEMA_CONFIG,
        ALL_DIRECTORIES_SCHEMA_CONFIG
    });
}

// Export configs
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        GUEST_POSTS_SCHEMA_CONFIG,
        SAAS_DIRECTORIES_SCHEMA_CONFIG,
        AI_DIRECTORIES_SCHEMA_CONFIG,
        ALL_DIRECTORIES_SCHEMA_CONFIG
    };
}
