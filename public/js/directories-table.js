let allDirectories = [];
let filteredDirectories = [];
let currentTypeFilters = [];
let currentSubmissionFilter = null;
let currentSourcesFilters = [];
let sortByName = false;
let sortDirection = 'asc';
let currentPage = 1;

const ITEMS_PER_PAGE = 50;
const defaultTypeFilter = normalizeFilterValue(document.body.dataset.defaultTypeFilter || '');
const schemaConfigName = document.body.dataset.schemaConfig || 'SAAS_DIRECTORIES_SCHEMA_CONFIG';
const pageLogPrefix = document.body.dataset.pageLogPrefix || 'directories';
const typeLabelMap = new Map();

function downloadBlob(filename, content, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
}

function escapeCsvValue(value) {
    const stringValue = value == null ? '' : String(value);
    const escaped = stringValue.replace(/"/g, '""');
    return `"${escaped}"`;
}

function convertDirectoriesToCsv(directories) {
    const headers = ['Name', 'URL', 'Type', 'Platform Fee', 'Domain Rating', 'Sources', 'Description', 'Notes'];
    const rows = directories.map(directory => {
        const typeValue = Array.isArray(directory.type) ? directory.type.join('; ') : directory.type || '';
        const submissionValue = Array.isArray(directory.submissionType)
            ? directory.submissionType.join('; ')
            : directory.submissionType || '';
        const sourcesValue = Array.isArray(directory.listedOn) ? directory.listedOn.join('; ') : '';

        return [
            directory.name,
            directory.url,
            typeValue,
            submissionValue,
            directory.domainRating,
            sourcesValue,
            directory.description || '',
            directory.notes || ''
        ].map(escapeCsvValue).join(',');
    });

    return [headers.map(escapeCsvValue).join(','), ...rows].join('\n');
}

function setupDownloadActions() {
    const filteredJsonButton = document.getElementById('download-filtered-json');
    const filteredCsvButton = document.getElementById('download-filtered-csv');

    filteredJsonButton?.addEventListener('click', () => {
        const payload = {
            exportedAt: new Date().toISOString(),
            filterSummary: {
                typeFilters: currentTypeFilters,
                submissionFilter: currentSubmissionFilter,
                sourcesFilters: currentSourcesFilters
            },
            directories: filteredDirectories
        };
        downloadBlob('directories-filtered.json', JSON.stringify(payload, null, 2), 'application/json');
    });

    filteredCsvButton?.addEventListener('click', () => {
        downloadBlob('directories-filtered.csv', convertDirectoriesToCsv(filteredDirectories), 'text/csv;charset=utf-8;');
    });
}

function getDirectoryName(dir) {
    return (dir?.name || '').toString().trim().toLowerCase();
}

function logSortPreview(label, directories) {
    console.log(`[${pageLogPrefix}] ${label}`, directories.slice(0, 5).map(dir => dir.name));
}

function normalizeSubmissionTypes(submissionType) {
    const values = Array.isArray(submissionType) ? submissionType : [submissionType];
    return values
        .filter(value => typeof value === 'string' && value.trim())
        .map(value => value.trim().toLowerCase());
}

function formatSubmissionTypeLabel(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
}

function normalizeFilterValue(value) {
    return typeof value === 'string'
        ? value.trim().replace(/\s+/g, ' ').toLowerCase()
        : '';
}

function syncTypeFilterButtons() {
    document.querySelectorAll('#type-filters .filter-btn[data-type-filter]').forEach(button => {
        const isActive = currentTypeFilters.includes(button.dataset.typeFilter);
        button.classList.toggle('active', isActive);
    });
}

function setTypeFilters(typeFilters) {
    currentTypeFilters = Array.from(new Set((typeFilters || []).filter(Boolean)));
    syncTypeFilterButtons();
    updateTypeFilterSummary();
}

function toggleTypeFilter(typeFilter) {
    if (!typeFilter) {
        setTypeFilters([]);
        return;
    }

    if (currentTypeFilters.includes(typeFilter)) {
        setTypeFilters(currentTypeFilters.filter(filter => filter !== typeFilter));
        return;
    }

    setTypeFilters([...currentTypeFilters, typeFilter]);
}

function applyInitialTypeFilter() {
    if (!defaultTypeFilter) {
        updateTypeFilterSummary();
        return false;
    }

    const matchingButton = document.querySelector(`#type-filters .filter-btn[data-type-filter="${defaultTypeFilter}"]`);
    if (!matchingButton) {
        console.warn(`[${pageLogPrefix}] Default type filter button not found`, defaultTypeFilter);
        updateTypeFilterSummary();
        return false;
    }

    setTypeFilters([defaultTypeFilter]);
    console.log(`[${pageLogPrefix}] Applied initial type filter`, defaultTypeFilter);
    return true;
}

function updateTypeFilterSummary() {
    const summary = document.getElementById('type-filter-summary');
    if (!summary) {
        return;
    }

    if (currentTypeFilters.length === 0) {
        summary.textContent = 'Showing all directory types. Open Directory Type to narrow the list or combine multiple product categories.';
        return;
    }

    const labels = currentTypeFilters.map(typeFilter => typeLabelMap.get(typeFilter) || typeFilter);
    summary.textContent = `Active type filters: ${labels.join(' + ')}.`;
}

async function loadDirectories() {
    try {
        const response = await fetch('/data/directories.json');
        if (!response.ok) {
            throw new Error('Could not load directories.json');
        }
        const data = await response.json();
        allDirectories = data.directories || [];

        allDirectories = allDirectories.filter(directory => directory.domainRating !== 'unknown' && directory.domainRating >= 30);
        allDirectories.sort((a, b) => b.domainRating - a.domainRating);

        console.log(`[${pageLogPrefix}] Loaded directories`, {
            totalLoaded: data.directories?.length || 0,
            totalWithDR: allDirectories.length
        });
        logSortPreview('Initial DR sort preview', allDirectories);

        generateTypeFilters();
        generateSourcesFilters();

        if (applyInitialTypeFilter()) {
            applyFilters();
        } else {
            filteredDirectories = [...allDirectories];
            renderTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading directories:', error);
        document.getElementById('table-body').innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 40px;">
                    Error loading directories.json<br>
                    <small style="color: #999;">Make sure the file is in the data/ folder relative to this HTML file</small>
                </td>
            </tr>
        `;
    }
}

function applyFilters() {
    let filtered = [...allDirectories];

    if (currentTypeFilters.length > 0) {
        filtered = filtered.filter(directory => {
            const types = Array.isArray(directory.type) ? directory.type : [directory.type];
            return types.some(type => currentTypeFilters.includes(normalizeFilterValue(type)));
        });
    }

    if (currentSubmissionFilter) {
        filtered = filtered.filter(directory => normalizeSubmissionTypes(directory.submissionType).includes(currentSubmissionFilter));
    }

    if (currentSourcesFilters.length > 0) {
        filtered = filtered.filter(directory => {
            const sourceCount = directory.listedOn ? directory.listedOn.length : 0;
            return currentSourcesFilters.includes(sourceCount);
        });
    }

    if (sortByName) {
        filtered.sort((a, b) => {
            const nameA = a.name.toLowerCase();
            const nameB = b.name.toLowerCase();
            return sortDirection === 'asc'
                ? nameA.localeCompare(nameB)
                : nameB.localeCompare(nameA);
        });
    } else {
        filtered.sort((a, b) => b.domainRating - a.domainRating);
    }

    console.log(`[${pageLogPrefix}] applyFilters state`, {
        typeFilters: currentTypeFilters,
        submissionFilter: currentSubmissionFilter,
        sourcesFilters: currentSourcesFilters,
        sortByName,
        sortDirection,
        resultCount: filtered.length
    });
    logSortPreview(sortByName ? `Name sort (${sortDirection}) preview` : 'DR sort preview', filtered);

    currentPage = 1;
    filteredDirectories = filtered;
    renderTable();
    updateStats();
}

function renderTable() {
    const tbody = document.getElementById('table-body');

    if (filteredDirectories.length === 0) {
        tbody.innerHTML = '<tr class="no-results"><td colspan="6">No directories found</td></tr>';
        document.getElementById('pagination-info-top').textContent = '';
        document.getElementById('pagination-info').textContent = '';
        document.getElementById('prev-btn').style.display = 'none';
        document.getElementById('next-btn').style.display = 'none';
        return;
    }

    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const pageItems = filteredDirectories.slice(startIndex, endIndex);
    const totalPages = Math.ceil(filteredDirectories.length / ITEMS_PER_PAGE);

    tbody.innerHTML = pageItems.map(directory => {
        const drClass = directory.domainRating >= 80
            ? 'dr-high'
            : directory.domainRating >= 60
                ? 'dr-medium'
                : 'dr-low';

        const nameDisplay = directory.url && directory.url.trim() !== ''
            ? `<a href="${directory.url}" target="_blank" rel="noopener noreferrer">${directory.name}</a>`
            : `<span class="name-text">${directory.name}</span>`;

        const submissionTypeValues = normalizeSubmissionTypes(directory.submissionType);
        const submissionTypeBadge = submissionTypeValues.length === 0 || submissionTypeValues.includes('unknown')
            ? ''
            : submissionTypeValues
                .map(value => `<span class="submission-type-badge">${formatSubmissionTypeLabel(value)}</span>`)
                .join('');

        const typeArray = Array.isArray(directory.type) ? directory.type : [directory.type];
        const typeBadges = typeArray
            .filter(type => typeof type === 'string' && type.trim())
            .map(type => `<span class="type-badge">${type}</span>`)
            .join('');

        return `
            <tr>
                <td class="name">${nameDisplay}</td>
                <td>${typeBadges || '<span class="type-badge">N/A</span>'}</td>
                <td>${submissionTypeBadge}</td>
                <td><span class="dr-badge ${drClass}">${directory.domainRating}</span></td>
                <td class="sources">${directory.listedOn.join(', ')}</td>
            </tr>
        `;
    }).join('');

    const startNum = (currentPage - 1) * ITEMS_PER_PAGE + 1;
    const endNum = Math.min(currentPage * ITEMS_PER_PAGE, filteredDirectories.length);
    const paginationText = `Showing ${startNum} - ${endNum} of ${filteredDirectories.length} directories`;
    document.getElementById('pagination-info-top').textContent = paginationText;
    document.getElementById('pagination-info').textContent = paginationText;

    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    prevBtn.style.display = currentPage > 1 ? 'block' : 'none';
    nextBtn.style.display = currentPage < totalPages ? 'block' : 'none';
}

function updateStats() {
    document.getElementById('total-count').textContent = filteredDirectories.length;

    const withDR = filteredDirectories.filter(directory => directory.domainRating !== 'unknown');
    document.getElementById('with-dr-count').textContent = withDR.length;

    if (withDR.length === 0) {
        document.getElementById('avg-dr').textContent = '0';
        document.getElementById('highest-dr').textContent = '0';
        return;
    }

    const avgDR = (withDR.reduce((sum, directory) => sum + directory.domainRating, 0) / withDR.length).toFixed(1);
    const maxDR = Math.max(...withDR.map(directory => directory.domainRating));
    document.getElementById('avg-dr').textContent = avgDR;
    document.getElementById('highest-dr').textContent = maxDR;
}

function generateTypeFilters() {
    allDirectories.forEach(directory => {
        const types = Array.isArray(directory.type) ? directory.type : (directory.type ? [directory.type] : []);
        types.forEach(type => {
            const normalizedType = normalizeFilterValue(type);
            if (normalizedType && !typeLabelMap.has(normalizedType)) {
                typeLabelMap.set(normalizedType, type.trim().replace(/\s+/g, ' '));
            }
        });
    });

    const sortedTypes = Array.from(typeLabelMap.entries()).sort((a, b) => a[1].localeCompare(b[1]));
    const typeFiltersContainer = document.getElementById('type-filters');
    typeFiltersContainer.innerHTML = '';

    const clearButton = document.createElement('button');
    clearButton.className = 'filter-btn';
    clearButton.dataset.clearTypeFilters = 'true';
    clearButton.textContent = 'Clear types';
    clearButton.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        setTypeFilters([]);
        applyFilters();
    });
    typeFiltersContainer.appendChild(clearButton);

    sortedTypes.forEach(([normalizedType, displayType]) => {
        const button = document.createElement('button');
        button.className = 'filter-btn';
        button.dataset.typeFilter = normalizedType;
        button.textContent = displayType;
        button.addEventListener('click', event => {
            event.preventDefault();
            event.stopPropagation();
            toggleTypeFilter(button.dataset.typeFilter);
            applyFilters();
        });
        typeFiltersContainer.appendChild(button);
    });

    document.getElementById('type-header').addEventListener('click', event => {
        if (!event.target.closest('.filter-btn')) {
            typeFiltersContainer.classList.toggle('open');
            document.querySelector('#type-header .th-chevron').classList.toggle('open');
        }
    });
}

function generateSourcesFilters() {
    const sourceCounts = {};
    allDirectories.forEach(directory => {
        const count = directory.listedOn ? directory.listedOn.length : 0;
        sourceCounts[count] = (sourceCounts[count] || 0) + 1;
    });

    const container = document.getElementById('sources-filters');
    container.innerHTML = '';

    Object.keys(sourceCounts).sort((a, b) => b - a).forEach(count => {
        const button = document.createElement('button');
        button.className = 'filter-btn';
        button.textContent = `${count} source${count > 1 ? 's' : ''} (${sourceCounts[count]})`;
        button.dataset.sourcesFilter = count;
        button.addEventListener('click', event => toggleSourcesFilter(count, button, event));
        container.appendChild(button);
    });
}

function toggleNameSort() {
    const button = document.querySelector('#name-header .th-header');
    const chevron = button?.querySelector('.th-chevron');

    console.log(`[${pageLogPrefix}] Directory Name header clicked`, {
        previousSortByName: sortByName,
        previousSortDirection: sortDirection,
        activeTypeFilters: currentTypeFilters,
        activeSubmissionFilter: currentSubmissionFilter,
        activeSourcesFilters: currentSourcesFilters,
        currentVisibleCount: filteredDirectories.length
    });

    if (sortByName) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
        if (chevron) {
            chevron.style.transform = sortDirection === 'desc' ? 'rotate(180deg)' : 'rotate(0deg)';
        }
    } else {
        sortByName = true;
        sortDirection = 'asc';
        if (chevron) {
            chevron.style.color = '#667eea';
            chevron.style.opacity = '1';
        }
    }

    console.log(`[${pageLogPrefix}] Directory Name sort updated`, {
        sortByName,
        sortDirection
    });
    applyFilters();
}

function toggleSourcesFilter(sourceCount, button, event) {
    if (event) {
        event.stopPropagation();
    }

    const count = parseInt(sourceCount, 10);
    if (currentSourcesFilters.includes(count)) {
        currentSourcesFilters = currentSourcesFilters.filter(value => value !== count);
        button.classList.remove('active');
    } else {
        currentSourcesFilters.push(count);
        button.classList.add('active');
    }
    applyFilters();
}

document.getElementById('name-header')?.addEventListener('click', () => {
    toggleNameSort();
});

document.getElementById('submission-header').addEventListener('click', event => {
    if (!event.target.closest('.filter-btn')) {
        document.getElementById('submission-filters-dropdown').classList.toggle('open');
        document.querySelector('#submission-header .th-chevron').classList.toggle('open');
    }
});

document.getElementById('sources-header').addEventListener('click', event => {
    if (!event.target.closest('.filter-btn')) {
        document.getElementById('sources-filters').classList.toggle('open');
        document.querySelector('#sources-header .th-chevron').classList.toggle('open');
    }
});

document.querySelectorAll('#submission-filters-dropdown .filter-btn').forEach(button => {
    button.addEventListener('click', event => {
        const isActive = event.target.classList.contains('active');
        document.querySelectorAll('#submission-filters-dropdown .filter-btn').forEach(filterButton => {
            filterButton.classList.remove('active');
        });

        if (isActive) {
            currentSubmissionFilter = null;
        } else {
            event.target.classList.add('active');
            currentSubmissionFilter = event.target.dataset.filter;
        }
        applyFilters();
    });
});

const freeToolsDropdown = document.querySelector('#free-tools-toggle')?.parentElement;
const servicesDropdown = document.querySelector('#services-toggle')?.parentElement;

document.getElementById('free-tools-toggle')?.addEventListener('click', event => {
    const menu = document.getElementById('free-tools-menu');
    const toggle = event.currentTarget;
    menu?.classList.toggle('open');
    toggle?.classList.toggle('open');
});

document.getElementById('services-toggle')?.addEventListener('click', event => {
    const menu = document.getElementById('services-menu');
    const toggle = event.currentTarget;
    menu?.classList.toggle('open');
    toggle?.classList.toggle('open');
});

freeToolsDropdown?.addEventListener('mouseenter', () => {
    document.getElementById('free-tools-menu')?.classList.add('open');
    document.getElementById('free-tools-toggle')?.classList.add('open');
});

freeToolsDropdown?.addEventListener('mouseleave', () => {
    document.getElementById('free-tools-menu')?.classList.remove('open');
    document.getElementById('free-tools-toggle')?.classList.remove('open');
});

servicesDropdown?.addEventListener('mouseenter', () => {
    document.getElementById('services-menu')?.classList.add('open');
    document.getElementById('services-toggle')?.classList.add('open');
});

servicesDropdown?.addEventListener('mouseleave', () => {
    document.getElementById('services-menu')?.classList.remove('open');
    document.getElementById('services-toggle')?.classList.remove('open');
});

document.addEventListener('click', event => {
    const dropdowns = document.querySelectorAll('.dropdown');
    let clickedInDropdown = false;

    dropdowns.forEach(dropdown => {
        if (dropdown.contains(event.target)) {
            clickedInDropdown = true;
        }
    });

    if (!clickedInDropdown) {
        document.getElementById('free-tools-menu')?.classList.remove('open');
        document.getElementById('free-tools-toggle')?.classList.remove('open');
        document.getElementById('services-menu')?.classList.remove('open');
        document.getElementById('services-toggle')?.classList.remove('open');
    }

    if (!event.target.closest('#type-header')) {
        document.getElementById('type-filters')?.classList.remove('open');
        document.querySelector('#type-header .th-chevron')?.classList.remove('open');
    }

    if (!event.target.closest('#submission-header')) {
        document.getElementById('submission-filters-dropdown')?.classList.remove('open');
        document.querySelector('#submission-header .th-chevron')?.classList.remove('open');
    }

    if (!event.target.closest('#sources-header')) {
        document.getElementById('sources-filters')?.classList.remove('open');
        document.querySelector('#sources-header .th-chevron')?.classList.remove('open');
    }
});

document.getElementById('prev-btn')?.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage -= 1;
        renderTable();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

document.getElementById('next-btn')?.addEventListener('click', () => {
    const totalPages = Math.ceil(filteredDirectories.length / ITEMS_PER_PAGE);
    if (currentPage < totalPages) {
        currentPage += 1;
        renderTable();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

(async () => {
    setupDownloadActions();
    await loadDirectories();

    setTimeout(() => {
        const schemaGen = new SchemaGenerator();
        const config = window[schemaConfigName] || SAAS_DIRECTORIES_SCHEMA_CONFIG;
        const schemas = [];

        if (config.organization.enabled) {
            schemas.push({
                schema: schemaGen.generateOrganization(),
                id: 'org-schema'
            });
        }

        if (config.breadcrumb.enabled) {
            schemas.push({
                schema: schemaGen.generateBreadcrumb(config.breadcrumb.items),
                id: 'breadcrumb-schema'
            });
        }

        if (config.dataset.enabled) {
            schemas.push({
                schema: schemaGen.generateDataset({
                    ...config.dataset,
                    url: config.pageUrl,
                    itemCount: filteredDirectories.length,
                    creator: config.organization
                }),
                id: 'dataset-schema'
            });
        }

        if (config.faq.enabled) {
            const faqs = config.faq.extractFromDOM
                ? schemaGen.extractFAQsFromDOM()
                : config.faq.faqs;

            if (faqs.length > 0) {
                schemas.push({
                    schema: schemaGen.generateFAQPage(faqs, config.pageUrl),
                    id: 'faq-schema'
                });
            }
        }

        schemaGen.injectSchemas(schemas);
    }, 100);
})();