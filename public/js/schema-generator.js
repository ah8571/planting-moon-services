/**
 * Schema Generator - Creates JSON-LD markup for SEO
 * Generates FAQPage, Dataset, and Organization schemas
 */

class SchemaGenerator {
    constructor(baseConfig = {}) {
        this.baseConfig = {
            organizationName: 'Planting Moon',
            organizationUrl: 'https://plantingmoon.com',
            organizationLogo: 'https://plantingmoon.com/logo.png',
            ...baseConfig
        };
    }

    /**
     * Generate Organization schema
     */
    generateOrganization(overrides = {}) {
        const config = { ...this.baseConfig, ...overrides };
        return {
            '@context': 'https://schema.org',
            '@type': 'Organization',
            'name': config.organizationName,
            'url': config.organizationUrl,
            'logo': config.organizationLogo,
            'sameAs': [
                'https://www.linkedin.com/company/planting-moon',
                'https://twitter.com/plantingmoon'
            ].filter(url => url)
        };
    }

    /**
     * Generate FAQPage schema
     * @param {Array} faqs - Array of FAQ objects with question and answer properties
     * @param {string} pageUrl - The URL of the page
     */
    generateFAQPage(faqs = [], pageUrl = '') {
        return {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': faqs.map(faq => ({
                '@type': 'Question',
                'name': faq.question,
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': faq.answer
                }
            }))
        };
    }

    /**
     * Generate Dataset schema
     * @param {Object} config - Configuration object
     * @param {string} config.name - Dataset name
     * @param {string} config.description - Dataset description
     * @param {string} config.url - Dataset URL
     * @param {number} config.itemCount - Total number of items in dataset
     * @param {Array} config.keywords - Array of keywords
     * @param {Object} config.distribution - Distribution info
     * @param {string} config.datePublished - Publication date
     * @param {Object} config.creator - Creator information (Organization or Person)
     * @param {string} config.license - License URL or name
     */
    generateDataset(config = {}) {
        const schema = {
            '@context': 'https://schema.org',
            '@type': 'Dataset',
            'name': config.name || 'Directory Dataset',
            'description': config.description || '',
            'url': config.url || '',
            'keywords': config.keywords || [],
            'license': config.license || 'https://creativecommons.org/publicdomain/zero/1.0/'
        };

        if (config.itemCount) {
            schema.variableMeasured = [{
                '@type': 'PropertyValue',
                'name': 'Total Items',
                'value': config.itemCount
            }];
        }

        if (config.distribution) {
            schema.distribution = [{
                '@type': 'DataDownload',
                'encodingFormat': 'JSON',
                'contentUrl': config.distribution.url || ''
            }];
        }

        if (config.datePublished) {
            schema.datePublished = config.datePublished;
        }

        // Properly format creator as Organization
        if (config.creator) {
            if (typeof config.creator === 'object' && config.creator['@type']) {
                // Already a proper schema object
                schema.creator = config.creator;
            } else {
                // Create Organization from base config
                schema.creator = {
                    '@type': 'Organization',
                    'name': this.baseConfig.organizationName || 'Planting Moon',
                    'url': this.baseConfig.organizationUrl || 'https://plantingmoon.com'
                };
            }
        }

        return schema;
    }

    /**
     * Generate SearchAction schema for searchable pages
     * @param {string} searchUrl - URL where search results appear
     */
    generateSearchAction(searchUrl = '') {
        return {
            '@context': 'https://schema.org',
            '@type': 'WebSite',
            'url': searchUrl,
            'potentialAction': {
                '@type': 'SearchAction',
                'target': {
                    '@type': 'EntryPoint',
                    'urlTemplate': searchUrl + '?q={search_term_string}'
                },
                'query-input': 'required name=search_term_string'
            }
        };
    }

    /**
     * Generate Breadcrumb schema
     * @param {Array} breadcrumbs - Array of breadcrumb objects with name and url
     */
    generateBreadcrumb(breadcrumbs = []) {
        return {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': breadcrumbs.map((crumb, index) => ({
                '@type': 'ListItem',
                'position': index + 1,
                'name': crumb.name,
                'item': crumb.url
            }))
        };
    }

    /**
     * Inject schema into page head
     * @param {Object} schema - Schema object to inject
     * @param {string} id - Optional ID for the script tag
     */
    injectSchema(schema, id = '') {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        if (id) script.id = id;
        script.textContent = JSON.stringify(schema);
        document.head.appendChild(script);
        return script;
    }

    /**
     * Inject multiple schemas
     * @param {Array} schemas - Array of schemas to inject
     */
    injectSchemas(schemas = []) {
        return schemas.map((schema, index) => 
            this.injectSchema(schema.schema, schema.id || `schema-${index}`)
        );
    }

    /**
     * Extract FAQs from page DOM
     * Expects structure: .faq-item > h3 (question) and .faq-answer (answer)
     */
    extractFAQsFromDOM() {
        const faqs = [];
        document.querySelectorAll('.faq-item').forEach(item => {
            const questionEl = item.querySelector('h3');
            const answerEl = item.querySelector('.faq-answer');
            
            if (questionEl && answerEl) {
                faqs.push({
                    question: questionEl.textContent.trim(),
                    answer: answerEl.textContent.trim()
                });
            }
        });
        return faqs;
    }
}

// Export for use in both module and browser contexts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SchemaGenerator;
}
